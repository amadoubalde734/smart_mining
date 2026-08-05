from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/dashboard/accounts/login/')
def index(request):
    return render(request, 'backend/index.html')
