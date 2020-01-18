from django.urls import path
from . import views


urlpatterns = [
    path('Transactions/', views.TransactionsListView.as_view(), name='transactions'),
]
