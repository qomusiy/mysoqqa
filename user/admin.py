from django.contrib import admin
from .models import CustomUser, Currency, VerificationCode, Income, Expense

admin.site.register(CustomUser)
admin.site.register(Currency)
admin.site.register(VerificationCode)
# admin.site.register(UserManager)
admin.site.register(Income)
admin.site.register(Expense)