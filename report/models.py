from django.db import models
from datetime import date

class Debtor(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Ism va familiyasi")
    social_link = models.TextField(blank=True, null=True, verbose_name="Ijtimoiy tarmoqdagi manzili")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon nomeri")
    address = models.TextField(blank=True, null=True, verbose_name="Manzili")

    def __str__(self):
        return self.full_name
    
class Debt(models.Model):
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, related_name="debts")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.debtor.full_name} - {self.amount} so'm"
