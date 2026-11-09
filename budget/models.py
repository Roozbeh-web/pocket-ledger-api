from django.conf import settings
from django.db import models

class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
    )
    name = models.CharField(max_length=255, unique=True)
    budget = models.DecimalField(max_digits=20, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"username: {self.user.username} /n cat-name: {self.name} /n budget: {self.budget} /n created-at: {self.created_at}"

class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='expenses',
    )
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=0)
    note = models.TextField(blank=True)
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.amount} - {self.category.name} ({self.date})"    