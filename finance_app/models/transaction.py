from django.conf import settings
from django.db import models

class Transaction(models.Model):

    choices = (
        ('expense', 'Expense'),
        ('income', 'Income')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions', null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('finance_app.category', on_delete=models.RESTRICT, related_name='transactions')
    transaction_type = models.CharField(max_length=7, choices=choices)

    def __str__(self):
        return self.transaction_type

