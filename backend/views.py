from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# parametrage_global/views.py
from django.shortcuts import redirect
@login_required
def dashboard(request):
    # Si admin, on reste sur le dashboard principal
    return render(request, 'backend/index.html')
