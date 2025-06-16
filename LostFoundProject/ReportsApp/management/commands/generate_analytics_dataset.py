from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from ReportsApp.models import ItemReport, Category, Location
from ClaimsApp.models import ClaimRequest
from datetime import datetime, timedelta
import random
from faker import Faker

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Generate comprehensive fake dataset for 2020-2024 analytics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=100,
            help='Number of users to create (default: 100)'
        )
        parser.add_argument(
            '--reports',
            type=int,
            default=500,
            help='Number of reports to create (default: 500)'
        )
        parser.add_argument(
            '--claims',
            type=int,
            default=150,
            help='Number of claims to create (default: 150)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting analytics dataset generation...'))
        
        # Create categories and locations
        self.create_categories_and_locations()
        
        # Create users
        users = self.create_users(options['users'])
        
        # Create reports
        reports = self.create_reports(users, options['reports'])
        
        # Create claims
        self.create_claims(users, reports, options['claims'])
        
        self.stdout.write(self.style.SUCCESS('Analytics dataset generation completed!'))

    def create_categories_and_locations(self):
        """Create categories and locations for the dataset"""
        categories = [
            'Electronics', 'Documents', 'Accessories', 'Clothing', 'Books',
            'Jewelry', 'Sports Equipment', 'Musical Instruments', 'Tools',
            'Personal Care', 'Food & Beverages', 'Art Supplies'
        ]
        
        locations = [
            'Library', 'Cafeteria', 'Classroom A101', 'Classroom B205', 'Computer Lab',
            'Parking Lot A', 'Parking Lot B', 'Student Center', 'Gymnasium',
            'Administration Building', 'Science Lab', 'Art Studio', 'Music Room',
            'Study Hall', 'Campus Store', 'Dormitory A', 'Dormitory B',
            'Sports Complex', 'Auditorium', 'Medical Center'
        ]
        
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
            
        for location_name in locations:
            Location.objects.get_or_create(name=location_name)
            
        self.stdout.write(f'Created {len(categories)} categories and {len(locations)} locations')

    def create_users(self, num_users):
        """Create fake users with realistic data"""
        users = []
        departments = [
            'Computer Science', 'Engineering', 'Business Administration',
            'Arts and Humanities', 'Sciences', 'Education', 'Medicine',
            'Law', 'Social Sciences', 'Agriculture'
        ]
        
        # Create staff users (20% of total)
        num_staff = int(num_users * 0.2)
        num_students = num_users - num_staff
        
        # Create staff users
        for i in range(num_staff):
            user = User.objects.create_user(
                username=f'staff_{i+1:03d}',
                email=f'staff{i+1}@university.edu',
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                department=random.choice(departments),
                role='staff',
                is_staff=True,
                date_joined=fake.date_time_between(
                    start_date='2020-01-01',
                    end_date='2024-12-31'
                )
            )
            users.append(user)
        
        # Create student users
        for i in range(num_students):
            user = User.objects.create_user(
                username=f'student_{i+1:03d}',
                email=f'student{i+1}@university.edu',
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                student_id=f'202{random.randint(0,4)}{random.randint(1000,9999)}',
                department=random.choice(departments),
                role='student',
                date_joined=fake.date_time_between(
                    start_date='2020-01-01',
                    end_date='2024-12-31'
                )
            )
            users.append(user)
        
        self.stdout.write(f'Created {len(users)} users ({num_staff} staff, {num_students} students)')
        return users

    def create_reports(self, users, num_reports):
        """Create fake item reports with realistic patterns"""
        reports = []
        categories = list(Category.objects.all())
        locations = list(Location.objects.all())
        
        # Define item templates for each category
        item_templates = {
            'Electronics': [
                'Laptop', 'Smartphone', 'Tablet', 'Calculator', 'Headphones',
                'Charger', 'USB Drive', 'Mouse', 'Keyboard', 'Camera'
            ],
            'Documents': [
                'Student ID', 'Driver License', 'Passport', 'Credit Card',
                'Library Card', 'Transcript', 'Certificate', 'Notebook',
                'Textbook', 'Assignment Paper'
            ],
            'Accessories': [
                'Keys', 'Wallet', 'Watch', 'Sunglasses', 'Backpack',
                'Water Bottle', 'Umbrella', 'Gloves', 'Scarf', 'Hat'
            ],
            'Clothing': [
                'Jacket', 'Sweater', 'Shirt', 'Pants', 'Shoes',
                'Socks', 'Gloves', 'Scarf', 'Hat', 'Belt'
            ],
            'Books': [
                'Textbook', 'Novel', 'Notebook', 'Journal', 'Magazine',
                'Dictionary', 'Encyclopedia', 'Workbook', 'Manual', 'Guide'
            ],
            'Jewelry': [
                'Ring', 'Necklace', 'Earrings', 'Bracelet', 'Watch',
                'Brooch', 'Anklet', 'Cufflinks', 'Tie Clip', 'Chain'
            ],
            'Sports Equipment': [
                'Basketball', 'Soccer Ball', 'Tennis Racket', 'Gym Bag',
                'Water Bottle', 'Towel', 'Shoes', 'Jersey', 'Cap', 'Gloves'
            ],
            'Musical Instruments': [
                'Guitar', 'Violin', 'Flute', 'Clarinet', 'Trumpet',
                'Drum Sticks', 'Music Stand', 'Case', 'Metronome', 'Tuner'
            ],
            'Tools': [
                'Screwdriver', 'Wrench', 'Hammer', 'Pliers', 'Tape Measure',
                'Level', 'Drill', 'Saw', 'Chisel', 'File'
            ],
            'Personal Care': [
                'Toothbrush', 'Toothpaste', 'Soap', 'Shampoo', 'Deodorant',
                'Hairbrush', 'Mirror', 'Towel', 'Razor', 'Lotion'
            ],
            'Food & Beverages': [
                'Lunch Box', 'Thermos', 'Coffee Mug', 'Water Bottle',
                'Snack Container', 'Utensils', 'Napkins', 'Condiments'
            ],
            'Art Supplies': [
                'Paint Brushes', 'Canvas', 'Paints', 'Sketchbook',
                'Pencils', 'Markers', 'Eraser', 'Ruler', 'Palette'
            ]
        }
        
        # Generate reports with realistic patterns
        for i in range(num_reports):
            # Select random category and get appropriate items
            category = random.choice(categories)
            category_items = item_templates.get(category.name, ['Item'])
            item_name = random.choice(category_items)
            
            # Generate realistic date (more reports during academic year)
            report_date = self.generate_realistic_date()
            
            # Select status with realistic distribution
            status_weights = {'lost': 0.6, 'found': 0.35, 'claimed': 0.05}
            status = random.choices(
                list(status_weights.keys()),
                weights=list(status_weights.values())
            )[0]
            
            # Select location with some bias towards common areas
            location_weights = [1] * len(locations)
            common_locations = ['Library', 'Cafeteria', 'Student Center', 'Classroom A101']
            for loc in common_locations:
                try:
                    idx = [l.name for l in locations].index(loc)
                    location_weights[idx] = 2  # Higher weight for common locations
                except ValueError:
                    pass
            
            location = random.choices(locations, weights=location_weights)[0]
            
            # Create the report
            report = ItemReport.objects.create(
                title=f"{'Lost' if status == 'lost' else 'Found'} {item_name}",
                description=fake.text(max_nb_chars=200),
                category=category,
                location=location,
                date_lost_or_found=report_date,
                time_lost_or_found=fake.time(),
                status=status,
                reporter=random.choice(users),
                timestamp_reported=fake.date_time_between(
                    start_date=report_date,
                    end_date=report_date + timedelta(days=7)
                )
            )
            reports.append(report)
        
        self.stdout.write(f'Created {len(reports)} item reports')
        return reports

    def generate_realistic_date(self):
        """Generate dates with realistic academic patterns"""
        # Academic year pattern: more activity during semesters
        year = random.randint(2020, 2024)
        
        # Define academic periods (higher probability during these times)
        academic_periods = [
            # Spring semester
            (f'{year}-01-15', f'{year}-05-15', 0.4),
            # Fall semester  
            (f'{year}-08-15', f'{year}-12-15', 0.4),
            # Summer break
            (f'{year}-05-16', f'{year}-08-14', 0.2),
        ]
        
        # Select period based on weights
        periods = [p[0:2] for p in academic_periods]
        weights = [p[2] for p in academic_periods]
        selected_period = random.choices(periods, weights=weights)[0]
        
        start_date = datetime.strptime(selected_period[0], '%Y-%m-%d').date()
        end_date = datetime.strptime(selected_period[1], '%Y-%m-%d').date()
        
        # Generate random date within the period
        days_between = (end_date - start_date).days
        random_days = random.randint(0, days_between)
        return start_date + timedelta(days=random_days)

    def create_claims(self, users, reports, num_claims):
        """Create fake claim requests"""
        # Only found items can be claimed
        found_reports = [r for r in reports if r.status == 'found']
        
        if len(found_reports) < num_claims:
            self.stdout.write(
                self.style.WARNING(
                    f'Only {len(found_reports)} found reports available, '
                    f'creating {len(found_reports)} claims instead of {num_claims}'
                )
            )
            num_claims = len(found_reports)
        
        claims_created = 0
        for i in range(num_claims):
            report = random.choice(found_reports)
            found_reports.remove(report)  # Remove to avoid duplicate claims
            
            # Create claim
            claim = ClaimRequest.objects.create(
                item=report,
                claimer=random.choice(users),
                reason=fake.text(max_nb_chars=300),
                is_verified=random.choice([True, False]),
                verified_by=random.choice([u for u in users if u.role == 'staff']) if random.choice([True, False]) else None,
                submitted_at=fake.date_time_between(
                    start_date=report.timestamp_reported,
                    end_date=report.timestamp_reported + timedelta(days=30)
                ),
                verified_at=fake.date_time_between(
                    start_date=report.timestamp_reported,
                    end_date=report.timestamp_reported + timedelta(days=60)
                ) if random.choice([True, False]) else None
            )
            
            # Update report status if claim is verified
            if claim.is_verified:
                report.status = 'claimed'
                report.save()
            
            claims_created += 1
        
        self.stdout.write(f'Created {claims_created} claim requests') 