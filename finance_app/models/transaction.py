from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Transaction(models.Model):

    choices = (
        ('expense', 'Expense'),
        ('income', 'Income')
    )

    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('finance_app.category', on_delete=models.RESTRICT, related_name='transactions', null=True, blank=True)
    transaction_type = models.CharField(max_length=7, choices=choices)

    def __str__(self):
        return self.transaction_type

