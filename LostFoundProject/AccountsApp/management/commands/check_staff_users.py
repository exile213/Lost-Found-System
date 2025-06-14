from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Check and debug staff users'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Check specific user by email')

    def handle(self, *args, **options):
        email = options.get('email')
        
        if email:
            # Check specific user
            try:
                user = User.objects.get(email=email)
                self.display_user_info(user)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'No user found with email: {email}')
                )
        else:
            # List all staff users
            staff_users = User.objects.filter(role='staff')
            
            if staff_users.exists():
                self.stdout.write(
                    self.style.SUCCESS(f'Found {staff_users.count()} staff user(s):')
                )
                for user in staff_users:
                    self.display_user_info(user)
            else:
                self.stdout.write(
                    self.style.WARNING('No staff users found in the database.')
                )
                
            # Also check users with Django's built-in is_staff
            django_staff_users = User.objects.filter(is_staff=True)
            if django_staff_users.exists():
                self.stdout.write(
                    self.style.WARNING(f'\nFound {django_staff_users.count()} user(s) with Django is_staff=True:')
                )
                for user in django_staff_users:
                    self.stdout.write(f'  - {user.email} (role: {getattr(user, "role", "None")})')

    def display_user_info(self, user):
        self.stdout.write(f'\nUser: {user.email}')
        self.stdout.write(f'  Username: {user.username}')
        self.stdout.write(f'  Full Name: {user.get_full_name() or "Not set"}')
        self.stdout.write(f'  Custom Role: {getattr(user, "role", "None")}')
        self.stdout.write(f'  Django is_staff: {user.is_staff}')
        self.stdout.write(f'  Django is_superuser: {user.is_superuser}')
        self.stdout.write(f'  Is Active: {user.is_active}')
        self.stdout.write(f'  Date Joined: {user.date_joined}')
        
        # Check if password is properly hashed
        if user.password.startswith('pbkdf2_sha256$'):
            self.stdout.write(f'  Password: Properly hashed')
        else:
            self.stdout.write(
                self.style.ERROR(f'  Password: NOT properly hashed (starts with: {user.password[:20]}...)')
            ) 