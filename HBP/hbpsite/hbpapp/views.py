from django.shortcuts import render
from django.views import generic

from .models import Transactions, CCY, Category

class TransactionsListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Transactions
    paginate_by = 10


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_trans = Transactions.objects.all().count()
    num_ccys = CCY.objects.all().count()
    num_categories = Category.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_trans': num_trans, 'num_ccys': num_ccys,
                 'num_categories': num_categories, 'num_visits': num_visits},
    )

