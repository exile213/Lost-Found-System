from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Seed all data: categories, locations, users, and sample reports'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting comprehensive data seeding...'))
        
        # Step 1: Seed categories and locations
        self.stdout.write(self.style.SUCCESS('Step 1: Seeding categories and locations...'))
        call_command('populate_categories_locations')
        
        # Step 2: Seed users
        self.stdout.write(self.style.SUCCESS('Step 2: Seeding users...'))
        call_command('seed_users')
        
        # Step 3: Seed sample reports
        self.stdout.write(self.style.SUCCESS('Step 3: Seeding sample reports...'))
        call_command('seed_sample_reports')
        
        self.stdout.write(self.style.SUCCESS('All data seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now test the application with:'))
        self.stdout.write(self.style.SUCCESS('- admin/admin123 (superuser)'))
        self.stdout.write(self.style.SUCCESS('- trial/trial123 (student)'))
        self.stdout.write(self.style.SUCCESS('- emil123/emil123 (staff)'))
        self.stdout.write(self.style.SUCCESS('- trial234/trial234 (student)')) 