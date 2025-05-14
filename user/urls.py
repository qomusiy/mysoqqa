from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('dashboard/', dashboard, name="dashboard"),
    path('statistics/', statistics, name="statistics"),
    path('calendar/', calendar, name="calendar"),
    path('history/', history, name="history"),
    path('settings/', settingss, name="settings"),
    path('password/reset/', password_reset, name="password_reset"),
    path('add_income/', add_income, name="add_income"),
    path('add_expense/', add_expense, name="add_expense"),
    path('update_income/<int:income_id>/', update_income, name="update_income"),
    path('delete_income/<int:income_id>/', delete_income, name="delete_income"),
    path('update_expense/<int:expense_id>/', update_expense, name="update_expense"),
    path('delete_expense/<int:expense_id>/', delete_expense, name="delete_expense"),
]