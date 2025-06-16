from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as auth_login

User = get_user_model()

class Command(BaseCommand):
    help = 'Check users in database and test authentication'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Users in Database ==='))
        
        users = User.objects.all()
        for user in users:
            self.stdout.write(
                f'Username: {user.username} | Email: {user.email} | Role: {user.role} | Active: {user.is_active}'
            )
        
        self.stdout.write(self.style.SUCCESS('\n=== Testing Authentication ==='))
        
        # Test authentication for each user
        test_credentials = [
            ('admin@gmail.com', 'admin123'),
            ('try@gmail.com', 'trial123'),
            ('diaz@gmail.com', 'emil123'),
            ('try2@gmail.com', 'trial234'),
        ]
        
        for email, password in test_credentials:
            user = authenticate(username=email, password=password)
            if user:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Authentication successful for {email}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'✗ Authentication failed for {email}')
                ) 