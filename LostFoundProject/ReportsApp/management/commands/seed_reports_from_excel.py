from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ReportsApp.models import ItemReport, Category, Location
from datetime import datetime
import pandas as pd
from django.utils import timezone
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed item reports from Excel file using existing categories and locations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='reports_lost_only.xlsx',
            help='Path to the Excel file (default: reports_lost_only.xlsx)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed reports from Excel...'))
        
        # Get the base directory (where manage.py is located)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        excel_path = os.path.join(base_dir, options['file'])
        
        # Read Excel file
        try:
            self.stdout.write(f'Reading Excel file from: {excel_path}')
            df = pd.read_excel(excel_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading Excel file: {str(e)}'))
            return

        # Get existing categories and locations from database
        existing_categories = {cat.name.lower(): cat for cat in Category.objects.all()}
        existing_locations = {loc.name.lower(): loc for loc in Location.objects.all()}

        self.stdout.write(f'Found {len(existing_categories)} existing categories and {len(existing_locations)} existing locations')

        # Process each row
        created_count = 0
        skipped_count = 0
        for index, row in df.iterrows():
            try:
                # Get or create user based on email
                if pd.isna(row['reporter_email']):
                    self.stdout.write(self.style.WARNING(f'Skipping row {index + 2}: No reporter email'))
                    skipped_count += 1
                    continue

                user, created = User.objects.get_or_create(
                    email=row['reporter_email'],
                    defaults={
                        'username': row['reporter_email'].split('@')[0],
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new user: {user.email}'))

                # Get category and location from existing ones
                category = None
                location = None
                
                if not pd.isna(row['category']):
                    category_name = str(row['category']).lower()
                    category = existing_categories.get(category_name)
                    if not category:
                        self.stdout.write(self.style.WARNING(f'Skipping row {index + 2}: Category "{row["category"]}" not found in database'))
                        skipped_count += 1
                        continue

                if not pd.isna(row['location']):
                    location_name = str(row['location']).lower()
                    location = existing_locations.get(location_name)
                    if not location:
                        self.stdout.write(self.style.WARNING(f'Skipping row {index + 2}: Location "{row["location"]}" not found in database'))
                        skipped_count += 1
                        continue

                # Convert timestamp
                try:
                    timestamp = pd.to_datetime(row['timestamp_reported'])
                    if pd.isna(timestamp):
                        timestamp = timezone.now()
                except:
                    timestamp = timezone.now()

                # Create the report using only the new ForeignKey fields
                report, created = ItemReport.objects.get_or_create(
                    title=row['item_name'],
                    reporter=user,
                    defaults={
                        'description': row['description'] if not pd.isna(row['description']) else '',
                        'category': category,  # Using the new ForeignKey field
                        'location': location,  # Using the new ForeignKey field
                        'date_lost_or_found': timestamp.date(),
                        'time_lost_or_found': timestamp.time(),
                        'status': 'lost',  # Since this is lost_only.xlsx
                        'timestamp_reported': timestamp,
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created report: {report.title} by {report.reporter.email}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Report already exists: {report.title} by {report.reporter.email}'
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error processing row {index + 2}: {str(e)}'
                    )
                )
                skipped_count += 1
                continue

        self.stdout.write(
            self.style.SUCCESS(
                f'Reports seeding completed!\n'
                f'Created: {created_count} new reports\n'
                f'Skipped: {skipped_count} rows\n'
                f'Using {len(existing_categories)} existing categories\n'
                f'Using {len(existing_locations)} existing locations'
            )
        ) 