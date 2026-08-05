from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import BonCommande, BonCommandeLigne, BonLivraison, BonLivraisonLigne
from .forms import BonCommandeForm, BonCommandeLigneForm, BonLivraisonForm, BonLivraisonLigneForm

# ===============================
# Bons de Commande
# ===============================
def liste_bons_commandes(request):
    commandes = BonCommande.objects.all()
    return render(request, 'commercial/liste_bons_commandes.html', {'commandes': commandes})

def creer_bon_commande(request):
    if request.method == 'POST':
        form = BonCommandeForm(request.POST)
        if form.is_valid():
            bon = form.save(commit=False)
            bon.created_by = request.user
            bon.save()
            return redirect('commercial:liste_bons_commandes')
    else:
        form = BonCommandeForm()
    return render(request, 'commercial/bon_commande_form.html', {'form': form})

def modifier_bon_commande(request, slug):
    bon = get_object_or_404(BonCommande, slug=slug)
    if request.method == 'POST':
        form = BonCommandeForm(request.POST, instance=bon)
        if form.is_valid():
            form.save()
            return redirect('commercial:liste_bons_commandes')
    else:
        form = BonCommandeForm(instance=bon)
    return render(request, 'commercial/bon_commande_form.html', {'form': form, 'bon': bon})

# ===============================
# Bons de Livraison
# ===============================
def liste_bons_livraison(request):
    livraisons = BonLivraison.objects.all()
    return render(request, 'commercial/liste_bons_livraison.html', {'livraisons': livraisons})

def creer_bon_livraison(request):
    if request.method == 'POST':
        form = BonLivraisonForm(request.POST)
        if form.is_valid():
            bl = form.save(commit=False)
            bl.created_by = request.user
            bl.save()
            return redirect('commercial:liste_bons_livraison')
    else:
        form = BonLivraisonForm()
    return render(request, 'commercial/bon_livraison_form.html', {'form': form})
