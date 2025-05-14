from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        print(f"Creating superuser with email: {email}, extra_fields: {extra_fields}")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', 'Admin')  # Default for required field
        extra_fields.setdefault('preferred_language', 'en')  # Default for required field

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    worth = models.FloatField(default=1.0)  # Exchange rate relative to USD

    def __str__(self):
        return f"{self.name} ({self.code})"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    preferred_language = models.CharField(
        max_length=2,
        choices=(('en', 'English'), ('uz', 'Uzbek'), ('ru', 'Russian')),
        default='en'
    )
    preferred_currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    username = None

class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.email} - {self.code}"


class Income(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='incomes')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    income_datetime = models.DateTimeField(default=timezone.now)
    created_datetime = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    category = models.CharField(
        max_length=20,
        choices=[
            ('salary', 'Salary'),
            ('bonus', 'Bonus'),
            ('other', 'Other')
        ],
        default='other'
    )
    account = models.CharField(
        max_length=10,
        choices=[
            ('cash', 'Cash'),
            ('card', 'Card')
        ],
        default='cash'
    )

    def __str__(self):
        return f"{self.user.email} - {self.category} - {self.amount} {self.currency.code}"

class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    expense_datetime = models.DateTimeField(default=timezone.now)
    created_datetime = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    category = models.CharField(
        max_length=20,
        choices=[
            ('food', 'Food'),
            ('social_life', 'Social Life'),
            ('transport', 'Transport'),
            ('household', 'Household'),
            ('health', 'Health'),
            ('education', 'Education'),
            ('apparel', 'Apparel'),
            ('gift', 'Gift'),
            ('beauty', 'Beauty'),
            ('other', 'Other')
        ],
        default='other'
    )
    account = models.CharField(
        max_length=10,
        choices=[
            ('cash', 'Cash'),
            ('card', 'Card')
        ],
        default='cash'
    )

    def __str__(self):
        return f"{self.user.email} - {self.category} - {self.amount} {self.currency.code}"