from django.shortcuts import render
from .models import Fournisseur, ContactFournisseur

# ===============================
# FOURNISSEURS
# ===============================

def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseurs/liste_fournisseurs.html', {'fournisseurs': fournisseurs})


def detail_fournisseur(request, slug):
    fournisseur = Fournisseur.objects.get(slug=slug)
    return render(request, 'fournisseurs/detail_fournisseur.html', {'fournisseur': fournisseur})


def ajouter_fournisseur(request):
    return render(request, 'fournisseurs/ajouter_fournisseur.html')


def modifier_fournisseur(request, slug):
    fournisseur = Fournisseur.objects.get(slug=slug)
    return render(request, 'fournisseurs/modifier_fournisseur.html', {'fournisseur': fournisseur})


def supprimer_fournisseur(request, slug):
    fournisseur = Fournisseur.objects.get(slug=slug)
    return render(request, 'fournisseurs/supprimer_fournisseur.html', {'fournisseur': fournisseur})


# ===============================
# CONTACTS FOURNISSEURS
# ===============================

def liste_contacts(request, slug):
    fournisseur = Fournisseur.objects.get(slug=slug)
    contacts = ContactFournisseur.objects.filter(fournisseur=fournisseur)
    return render(request, 'fournisseurs/liste_contacts.html', {'fournisseur': fournisseur, 'contacts': contacts})


def ajouter_contact(request, slug):
    fournisseur = Fournisseur.objects.get(slug=slug)
    return render(request, 'fournisseurs/ajouter_contact.html', {'fournisseur': fournisseur})


def modifier_contact(request, pk):
    contact = ContactFournisseur.objects.get(pk=pk)
    return render(request, 'fournisseurs/modifier_contact.html', {'contact': contact})


def supprimer_contact(request, pk):
    contact = ContactFournisseur.objects.get(pk=pk)
    return render(request, 'fournisseurs/supprimer_contact.html', {'contact': contact})
