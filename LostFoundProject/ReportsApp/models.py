from django.db import models
from AccountsApp.models import User

class ItemReport(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('claimed', 'Claimed'),
    ]

    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('documents', 'Documents'),
        ('accessories', 'Accessories'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    location = models.CharField(max_length=100)
    date_lost_or_found = models.DateField()
    time_lost_or_found = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    timestamp_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status}) - {self.location}"
