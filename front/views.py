from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy

def start_plan(request):
    if not request.user.is_authenticated:
        # Redirige vers l'inscription avec redirection automatique vers /pages/demarrer/
        return redirect(f"{reverse('front_register')}?next={reverse('demarrer')}")
    return redirect('demarrer')


@login_required(login_url=reverse_lazy('accounts:front_login'))
def index(request):
    return render(request, 'front/index.html')
