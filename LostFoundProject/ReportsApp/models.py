from django.db import models
from AccountsApp.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

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
    # Old fields (to be removed after data migration)
    category_old = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', null=True, blank=True)
    location_old = models.CharField(max_length=100, null=True, blank=True)
    # New ForeignKey fields
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    date_lost_or_found = models.DateField()
    time_lost_or_found = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    timestamp_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status}) - {self.location.name if self.location else self.location_old}"
