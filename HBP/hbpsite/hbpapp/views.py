from django.shortcuts import render
from django.views import generic

from .models import Transactions

class TransactionsListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Transactions
    paginate_by = 10
