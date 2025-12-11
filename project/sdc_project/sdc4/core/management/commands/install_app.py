"""
Django management command to install a generated DM app from a ZIP file.

Usage:
    python manage.py install_app /path/to/app.zip
    python manage.py install_app /path/to/app.zip --force  # Skip confirmation
"""
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from sdc4.utils.app_installer import AppInstaller


class Command(BaseCommand):
    help = 'Install a generated SDC4 DM app from a ZIP archive'

    def add_arguments(self, parser):
        parser.add_argument(
            'zip_file',
            type=str,
            help='Path to the ZIP file containing the generated app'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt'
        )

    def handle(self, *args, **options):
        zip_path = options['zip_file']
        force = options['force']

        # Validate file exists
        if not Path(zip_path).exists():
            raise CommandError(f"ZIP file not found: {zip_path}")

        self.stdout.write(self.style.MIGRATE_HEADING('\nSDC4 App Installer'))
        self.stdout.write(f"ZIP file: {zip_path}\n")

        # Confirmation prompt
        if not force:
            confirm = input("Proceed with installation? [y/N]: ")
            if confirm.lower() not in ['y', 'yes']:
                self.stdout.write(self.style.WARNING("Installation cancelled."))
                return

        # Run installation
        installer = AppInstaller(zip_path, stdout=self.stdout)
        result = installer.install()

        # Display results
        self.stdout.write("\n" + "="*60)

        if result.success:
            self.stdout.write(self.style.SUCCESS(f"\nSuccessfully installed app: {result.app_name}"))

            if result.warnings:
                self.stdout.write(self.style.WARNING("\nWarnings:"))
                for warning in result.warnings:
                    self.stdout.write(f"  - {warning}")

            self.stdout.write("\nNext steps:")
            self.stdout.write(f"  1. Restart your Django server")
            self.stdout.write(f"  2. Visit: http://localhost:8000/{result.app_name}/")
            self.stdout.write(f"  3. Access admin: http://localhost:8000/admin/")
        else:
            self.stdout.write(self.style.ERROR(f"\nInstallation failed!"))
            self.stdout.write(self.style.ERROR("\nErrors:"))
            for error in result.errors:
                self.stdout.write(f"  - {error}")

            if result.warnings:
                self.stdout.write(self.style.WARNING("\nWarnings:"))
                for warning in result.warnings:
                    self.stdout.write(f"  - {warning}")

            raise CommandError("Installation failed. See errors above.")
