"""
SDC4 App Installer - Automated installation of generated DM apps.

This module provides the core logic for installing generated Django app ZIPs
into an existing SDC4 project. It handles:
- ZIP validation and extraction
- File operations with rollback capability
- Configuration updates (settings.py, urls.py)
- Database migrations
- Triplestore (Fuseki/GraphDB) RDF upload
"""
import os
import ast
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from django.conf import settings
from django.core.management import call_command


@dataclass
class InstallationResult:
    """Result of an app installation attempt."""
    success: bool
    app_name: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    installed_files: List[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0


class AppInstaller:
    """
    Core logic for installing generated DM apps from ZIP archives.

    Usage:
        installer = AppInstaller(zip_path='/path/to/app.zip')
        result = installer.install()

        if result.success:
            print(f"Successfully installed {result.app_name}")
        else:
            print(f"Installation failed: {result.errors}")
    """

    def __init__(self, zip_path: str, stdout=None):
        """
        Initialize the installer.

        Args:
            zip_path: Path to the ZIP file containing the generated app
            stdout: Optional output stream for progress messages (for management commands)
        """
        self.zip_path = Path(zip_path)
        self.stdout = stdout
        self.base_dir = Path(settings.BASE_DIR)
        self.temp_dir = None
        self.app_name = None
        self.rollback_actions = []  # Stack of rollback functions

    def _log(self, message: str, style=None):
        """Log a message to stdout if available."""
        if self.stdout:
            if style:
                self.stdout.write(style(message))
            else:
                self.stdout.write(message)

    def install(self) -> InstallationResult:
        """
        Main installation entry point.

        Returns:
            InstallationResult with success status and details
        """
        result = InstallationResult(
            success=False,
            app_name='',
        )

        try:
            # 1. Validate ZIP file
            self._log("Validating ZIP file...")
            validation_errors = self._validate_zip()
            if validation_errors:
                result.errors.extend(validation_errors)
                return result

            # 2. Extract to temp directory
            self._log("Extracting ZIP archive...")
            self.temp_dir = self._extract_zip()

            # 3. Detect app name from structure
            self._log("Detecting app name...")
            self.app_name = self._detect_app_name()
            result.app_name = self.app_name

            # 4. Check for conflicts
            self._log(f"Checking for conflicts with app '{self.app_name}'...")
            conflict_errors = self._check_conflicts()
            if conflict_errors:
                result.errors.extend(conflict_errors)
                return result

            # 5. Copy app directory
            self._log(f"Installing app '{self.app_name}'...")
            self._copy_app_directory()

            # 6. Copy dmlib files
            self._log("Copying schema files to dmlib...")
            self._copy_dmlib_files()

            # 7. Update configuration
            self._log("Updating settings.py...")
            self._update_settings()

            self._log("Updating urls.py...")
            self._update_urls()

            # 8. Run migrations
            self._log("Running database migrations...")
            self._run_migrations()

            # 9. Upload to triplestore
            self._log("Uploading RDF data to triplestore...")
            triplestore_warnings = self._upload_to_triplestore()
            if triplestore_warnings:
                result.warnings.extend(triplestore_warnings)

            # 10. Verify installation
            self._log("Verifying installation...")
            verification_errors = self._verify_installation()
            if verification_errors:
                result.errors.extend(verification_errors)
                # Don't rollback - app might still be usable
                result.warnings.append("App installed but verification had issues")

            result.success = True
            self._log(f"Successfully installed app '{self.app_name}'!")

        except Exception as e:
            result.errors.append(f"Installation failed: {str(e)}")
            self._log(f"ERROR: {str(e)}")

            # Attempt rollback
            if self.rollback_actions:
                self._log("Rolling back changes...")
                self._rollback()

        finally:
            # Cleanup temp directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)

        return result

    def _validate_zip(self) -> List[str]:
        """
        Validate ZIP file structure.

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Check file exists
        if not self.zip_path.exists():
            errors.append(f"ZIP file not found: {self.zip_path}")
            return errors

        # Check it's a valid ZIP
        if not zipfile.is_zipfile(self.zip_path):
            errors.append(f"Not a valid ZIP file: {self.zip_path}")
            return errors

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zf:
                # Check for bad ZIP
                bad_file = zf.testzip()
                if bad_file:
                    errors.append(f"Corrupt file in ZIP: {bad_file}")

                # Verify structure (should contain at least one app directory)
                file_list = zf.namelist()

                # Look for sdc_project/{app_name}/ structure
                # Generated ZIPs have: sdc_project/{app_name}/models.py, etc.
                app_dirs = [f for f in file_list if f.count('/') >= 2 and 'models.py' in f]
                if not app_dirs:
                    errors.append(
                        "Invalid ZIP structure. Expected: sdc_project/{app_name}/models.py"
                    )

                # Verify dmlib files exist
                dmlib_files = [f for f in file_list if 'mediafiles/dmlib/dm-' in f]
                if not dmlib_files:
                    errors.append(
                        "No schema files found. Expected: mediafiles/dmlib/dm-*.xsd"
                    )

        except Exception as e:
            errors.append(f"Error reading ZIP: {str(e)}")

        return errors

    def _extract_zip(self) -> str:
        """
        Extract ZIP to temporary directory.

        Returns:
            Path to temp directory
        """
        temp_dir = tempfile.mkdtemp(prefix='sdc_app_install_')

        with zipfile.ZipFile(self.zip_path, 'r') as zf:
            zf.extractall(temp_dir)

        return temp_dir

    # Infrastructure apps that should be excluded when detecting the data model app
    INFRASTRUCTURE_APPS = {
        'api',
        'core',
        'generic_storage',
        'sdc4',
        'templates',
        'staticfiles',
        'mediafiles',
        'ontologies',
        'docs',
    }

    def _detect_app_name(self) -> str:
        """
        Detect app name from extracted ZIP structure.

        Handles two structures:
        1. {temp_dir}/sdc_project/{app_name}/models.py (legacy)
        2. {temp_dir}/sdc_project/{project_name}/{app_name}/models.py (current)

        Excludes infrastructure apps (api, core, generic_storage, etc.) that are
        part of the project template but are not the data model app to install.

        Returns:
            App name

        Raises:
            ValueError if app name cannot be detected
        """
        sdc_project_dir = Path(self.temp_dir) / 'sdc_project'

        if not sdc_project_dir.exists():
            raise ValueError("Invalid ZIP: missing 'sdc_project' directory")

        # Find app directories (directories with models.py), excluding infrastructure apps
        # First try direct children (legacy structure)
        app_dirs = [
            d for d in sdc_project_dir.iterdir()
            if d.is_dir()
            and (d / 'models.py').exists()
            and d.name not in self.INFRASTRUCTURE_APPS
        ]

        # If not found, look one level deeper (current structure with project directory)
        if not app_dirs:
            for project_dir in sdc_project_dir.iterdir():
                if project_dir.is_dir():
                    app_dirs = [
                        d for d in project_dir.iterdir()
                        if d.is_dir()
                        and (d / 'models.py').exists()
                        and d.name not in self.INFRASTRUCTURE_APPS
                    ]
                    if app_dirs:
                        # Update sdc_project_dir to point to the actual project directory
                        # This allows the rest of the installer to work correctly
                        self._sdc_project_path = project_dir
                        break

        if not app_dirs:
            raise ValueError("No app directory found in ZIP")

        if len(app_dirs) > 1:
            raise ValueError(f"Multiple app directories found: {[d.name for d in app_dirs]}")

        return app_dirs[0].name

    def _check_conflicts(self) -> List[str]:
        """
        Check for conflicts with existing apps.

        Returns:
            List of error messages (empty if no conflicts)
        """
        errors = []

        # Check if app directory already exists
        app_path = self.base_dir / self.app_name
        if app_path.exists():
            errors.append(
                f"App '{self.app_name}' already exists at {app_path}. "
                "Remove the existing app before reinstalling."
            )

        # Check if app is already in INSTALLED_APPS
        if self.app_name in settings.INSTALLED_APPS:
            errors.append(
                f"App '{self.app_name}' is already in INSTALLED_APPS"
            )

        return errors

    def _copy_app_directory(self):
        """Copy app directory from temp to project root with rollback support."""
        # Use the detected project path if available (for nested structure)
        if hasattr(self, '_sdc_project_path'):
            source = self._sdc_project_path / self.app_name
        else:
            source = Path(self.temp_dir) / 'sdc_project' / self.app_name

        dest = self.base_dir / self.app_name

        try:
            shutil.copytree(source, dest)

            # Fix ownership to match project directory
            # This prevents root-owned files when running in Docker as root
            self._fix_ownership(dest)

            # Register rollback
            self.rollback_actions.append(lambda: shutil.rmtree(dest) if dest.exists() else None)

        except Exception as e:
            raise ValueError(f"Failed to copy app directory: {str(e)}")

    def _copy_dmlib_files(self):
        """Copy dm-*.* files from ZIP to mediafiles/dmlib/ with rollback support."""
        # Use the detected project path if available (for nested structure)
        if hasattr(self, '_sdc_project_path'):
            source_dmlib = self._sdc_project_path / 'mediafiles' / 'dmlib'
        else:
            source_dmlib = Path(self.temp_dir) / 'sdc_project' / 'mediafiles' / 'dmlib'

        dest_dmlib = self.base_dir / 'mediafiles' / 'dmlib'

        if not source_dmlib.exists():
            raise ValueError("No dmlib directory found in ZIP")

        # Create destination if it doesn't exist
        dest_dmlib.mkdir(parents=True, exist_ok=True)

        # Copy all dm-* files
        copied_files = []
        for file_path in source_dmlib.glob('dm-*'):
            if file_path.is_file():
                dest_file = dest_dmlib / file_path.name

                # Check if file already exists
                if dest_file.exists():
                    # Backup existing file
                    backup_file = dest_file.with_suffix(dest_file.suffix + '.backup')
                    shutil.copy2(dest_file, backup_file)

                    # Register rollback to restore backup
                    self.rollback_actions.append(
                        lambda f=dest_file, b=backup_file: (
                            shutil.move(b, f) if b.exists() else None
                        )
                    )
                else:
                    # Register rollback to delete new file
                    self.rollback_actions.append(
                        lambda f=dest_file: f.unlink() if f.exists() else None
                    )

                # Copy file
                shutil.copy2(file_path, dest_file)
                copied_files.append(dest_file)

        if not copied_files:
            raise ValueError("No dm-* files found in ZIP to copy")

    def _update_settings(self):
        """
        Update settings.py to add app to INSTALLED_APPS using AST.

        Reuses the pattern from AppGenerator._register_app()
        """
        # Determine project name from settings module
        project_name = settings.SETTINGS_MODULE.split('.')[0]
        settings_path = self.base_dir / project_name / 'settings.py'

        if not settings_path.exists():
            raise ValueError(f"settings.py not found at {settings_path}")

        # Backup settings.py
        backup_path = settings_path.with_suffix('.py.backup')
        shutil.copy2(settings_path, backup_path)

        # Register rollback
        self.rollback_actions.append(
            lambda: shutil.move(backup_path, settings_path) if backup_path.exists() else None
        )

        try:
            with open(settings_path, 'r') as f:
                content = f.read()

            # Quick check if already registered (shouldn't happen, but safety check)
            if f"'{self.app_name}'" in content:
                self._log(f"Warning: App '{self.app_name}' already in INSTALLED_APPS")
                return

            # Parse AST
            tree = ast.parse(content)
            modified = False

            # Find INSTALLED_APPS assignment
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == 'INSTALLED_APPS':
                            if isinstance(node.value, (ast.List, ast.Tuple)):
                                # Insert app name at the end (before any closing comments)
                                new_app = ast.Constant(value=self.app_name)
                                if isinstance(node.value, ast.List):
                                    node.value.elts.append(new_app)
                                else:  # Tuple
                                    node.value.elts = list(node.value.elts) + [new_app]
                                modified = True
                                break

            if modified:
                # Unparse AST back to code
                new_content = ast.unparse(tree)
                with open(settings_path, 'w') as f:
                    f.write(new_content)
                self._log(f"Added '{self.app_name}' to INSTALLED_APPS")
            else:
                self._log("Warning: Could not find INSTALLED_APPS in settings.py")

        except Exception as e:
            raise ValueError(f"Failed to update settings.py: {str(e)}")

    def _update_urls(self):
        """
        Update urls.py to add app URL pattern.

        Reuses the pattern from AppGenerator._register_app()
        """
        project_name = settings.SETTINGS_MODULE.split('.')[0]
        urls_path = self.base_dir / project_name / 'urls.py'

        if not urls_path.exists():
            raise ValueError(f"urls.py not found at {urls_path}")

        # Backup urls.py
        backup_path = urls_path.with_suffix('.py.backup')
        shutil.copy2(urls_path, backup_path)

        # Register rollback
        self.rollback_actions.append(
            lambda: shutil.move(backup_path, urls_path) if backup_path.exists() else None
        )

        try:
            with open(urls_path, 'r') as f:
                content = f.read()

            # Check if already registered
            if f"path('{self.app_name}/'" in content:
                self._log(f"Warning: URL pattern for '{self.app_name}' already exists")
                return

            # Add include import if missing
            if "include" not in content and "from django.urls import" in content:
                content = content.replace(
                    "from django.urls import path",
                    "from django.urls import path, include"
                )

            # Add path to urlpatterns
            if "urlpatterns = [" in content:
                content = content.replace(
                    "urlpatterns = [",
                    f"urlpatterns = [\n    path('{self.app_name}/', include('{self.app_name}.urls', namespace='{self.app_name}')),"
                )

                with open(urls_path, 'w') as f:
                    f.write(content)

                self._log(f"Added '{self.app_name}/' to project URLs")
            else:
                self._log("Warning: Could not find urlpatterns in urls.py")

        except Exception as e:
            raise ValueError(f"Failed to update urls.py: {str(e)}")

    def _run_migrations(self):
        """
        Run migrations for the app.

        Note: Generated apps already include migrations, so we skip makemigrations
        and just apply the existing migrations with migrate.
        """
        try:
            # Check if migrations directory exists in the app
            migrations_dir = self.base_dir / self.app_name / 'migrations'

            if migrations_dir.exists():
                self._log(f"App already has migrations, skipping makemigrations...")
            else:
                # Run makemigrations only if migrations don't exist
                self._log(f"Running makemigrations for {self.app_name}...")
                try:
                    call_command('makemigrations', self.app_name, verbosity=0)
                except SystemExit as e:
                    if e.code != 0:
                        # Non-fatal - migrations might already exist
                        self._log(f"makemigrations exited with code {e.code} (may be expected)")

            # Run migrate to apply migrations
            self._log("Running migrate...")
            call_command('migrate', verbosity=0)

        except SystemExit as e:
            # migrate should not exit, but catch it just in case
            if e.code != 0:
                raise ValueError(
                    f"Migration command exited with code {e.code}. "
                    f"Check Django logs for details."
                )
        except Exception as e:
            raise ValueError(f"Migration failed: {str(e)}")

    def _upload_to_triplestore(self) -> List[str]:
        """
        Upload RDF/TTL files to the appropriate triplestore.

        Detects profile (lightweight=Fuseki, enterprise=GraphDB) from settings
        and uploads dm-*.ttl and dm-*.rdf files.

        Returns:
            List of warning messages (non-fatal errors)
        """
        warnings = []

        # Detect triplestore backend
        backend = self._detect_triplestore_backend()

        if backend == 'none':
            warnings.append("Triplestore disabled - skipping RDF upload")
            return warnings

        # Get dmlib directory
        dmlib_dir = self.base_dir / 'mediafiles' / 'dmlib'

        # Find dm-*.ttl and dm-*.rdf files (recently copied)
        rdf_files = list(dmlib_dir.glob('dm-*.ttl')) + list(dmlib_dir.glob('dm-*.rdf'))

        if not rdf_files:
            warnings.append("No RDF files found to upload")
            return warnings

        # Upload based on backend
        try:
            if backend == 'fuseki':
                self._upload_to_fuseki(rdf_files)
            elif backend == 'graphdb':
                self._upload_to_graphdb(rdf_files)
        except Exception as e:
            warnings.append(f"Triplestore upload failed (non-fatal): {str(e)}")

        return warnings

    def _detect_triplestore_backend(self) -> str:
        """
        Detect triplestore backend from settings.

        Returns:
            'fuseki', 'graphdb', or 'none'
        """
        # Check for explicit TRIPLESTORE_BACKEND setting
        backend = getattr(settings, 'TRIPLESTORE_BACKEND', None)
        if backend:
            return backend.lower()

        # Infer from presence of settings
        if hasattr(settings, 'GRAPHDB_URL'):
            return 'graphdb'
        elif hasattr(settings, 'FUSEKI_URL'):
            return 'fuseki'
        else:
            return 'none'

    def _upload_to_fuseki(self, rdf_files: List[Path]):
        """Upload RDF files to Fuseki."""
        import requests

        fuseki_url = getattr(settings, 'FUSEKI_URL')
        fuseki_user = getattr(settings, 'FUSEKI_USER', 'admin')
        fuseki_password = getattr(settings, 'FUSEKI_PASSWORD', 'admin123')
        auth = (fuseki_user, fuseki_password)

        for rdf_file in rdf_files:
            self._log(f"Uploading {rdf_file.name} to Fuseki...")

            content_type = 'text/turtle' if rdf_file.suffix == '.ttl' else 'application/rdf+xml'

            with open(rdf_file, 'rb') as f:
                response = requests.post(
                    f"{fuseki_url}/data",
                    headers={'Content-Type': content_type},
                    auth=auth,
                    data=f.read(),
                    timeout=30
                )

            if response.status_code not in [200, 201, 204]:
                # Check if duplicate (non-fatal)
                if 'duplicate' in response.text.lower():
                    self._log(f"Warning: {rdf_file.name} already loaded in Fuseki")
                else:
                    raise ValueError(f"Fuseki upload failed: {response.status_code} - {response.text}")

    def _upload_to_graphdb(self, rdf_files: List[Path]):
        """Upload RDF files to GraphDB."""
        import requests

        graphdb_url = getattr(settings, 'GRAPHDB_URL')
        graphdb_repo = getattr(settings, 'GRAPHDB_REPOSITORY')
        graphdb_user = getattr(settings, 'GRAPHDB_USER', 'admin')
        graphdb_password = getattr(settings, 'GRAPHDB_PASSWORD', 'admin123')
        auth = (graphdb_user, graphdb_password)

        for rdf_file in rdf_files:
            self._log(f"Uploading {rdf_file.name} to GraphDB...")

            content_type = 'text/turtle' if rdf_file.suffix == '.ttl' else 'application/rdf+xml'

            with open(rdf_file, 'rb') as f:
                response = requests.post(
                    f"{graphdb_url}/repositories/{graphdb_repo}/statements",
                    headers={'Content-Type': content_type},
                    auth=auth,
                    data=f.read(),
                    timeout=30
                )

            if response.status_code not in [200, 201, 204]:
                raise ValueError(f"GraphDB upload failed: {response.status_code} - {response.text}")

    def _verify_installation(self) -> List[str]:
        """
        Verify the app was installed correctly.

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Check app directory exists
        app_path = self.base_dir / self.app_name
        if not app_path.exists():
            errors.append(f"App directory not found: {app_path}")

        # Check app can be imported
        try:
            __import__(self.app_name)
        except ImportError as e:
            errors.append(f"App import failed: {str(e)}")

        # Check app is in INSTALLED_APPS
        if self.app_name not in settings.INSTALLED_APPS:
            errors.append(f"App '{self.app_name}' not in INSTALLED_APPS")

        return errors

    def _fix_ownership(self, directory: Path):
        """
        Fix ownership of directory to match project owner.

        This prevents root-owned files when running as root in Docker.
        The directory ownership will match the BASE_DIR ownership.

        Args:
            directory: Path to directory to fix ownership for
        """
        try:
            # Get the uid/gid of the project's BASE_DIR
            stat_info = os.stat(self.base_dir)
            target_uid = stat_info.st_uid
            target_gid = stat_info.st_gid

            # Get current process uid/gid
            current_uid = os.getuid()

            # Only attempt chown if running as root or owner
            if current_uid != 0 and current_uid != target_uid:
                self._log(f"Skipping ownership fix (not root and not owner)")
                return

            # Recursively change ownership
            for root, dirs, files in os.walk(directory):
                # Change directory ownership
                try:
                    os.chown(root, target_uid, target_gid)
                except (OSError, PermissionError) as e:
                    # Non-fatal - log and continue
                    self._log(f"Warning: Could not chown {root}: {e}")

                # Change file ownership
                for name in files:
                    filepath = os.path.join(root, name)
                    try:
                        os.chown(filepath, target_uid, target_gid)
                    except (OSError, PermissionError) as e:
                        # Non-fatal - log and continue
                        self._log(f"Warning: Could not chown {filepath}: {e}")

            self._log(f"Fixed ownership of {directory} to match project owner ({target_uid}:{target_gid})")

        except Exception as e:
            # Non-fatal - ownership fix is a nice-to-have
            self._log(f"Warning: Ownership fix failed (non-fatal): {str(e)}")

    def _rollback(self):
        """Execute rollback actions in reverse order."""
        self._log("Rolling back changes...")

        # Execute rollback actions in reverse order (LIFO)
        for action in reversed(self.rollback_actions):
            try:
                action()
            except Exception as e:
                self._log(f"Warning: Rollback action failed: {str(e)}")

        self.rollback_actions.clear()
