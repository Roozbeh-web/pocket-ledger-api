from  rest_framework import serializers

from .models import Category, Expense
from .services import check_budget, BudgetExceeded

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'budget']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'date', 'note']
        read_only_fields = ['id']

    def validate_category(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidateError("Category not found.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            check_budget(
                user=user,
                category=validated_data['category'],
                amount=validated_data['amount'],
                expense_date=validated_data['date'],
            )
        except BudgetExceeded as e:
            raise serializers.ValidationError({'detail': str(e)})

        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        category = validated_data.get('category', instance.category)
        amount = validated_data.get('date', instance.data)
        expence_date = validated_data.get('date', instance.date)

        try:
            check_budget(
                user=user,
                category=category,
                amount=amount,
                expense_date=expence_date,
                exclude_expense_id=instance.id,
            )
        except BudgetExceeded as e:
            raise serializers.ValidationError({'detail': str(e)})

        return super().update(instance, validated_data)

    