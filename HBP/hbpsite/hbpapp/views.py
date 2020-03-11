from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Transactions, CCY, Category, Document

# own function to handle an uploaded file
from .xlsx_parser import parse
from .forms import UploadFileForm


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


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            parse(newdoc.docfile.name)
            return HttpResponseRedirect(reverse('upload_file'))
    else:
        form = UploadFileForm() # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    return render(request, 'upload.html', {'documents': documents, 'form': form})
    

def file_view(request, pk):
    item = Document.objects.get(pk=pk)
    
    #return render(request, 'file_view.html', {'item': item, 'form': form})
    return render(request, 'file_view.html', {'item': item})