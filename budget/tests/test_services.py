from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from budget.models import Category, Expense
from budget.services import check_budget, monthly_total, BudgetExceeded

User = get_user_model()

class BudgetServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='ali', password='pass12345')
        self.category = Category.objects.create(user=self.user, name='Food', budget=Decimal('500'))

    def test_monthly_total_empty(self):
        total = monthly_total(self.user, self.category, 2026, 11)
        self.assertEqual(total, Decimal('0'))

    def test_monthly_total_sums_only_that_month(self):
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('100'),
            date=date(2026, 11, 1)
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('50'),
            date=date(2026, 11, 15)
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('999'),
            date=date(2026, 10, 1)
        )

        total = monthly_total(self.user, self.category, 2026, 11)
        self.assertEqual(total, Decimal('150'))

    def test_check_budget_allows_under_budget(self):
        check_budget(self.user, self.category, Decimal('100'), date(2026, 11, 1))

    def test_check_budget_allows_exact_budget(self):
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('400'),
            date=date(2026, 11, 1)
        )
        check_budget(self.user, self.category, Decimal('100'), date(2026, 11, 1))

    def test_check_budget_rejects_over_budget(self):
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('400'),
            date=date(2026, 11, 1)
        )

        with self.assertRaises(BudgetExceeded):
            check_budget(self.user, self.category, Decimal('150'), date(2026, 11, 15))

    def test_check_budget_excludes_the_expense_being_updated(self):
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('400'),
            date=date(2026, 11, 1)
            )
        
        check_budget(self.user, self.category,
            Decimal('450'),
            date(2026, 11, 1),
            exclude_expense_id=expense.id
            )
