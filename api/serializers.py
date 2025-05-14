from rest_framework import serializers
from user.models import Income, Expense, CustomUser, Currency
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name']

class IncomeSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), source='currency', write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Income
        fields = ['id', 'user', 'amount', 'currency', 'currency_id', 'income_datetime', 'note', 'category', 'account']
        read_only_fields = ['user']

class ExpenseSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), source='currency', write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'currency', 'currency_id', 'expense_datetime', 'note', 'category', 'account']
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    preferred_currency = CurrencySerializer(read_only=True)
    preferred_currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), source='preferred_currency', write_only=True, allow_null=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'preferred_language', 'preferred_currency', 'preferred_currency_id']
        read_only_fields = ['email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    preferred_currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), source='preferred_currency', required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'preferred_language', 'preferred_currency_id']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name'),
            preferred_language=validated_data.get('preferred_language', 'en'),
            preferred_currency=validated_data.get('preferred_currency')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class AdminRegisterSerializer(RegisterSerializer):
    secret_key = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'preferred_language', 'preferred_currency_id', 'secret_key']

    def validate_secret_key(self, value):
        if value != "mysoqqa_admin_secret":  # Replace with a secure key in production
            raise serializers.ValidationError("Invalid secret key.")
        return value

    def create(self, validated_data):
        validated_data.pop('secret_key')  # Remove secret_key before creating user
        user = super().create(validated_data)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        data['user'] = user
        return data