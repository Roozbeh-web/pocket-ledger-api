from django.contrib import admin
from .models import Category, Expense

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at')
    list_filter = ('user', 'name')
    search_fields = ('user', 'name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'category', 'date')
    list_filter = ('user', 'name', 'category')
    search_fields = ('user', 'name', 'category',)