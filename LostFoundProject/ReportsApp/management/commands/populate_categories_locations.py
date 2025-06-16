from django.core.management.base import BaseCommand
from ReportsApp.models import Category, Location

class Command(BaseCommand):
    help = 'Populate Category and Location tables with initial data'

    def handle(self, *args, **options):
        # Initial categories
        categories = [
            'Electronics',
            'Clothing',
            'Documents',
            'Accessories',
            'Other',
        ]
        
        # Initial locations
        locations = [
            'Library',
            'Cafeteria',
            'Classroom',
            'Dormitory',
            'Other',
        ]
        
        # Create categories
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category_name}')
                )
        
        # Create locations
        for location_name in locations:
            location, created = Location.objects.get_or_create(name=location_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created location: {location_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Location already exists: {location_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated Category and Location tables')
        ) 