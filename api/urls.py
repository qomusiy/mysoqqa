from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncomeViewSet, ExpenseViewSet, UserViewSet, CurrencyViewSet, register_user, register_admin, obtain_token

router = DefaultRouter()
router.register(r'incomes', IncomeViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'users', UserViewSet)
router.register(r'currencies', CurrencyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_token, name='api_token'),
    path('register/', register_user, name='api_register'),
    path('register-admin/', register_admin, name='api_register_admin'),
]