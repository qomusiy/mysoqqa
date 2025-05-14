from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import VerificationCode, Currency, CustomUser, Income, Expense
from django.utils import timezone
from datetime import timedelta
import secrets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, date
from django.db.models import Value, CharField, F, Sum
from django.db.models.functions import Coalesce
from django.db.models.fields import DecimalField
from decimal import Decimal
import calendar as cal_module
from django.contrib.auth.hashers import check_password

def index(request):
    return render(request, 'index.html')

def signup(request):
    currencies = Currency.objects.all()
    if request.method == 'POST':
        step = request.POST.get('step')

        if step == 'email':
            email = request.POST.get('email')
            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error': 'Email already registered', 'step': 'email'})
            
            code = str(secrets.randbelow(1000000)).zfill(6)
            expires_at = timezone.now() + timedelta(minutes=10)
            
            VerificationCode.objects.create(email=email, code=code, expires_at=expires_at)
            print(f'THE CODE sent to {email} is {code}')
            send_mail(
                'MySoqqa Verification Code',
                f'Your verification code is: {code} author: qomusiy.onrender.com',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            return render(request, 'signup.html', {'step': 'code', 'email': email, 'currencies': currencies})

        elif step == 'code':
            email = request.POST.get('email')
            code = request.POST.get('code')
            try:
                verification = VerificationCode.objects.get(email=email, code=code, expires_at__gt=timezone.now())
                return render(request, 'signup.html', {'step': 'register', 'email': email, 'currencies': currencies})
            except VerificationCode.DoesNotExist:
                return render(request, 'signup.html', {'step': 'code', 'email': email, 'error': 'Invalid or expired code', 'currencies': currencies})

        elif step == 'register':
            email = request.POST.get('email')
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            preferred_language = request.POST.get('preferred_language')
            preferred_currency_id = request.POST.get('preferred_currency', None)
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                return render(request, 'signup.html', {
                    'step': 'register',
                    'email': email,
                    'currencies': currencies,
                    'error': 'Passwords do not match'
                })

            user = CustomUser(
                email=email,
                first_name=name,
                last_name=surname or None,
                preferred_language=preferred_language,
                preferred_currency_id=preferred_currency_id or None
            )
            user.set_password(password)
            user.save()

            VerificationCode.objects.filter(email=email).delete()

            return redirect('login')

    return render(request, 'signup.html', {'step': 'email', 'currencies': currencies})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    currencies = Currency.objects.all()
    incomes = request.user.incomes.all().order_by('-income_datetime')
    expenses = request.user.expenses.all().order_by('-expense_datetime')
    return render(request, 'dashboard.html', {
        'currencies': currencies,
        'incomes': incomes,
        'expenses': expenses
    })

@login_required
def add_income(request):
    currencies = Currency.objects.all()
    if request.method == 'POST':
        amount = request.POST.get('amount')
        currency_id = request.POST.get('currency')
        income_datetime = request.POST.get('income_datetime')
        note = request.POST.get('note')
        category = request.POST.get('category')
        account = request.POST.get('account')

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError('Amount must be positive')
            currency = Currency.objects.get(id=currency_id)
            Income.objects.create(
                user=request.user,
                amount=amount,
                currency=currency,
                income_datetime=income_datetime or timezone.now(),
                note=note,
                category=category,
                account=account
            )
            return redirect('dashboard')
        except (ValueError, Currency.DoesNotExist):
            return render(request, 'add_income.html', {
                'currencies': currencies,
                'error': 'Invalid input. Please check your data.'
            })

    return render(request, 'add_income.html', {'currencies': currencies})

@login_required
def add_expense(request):
    currencies = Currency.objects.all()
    if request.method == 'POST':
        amount = request.POST.get('amount')
        currency_id = request.POST.get('currency')
        expense_datetime = request.POST.get('expense_datetime')
        note = request.POST.get('note')
        category = request.POST.get('category')
        account = request.POST.get('account')

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError('Amount must be positive')
            currency = Currency.objects.get(id=currency_id)
            Expense.objects.create(
                user=request.user,
                amount=amount,
                currency=currency,
                expense_datetime=expense_datetime or timezone.now(),
                note=note,
                category=category,
                account=account
            )
            return redirect('dashboard')
        except (ValueError, Currency.DoesNotExist):
            return render(request, 'add_expense.html', {
                'currencies': currencies,
                'error': 'Invalid input. Please check your data.'
            })

    return render(request, 'add_expense.html', {'currencies': currencies})

def update_profile(request):
    currencies = Currency.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        preferred_language = request.POST.get('preferred_language')
        preferred_currency_id = request.POST.get('preferred_currency') or None

        user = request.user
        user.first_name = name
        user.last_name = surname or None
        user.preferred_language = preferred_language
        user.preferred_currency_id = preferred_currency_id
        user.save()

        return render(request, 'dashboard.html', {
            'currencies': currencies,
            'profile_success': 'Profile updated successfully'
        })

    return render(request, 'dashboard.html', {'currencies': currencies})

def change_password(request):
    currencies = Currency.objects.all()
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user = request.user
        if not check_password(current_password, user.password):
            return render(request, 'dashboard.html', {
                'currencies': currencies,
                'password_error': 'Current password is incorrect'
            })

        if new_password != confirm_new_password:
            return render(request, 'dashboard.html', {
                'currencies': currencies,
                'password_error': 'New passwords do not match'
            })

        user.set_password(new_password)
        user.save()
        login(request, user)  # Re-authenticate user after password change
        return render(request, 'dashboard.html', {
            'currencies': currencies,
            'password_success': 'Password changed successfully'
        })

    return render(request, 'dashboard.html', {'currencies': currencies})

def delete_account(request):
    currencies = Currency.objects.all()
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('login')

    return render(request, 'dashboard.html', {'currencies': currencies})


@login_required
def statistics(request):
    # Get user's preferred currency or default to first available
    currency = request.user.preferred_currency or Currency.objects.first()
    currency_code = currency.code if currency else 'USD'

    # Calculate total income and expenses
    total_income = request.user.incomes.aggregate(
        total=Coalesce(Sum('amount'), Decimal(0), output_field=DecimalField())
    )['total']
    total_expense = request.user.expenses.aggregate(
        total=Coalesce(Sum('amount'), Decimal(0), output_field=DecimalField())
    )['total']
    net_balance = total_income - total_expense

    # Calculate percentages for progress bar
    total = total_income + total_expense
    income_percentage = (total_income / total * 100) if total > 0 else 50.0
    expense_percentage = (total_expense / total * 100) if total > 0 else 50.0

    # Category breakdown
    income_categories = Income._meta.get_field('category').choices
    expense_categories = Expense._meta.get_field('category').choices
    category_breakdown = []

    # Income by category
    for value, label in income_categories:
        amount = request.user.incomes.filter(category=value).aggregate(
            total=Coalesce(Sum('amount'), Decimal(0), output_field=DecimalField())
        )['total']
        if amount > 0:
            category_breakdown.append({
                'category': label,
                'type': 'Income',
                'amount': amount
            })

    # Expenses by category
    for value, label in expense_categories:
        amount = request.user.expenses.filter(category=value).aggregate(
            total=Coalesce(Sum('amount'), Decimal(0), output_field=DecimalField())
        )['total']
        if amount > 0:
            category_breakdown.append({
                'category': label,
                'type': 'Expense',
                'amount': amount
            })

    return render(request, 'statistics.html', {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'currency': currency_code,
        'income_percentage': income_percentage,
        'expense_percentage': expense_percentage,
        'category_breakdown': category_breakdown
    })

@login_required
def calendar(request):
   # Get user's preferred currency or default
    currency = request.user.preferred_currency or Currency.objects.first()
    currency_code = currency.code if currency else 'USD'

    # Get year and month from query params or default to current
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))

    # Calculate calendar days
    cal = cal_module.monthcalendar(year, month)
    calendar_days = []
    for week in cal:
        for day in week:
            if day == 0:
                calendar_days.append({'number': '', 'date': None, 'transactions': []})
                continue
            day_date = date(year, month, day)
            # Fetch transactions for the day
            incomes = Income.objects.filter(user=request.user, income_datetime__date=day_date).values('amount', 'category', 'note', 'currency__code').annotate(type=Value('income', output_field=CharField()))
            expenses = Expense.objects.filter(user=request.user, expense_datetime__date=day_date).values('amount', 'category', 'note', 'currency__code').annotate(type=Value('expense', output_field=CharField()))
            transactions = list(incomes) + list(expenses)
            calendar_days.append({
                'number': day,
                'date': day_date,
                'transactions': transactions
            })

    # Calculate monthly summary
    month_start = date(year, month, 1)
    month_end = date(year, month, cal_module.monthrange(year, month)[1])
    total_income = Income.objects.filter(user=request.user, income_datetime__date__range=[month_start, month_end]).aggregate(
        total=Coalesce(Sum('amount'), Decimal(0), output_field=DecimalField())
    )['total']
    total_expense = Expense.objects.filter(user=request.user, expense_datetime__date__range=[month_start, month_end]).aggregate(
        total=Coalesce(Sum('amount'), Decimal(0), output_field=DecimalField())
    )['total']
    net_balance = total_income - total_expense

    return render(request, 'calendar.html', {
        'calendar_days': calendar_days,
        'current_month': date(year, month, 1),
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'currency_code': currency_code,
    })

@login_required
def history(request):
    # Get filter and search parameters
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    category_filter = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Base querysets
    incomes = request.user.incomes.all()
    expenses = request.user.expenses.all()

    # Apply filters to incomes
    if search_query:
        incomes = incomes.filter(note__icontains=search_query)
    if type_filter == 'income':
        expenses = expenses.none()  # Exclude expenses
    elif type_filter == 'expense':
        incomes = incomes.none()  # Exclude incomes
    if category_filter:
        incomes = incomes.filter(category=category_filter)
    if start_date:
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            incomes = incomes.filter(income_datetime__gte=start_date)
        except (ValueError, TypeError):
            pass
    if end_date:
        try:
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                end_date = end_date.replace(hour=23, minute=59, second=59)
            incomes = incomes.filter(income_datetime__lte=end_date)
        except (ValueError, TypeError):
            pass

    # Apply filters to expenses
    if search_query:
        expenses = expenses.filter(note__icontains=search_query)
    if type_filter == 'income':
        expenses = expenses.none()
    elif type_filter == 'expense':
        incomes = incomes.none()
    if category_filter:
        expenses = expenses.filter(category=category_filter)
    if start_date:
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            expenses = expenses.filter(expense_datetime__gte=start_date)
        except (ValueError, TypeError):
            pass
    if end_date:
        try:
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                end_date = end_date.replace(hour=23, minute=59, second=59)
            expenses = expenses.filter(expense_datetime__lte=end_date)
        except (ValueError, TypeError):
            pass

    # Combine querysets
    incomes = incomes.values(
        'id', 'amount', 'currency__code', 'income_datetime', 'category', 'account', 'note'
    ).annotate(
        type=Value('income', output_field=CharField()),
        datetime=F('income_datetime')
    )
    expenses = expenses.values(
        'id', 'amount', 'currency__code', 'expense_datetime', 'category', 'account', 'note'
    ).annotate(
        type=Value('expense', output_field=CharField()),
        datetime=F('expense_datetime')
    )

    # Debugging: Print querysets
    # print("Filtered Incomes:", list(incomes))
    # print("Filtered Expenses:", list(expenses))

    # Combine and sort
    transactions = incomes.union(expenses).order_by('-datetime')

    # Pagination
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get category choices
    income_categories = Income._meta.get_field('category').choices
    expense_categories = Expense._meta.get_field('category').choices

    # Debugging: Print final transactions
    # print("Final transactions:", list(page_obj))

    return render(request, 'history.html', {
        'currencies': Currency.objects.all(),
        'page_obj': page_obj,
        'search_query': search_query,
        'type_filter': type_filter,
        'category_filter': category_filter,
        'start_date': start_date,
        'end_date': end_date,
        'income_categories': income_categories,
        'expense_categories': expense_categories
    })

@login_required
def settingss(request):
    currencies = Currency.objects.all()
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            preferred_language = request.POST.get('preferred_language')
            preferred_currency_id = request.POST.get('preferred_currency') or None

            user = request.user
            user.first_name = name
            user.last_name = surname or None
            user.preferred_language = preferred_language
            user.preferred_currency_id = preferred_currency_id
            user.save()

            return render(request, 'settings.html', {
                'currencies': currencies,
                'profile_success': 'Profile updated successfully'
            })

        elif action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            user = request.user
            if not check_password(current_password, user.password):
                return render(request, 'settings.html', {
                    'currencies': currencies,
                    'password_error': 'Current password is incorrect'
                })

            if new_password != confirm_new_password:
                return render(request, 'settings.html', {
                    'currencies': currencies,
                    'password_error': 'New passwords do not match'
                })

            user.set_password(new_password)
            user.save()
            login(request, user)
            return render(request, 'settings.html', {
                'currencies': currencies,
                'password_success': 'Password changed successfully'
            })

        elif action == 'delete_account':
            user = request.user
            user.delete()
            logout(request)
            return redirect('login')

    return render(request, 'settings.html', {'currencies': currencies})

def password_reset(request):
    if request.method == 'POST':
        step = request.POST.get('step')

        if step == 'request':
            email = request.POST.get('email')
            if not CustomUser.objects.filter(email=email).exists():
                return render(request, 'pass_reset/password_reset.html', {
                    'step': 'request',
                    'error': 'Email not found'
                })

            # Delete old codes to avoid conflicts
            VerificationCode.objects.filter(email=email).delete()

            code = str(secrets.randbelow(1000000)).zfill(6)
            expires_at = timezone.now() + timedelta(minutes=10)
            
            VerificationCode.objects.create(email=email, code=code, expires_at=expires_at)
            
            try:
                send_mail(
                    'MySoqqa Password Reset Code',
                    f'Your password reset code is: {code}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                print(f"Sent code: {code} for email: {email}")
            except Exception as e:
                print(f"Email sending failed: {e}")
                return render(request, 'pass_reset/password_reset.html', {
                    'step': 'request',
                    'error': 'Failed to send email. Please try again.'
                })
            
            return render(request, 'pass_reset/password_reset.html', {
                'step': 'verify',
                'email': email
            })

        elif step == 'verify':
            email = request.POST.get('email')
            code = request.POST.get('code')
            print(f"Received email: {email}, code: {code}")
            
            try:
                verification = VerificationCode.objects.get(email=email, code=code, expires_at__gt=timezone.now())
                print("Code verified successfully")
                return render(request, 'pass_reset/password_reset.html', {
                    'step': 'confirm',
                    'email': email
                })
            except VerificationCode.DoesNotExist:
                print("Invalid or expired code")
                verification_codes = VerificationCode.objects.filter(email=email)
                for vc in verification_codes:
                    print(f"Stored code: {vc.code}, Expires: {vc.expires_at}")
                return render(request, 'pass_reset/password_reset.html', {
                    'step': 'verify',
                    'email': email,
                    'error': 'Invalid or expired code'
                })

        elif step == 'confirm':
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                return render(request, 'pass_reset/password_reset.html', {
                    'step': 'confirm',
                    'email': email,
                    'error': 'Passwords do not match'
                })

            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(password)
                user.save()
                VerificationCode.objects.filter(email=email).delete()
                print("Password reset successfully")
                return redirect('login')
            except CustomUser.DoesNotExist:
                print("User not found")
                return render(request, 'pass_reset/password_reset.html', {
                    'step': 'confirm',
                    'email': email,
                    'error': 'User not found'
                })

    return render(request, 'pass_reset/password_reset.html', {'step': 'request'})


@login_required
def update_income(request, income_id):
    income = Income.objects.get(id=income_id, user=request.user)
    currencies = Currency.objects.all()
    if request.method == 'POST':
        amount = request.POST.get('amount')
        currency_id = request.POST.get('currency')
        income_datetime = request.POST.get('income_datetime')
        note = request.POST.get('note')
        category = request.POST.get('category')
        account = request.POST.get('account')

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError('Amount must be positive')
            currency = Currency.objects.get(id=currency_id)
            income.amount = amount
            income.currency = currency
            income.income_datetime = income_datetime or timezone.now()
            income.note = note
            income.category = category
            income.account = account
            income.save()
            return redirect('dashboard')
        except (ValueError, Currency.DoesNotExist):
            return render(request, 'add_income.html', {
                'currencies': currencies,
                'error': 'Invalid input. Please check your data.',
                'income': income
            })

    return render(request, 'add_income.html', {'currencies': currencies, 'income': income})

@login_required
def delete_income(request, income_id):
    income = Income.objects.get(id=income_id, user=request.user)
    if request.method == 'POST':
        income.delete()
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def update_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)
    currencies = Currency.objects.all()
    if request.method == 'POST':
        amount = request.POST.get('amount')
        currency_id = request.POST.get('currency')
        expense_datetime = request.POST.get('expense_datetime')
        note = request.POST.get('note')
        category = request.POST.get('category')
        account = request.POST.get('account')

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError('Amount must be positive')
            currency = Currency.objects.get(id=currency_id)
            expense.amount = amount
            expense.currency = currency
            expense.expense_datetime = expense_datetime or timezone.now()
            expense.note = note
            expense.category = category
            expense.account = account
            expense.save()
            return redirect('dashboard')
        except (ValueError, Currency.DoesNotExist):
            return render(request, 'add_expense.html', {
                'currencies': currencies,
                'error': 'Invalid input. Please check your data.',
                'expense': expense
            })

    return render(request, 'add_expense.html', {'currencies': currencies, 'expense': expense})

@login_required
def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return redirect('dashboard')
