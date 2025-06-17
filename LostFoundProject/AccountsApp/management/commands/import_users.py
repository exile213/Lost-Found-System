import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Imports user data from a specified Excel file (e.g., users_lost_only.xlsx)'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='The Excel file path relative to the Django project root (LostFoundProject).', required=True)

    def handle(self, *args, **options):
        file_name = options['file']
        file_path = os.path.join(os.getcwd(), file_name)

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found at: {file_path}'))
            return

        try:
            df = pd.read_excel(file_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully read {len(df)} rows from {file_name}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading Excel file: {e}'))
            return

        for index, row in df.iterrows():
            email = row.get('email')
            first_name = row.get('first_name')
            last_name = row.get('last_name')
            phone_number = row.get('phone_num') # Using 'phone_num' as per your Excel
            date_joined_excel = row.get('date_joined')
            is_active = row.get('is_active', True)
            is_staff = row.get('is_staff', False)
            is_superuser = row.get('is_superuser', False)

            if not email:
                self.stdout.write(self.style.WARNING(f'Skipping row {index + 1}: Email is missing.'))
                continue

            try:
                # Convert boolean strings to actual booleans
                is_active = str(is_active).upper() == 'TRUE'
                is_staff = str(is_staff).upper() == 'TRUE'
                is_superuser = str(is_superuser).upper() == 'TRUE'

                # Convert date_joined to a timezone-aware datetime object
                if pd.isna(date_joined_excel):
                    date_joined = timezone.now()
                else:
                    date_joined = timezone.make_aware(pd.to_datetime(date_joined_excel))

                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'first_name': first_name if pd.notna(first_name) else '',
                        'last_name': last_name if pd.notna(last_name) else '',
                        'phone_number': phone_number if pd.notna(phone_number) else '',
                        'date_joined': date_joined,
                        'is_active': is_active,
                        'is_staff': is_staff,
                        'is_superuser': is_superuser,
                        'username': email, # Set username to email if it's not provided by the model directly
                    }
                )
                
                if created:
                    user.set_unusable_password() # Set an unusable password for new users
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Created new user: {email}'))
                else:
                    # Update existing user fields if needed
                    # Note: We are not updating password here, only other fields
                    updated = False
                    if user.first_name != (first_name if pd.notna(first_name) else ''):
                        user.first_name = (first_name if pd.notna(first_name) else '')
                        updated = True
                    if user.last_name != (last_name if pd.notna(last_name) else ''):
                        user.last_name = (last_name if pd.notna(last_name) else '')
                        updated = True
                    if hasattr(user, 'phone_number') and user.phone_number != (phone_number if pd.notna(phone_number) else ''):
                        user.phone_number = (phone_number if pd.notna(phone_number) else '')
                        updated = True
                    if user.date_joined != date_joined:
                        user.date_joined = date_joined
                        updated = True
                    if user.is_active != is_active:
                        user.is_active = is_active
                        updated = True
                    if user.is_staff != is_staff:
                        user.is_staff = is_staff
                        updated = True
                    if user.is_superuser != is_superuser:
                        user.is_superuser = is_superuser
                        updated = True

                    if updated:
                        user.save()
                        self.stdout.write(self.style.INFO(f'Updated existing user: {email}'))
                    else:
                        self.stdout.write(self.style.NOTICE(f'User already exists and no updates needed: {email}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing row {index + 1} ({email}): {e}'))

        self.stdout.write(self.style.SUCCESS('User import complete.')) 