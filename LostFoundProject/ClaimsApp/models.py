from django.db import models
from AccountsApp.models import User
from ReportsApp.models import ItemReport

class ClaimRequest(models.Model):
    item = models.ForeignKey(ItemReport, on_delete=models.CASCADE)
    claimer = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    additional_proof = models.FileField(upload_to='claim_proofs/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_claims')
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Claim by {self.claimer.username} for {self.item.title}"
