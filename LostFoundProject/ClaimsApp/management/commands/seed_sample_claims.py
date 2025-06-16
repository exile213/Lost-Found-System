from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ClaimsApp.models import ClaimRequest
from ReportsApp.models import ItemReport
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed sample claim requests for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed sample claims...'))
        
        # Get users
        try:
            trial_user = User.objects.get(username='trial')
            trial234_user = User.objects.get(username='trial234')
            emil_user = User.objects.get(username='emil123')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Users not found. Please run seed_users command first.'))
            return
        
        # Get found items that can be claimed
        found_items = ItemReport.objects.filter(status='found')
        
        if not found_items.exists():
            self.stdout.write(self.style.ERROR('No found items available. Please run seed_sample_reports first.'))
            return
        
        # Sample claim data
        sample_claims = [
            {
                'item': found_items.first(),
                'claimer': trial_user,
                'reason': 'This is my laptop that I lost yesterday. I can identify it by the stickers on the lid.',
                'is_verified': False,
            },
            {
                'item': found_items.last() if found_items.count() > 1 else found_items.first(),
                'claimer': trial234_user,
                'reason': 'I lost my water bottle during my last class. It has my name written on the bottom.',
                'is_verified': False,
            },
        ]
        
        created_count = 0
        for claim_data in sample_claims:
            # Check if claim already exists
            existing_claim = ClaimRequest.objects.filter(
                item=claim_data['item'],
                claimer=claim_data['claimer']
            ).first()
            
            if not existing_claim:
                claim = ClaimRequest.objects.create(
                    item=claim_data['item'],
                    claimer=claim_data['claimer'],
                    reason=claim_data['reason'],
                    is_verified=claim_data['is_verified']
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created claim: {claim.claimer.username} claims {claim.item.title}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Claim already exists: {claim_data["claimer"].username} for {claim_data["item"].title}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Sample claims seeding completed! Created {created_count} new claims.'
            )
        )
        
        # Show current claim statistics
        total_claims = ClaimRequest.objects.count()
        pending_claims = ClaimRequest.objects.filter(is_verified=False).count()
        approved_claims = ClaimRequest.objects.filter(is_verified=True).count()
        
        self.stdout.write(self.style.SUCCESS(f'\nCurrent Claim Statistics:'))
        self.stdout.write(self.style.SUCCESS(f'- Total Claims: {total_claims}'))
        self.stdout.write(self.style.SUCCESS(f'- Pending Claims: {pending_claims}'))
        self.stdout.write(self.style.SUCCESS(f'- Approved Claims: {approved_claims}')) 