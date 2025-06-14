from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Fix all users with unhashed passwords'

    def add_arguments(self, parser):
        parser.add_argument('--password', type=str, default='changeme123', 
                          help='Default password to set for users with unhashed passwords')

    def handle(self, *args, **options):
        default_password = options['password']
        
        # Find all users with unhashed passwords
        users_with_unhashed_passwords = []
        
        for user in User.objects.all():
            if not user.password.startswith('pbkdf2_sha256$'):
                users_with_unhashed_passwords.append(user)
        
        if not users_with_unhashed_passwords:
            self.stdout.write(
                self.style.SUCCESS('All passwords are properly hashed!')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f'Found {len(users_with_unhashed_passwords)} user(s) with unhashed passwords:')
        )
        
        for user in users_with_unhashed_passwords:
            self.stdout.write(f'  - {user.email} (current password: {user.password[:20]}...)')
        
        # Ask for confirmation
        response = input(f'\nDo you want to fix these passwords? (y/N): ')
        if response.lower() != 'y':
            self.stdout.write('Operation cancelled.')
            return
        
        # Fix the passwords
        fixed_count = 0
        for user in users_with_unhashed_passwords:
            user.set_password(default_password)
            user.save()
            fixed_count += 1
            self.stdout.write(f'Fixed password for {user.email}')
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully fixed {fixed_count} user(s).')
        )
        self.stdout.write(
            self.style.WARNING(f'All fixed users now have password: {default_password}')
        )
        self.stdout.write(
            self.style.WARNING('Please ask users to change their passwords after logging in.')
        ) 