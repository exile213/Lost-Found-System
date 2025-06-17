from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed users from the existing database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed users...'))
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@gmail.com',
                'first_name': '',
                'last_name': '',
                'phone_number': None,
                'student_id': None,
                'role': 'student',
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
            }
        )
        
        if created:
            admin_user.set_password('admin123')  # You should change this password
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin user already exists: {admin_user.username}'))

        # Create trial user (student)
        trial_user, created = User.objects.get_or_create(
            username='trial',
            defaults={
                'email': 'try@gmail.com',
                'first_name': 'try name',
                'last_name': 'try name',
                'phone_number': '0996969439',
                'student_id': '20220548',
                'role': 'student',
                'is_superuser': False,
                'is_staff': False,
                'is_active': True,
            }
        )
        
        if created:
            trial_user.set_password('trial123')  # You should change this password
            trial_user.save()
            
            # Add profile picture if it exists
            profile_pic_path = 'profile_pics/yotsuba.png'
            if os.path.exists(f'media/{profile_pic_path}'):
                with open(f'media/{profile_pic_path}', 'rb') as f:
                    trial_user.profile_picture.save(
                        'yotsuba.png',
                        ContentFile(f.read()),
                        save=True
                    )
            
            self.stdout.write(self.style.SUCCESS(f'Created trial user: {trial_user.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Trial user already exists: {trial_user.username}'))

        # Create emil123 user (staff)
        emil_user, created = User.objects.get_or_create(
            username='emil123',
            defaults={
                'email': 'diaz@gmail.com',
                'first_name': 'Emil Joaquin',
                'last_name': 'Diaz',
                'phone_number': '09695282766',
                'student_id': '20220583',
                'role': 'staff',
                'is_superuser': False,
                'is_staff': True,
                'is_active': True,
            }
        )
        
        if created:
            emil_user.set_password('emil123')  # You should change this password
            emil_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created emil123 user: {emil_user.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Emil123 user already exists: {emil_user.username}'))

        # Create trial234 user (student)
        trial234_user, created = User.objects.get_or_create(
            username='trial234',
            defaults={
                'email': 'try2@gmail.com',
                'first_name': 'try',
                'last_name': 'student 2',
                'phone_number': '09540853945',
                'student_id': '2022052',
                'role': 'student',
                'is_superuser': False,
                'is_staff': False,
                'is_active': True,
            }
        )
        
        if created:
            trial234_user.set_password('trial234')  # You should change this password
            trial234_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created trial234 user: {trial234_user.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Trial234 user already exists: {trial234_user.username}'))

        self.stdout.write(self.style.SUCCESS('User seeding completed!'))
        self.stdout.write(self.style.SUCCESS('Default passwords:'))
        self.stdout.write(self.style.SUCCESS('- admin: admin123'))
        self.stdout.write(self.style.SUCCESS('- trial: trial123'))
        self.stdout.write(self.style.SUCCESS('- emil123: emil123'))
        self.stdout.write(self.style.SUCCESS('- trial234: trial234'))
        self.stdout.write(self.style.WARNING('Please change these passwords after first login!')) 