from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a staff user with proper password hashing'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True, help='Email for the staff user')
        parser.add_argument('--username', type=str, required=True, help='Username for the staff user')
        parser.add_argument('--password', type=str, required=True, help='Password for the staff user')
        parser.add_argument('--first-name', type=str, default='', help='First name (optional)')
        parser.add_argument('--last-name', type=str, default='', help='Last name (optional)')

    def handle(self, *args, **options):
        email = options['email']
        username = options['username']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            self.stdout.write(f'User with email {email} already exists.')
            
            # Update the user to be staff and set password properly
            user.role = 'staff'
            user.is_active = True
            user.set_password(password)  # This properly hashes the password
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated existing user {username} to staff role with new password.')
            )
        else:
            # Create new staff user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,  # This properly hashes the password
                first_name=first_name,
                last_name=last_name,
                role='staff',
                is_active=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created staff user {username} with email {email}.')
            )

        self.stdout.write(
            self.style.WARNING(f'Staff login credentials:\nEmail: {email}\nPassword: {password}')
        ) 