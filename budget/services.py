from decimal import Decimal
from django.db.models import Sum

from .models import Expense

class BudgetExceeded(Exception):
    """Raised when an expanse would push a category over its monthly budget."""
    pass

def monthly_total(user, category, year, month, exclude_expance_id=None):
    qs = Expense.objects.filter(
        user=user,
        category=category,
        date__year=year,
        date__month=month,
    )
    if exclude_expance_id is not None:
        qs = qs.exclude(id=exclude_expance_id)

    result = qs.aggregate(total=Sum('amount'))['total']
    return result or Decimal('0')

def check_budget(user, category, amount, expense_date, exclude_expense_id=None):
    current = monthly_total(
        user=user,
        category=category,
        year=expense_date.year,
        month=expense_date.month,
        exclude_expance_id=exclude_expense_id,
    )
    if current + amount > category.budget:
        remaining = category.budget - current
        raise BudgetExceeded(
            f"This expense would exceed the budget for '{category.name}'. "
            f"Remaining: {remaining}, requested: {amount}."
        )
