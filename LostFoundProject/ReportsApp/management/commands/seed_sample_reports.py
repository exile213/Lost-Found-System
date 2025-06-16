from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ReportsApp.models import ItemReport, Category, Location
from datetime import date, time

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed sample item reports with categories and locations'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed sample reports...'))
        
        # Get or create categories
        electronics, _ = Category.objects.get_or_create(name='Electronics')
        documents, _ = Category.objects.get_or_create(name='Documents')
        accessories, _ = Category.objects.get_or_create(name='Accessories')
        clothing, _ = Category.objects.get_or_create(name='Clothing')
        
        # Get or create locations
        library, _ = Location.objects.get_or_create(name='Library')
        cafeteria, _ = Location.objects.get_or_create(name='Cafeteria')
        classroom, _ = Location.objects.get_or_create(name='Classroom')
        parking_lot, _ = Location.objects.get_or_create(name='Parking Lot')
        computer_lab, _ = Location.objects.get_or_create(name='Computer Lab')
        
        # Get users
        try:
            trial_user = User.objects.get(username='trial')
            emil_user = User.objects.get(username='emil123')
            trial234_user = User.objects.get(username='trial234')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Users not found. Please run seed_users command first.'))
            return
        
        # Sample reports data
        sample_reports = [
            {
                'title': 'Lost Laptop',
                'description': 'Black Dell laptop with stickers on the lid',
                'category': electronics,
                'location': library,
                'date_lost_or_found': date(2025, 6, 11),
                'time_lost_or_found': time(14, 30),
                'status': 'lost',
                'reporter': trial_user,
            },
            {
                'title': 'Found Student ID',
                'description': 'Student ID card found near the cafeteria entrance',
                'category': documents,
                'location': cafeteria,
                'date_lost_or_found': date(2025, 6, 12),
                'time_lost_or_found': time(12, 15),
                'status': 'found',
                'reporter': emil_user,
            },
            {
                'title': 'Lost Keys',
                'description': 'Set of keys with a red keychain',
                'category': accessories,
                'location': classroom,
                'date_lost_or_found': date(2025, 6, 12),
                'time_lost_or_found': time(9, 45),
                'status': 'lost',
                'reporter': trial234_user,
            },
            {
                'title': 'Found Water Bottle',
                'description': 'Blue stainless steel water bottle',
                'category': accessories,
                'location': computer_lab,
                'date_lost_or_found': date(2025, 6, 13),
                'time_lost_or_found': time(16, 20),
                'status': 'found',
                'reporter': trial_user,
            },
            {
                'title': 'Lost Jacket',
                'description': 'Black hoodie with university logo',
                'category': clothing,
                'location': parking_lot,
                'date_lost_or_found': date(2025, 6, 13),
                'time_lost_or_found': time(18, 0),
                'status': 'lost',
                'reporter': trial234_user,
            },
            {
                'title': 'Found Calculator',
                'description': 'Scientific calculator, brand: Casio',
                'category': electronics,
                'location': library,
                'date_lost_or_found': date(2025, 6, 14),
                'time_lost_or_found': time(10, 30),
                'status': 'found',
                'reporter': emil_user,
            },
        ]
        
        created_count = 0
        for report_data in sample_reports:
            report, created = ItemReport.objects.get_or_create(
                title=report_data['title'],
                reporter=report_data['reporter'],
                defaults=report_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created report: {report.title} by {report.reporter.username}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Report already exists: {report.title} by {report.reporter.username}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Sample reports seeding completed! Created {created_count} new reports.'
            )
        ) 