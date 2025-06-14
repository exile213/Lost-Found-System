from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Fix password for an existing staff user'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True, help='Email of the staff user')
        parser.add_argument('--password', type=str, required=True, help='New password for the staff user')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']

        try:
            user = User.objects.get(email=email)
            
            if user.role != 'staff':
                self.stdout.write(
                    self.style.ERROR(f'User {email} is not a staff user. Current role: {user.role}')
                )
                return
            
            # Set the password properly (this will hash it)
            user.set_password(password)
            user.is_active = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated password for staff user {email}.')
            )
            self.stdout.write(
                self.style.WARNING(f'New login credentials:\nEmail: {email}\nPassword: {password}')
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'No user found with email {email}.')
            ) 