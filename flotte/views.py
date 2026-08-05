from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .models import Flotte, SiteEngin, Engin
from .forms import FlotteForm

# ===============================
# LISTE DES FLOTTES
# ===============================
@login_required
def flotte_list(request):
    flottes = Flotte.objects.select_related("site").prefetch_related("engins")

    # Si modal soumis (POST)
    if request.method == "POST":
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        site_id = request.POST.get("site")
        actif = request.POST.get("actif") == "on"
        engins_ids = request.POST.getlist("engins[]")

        flotte = Flotte.objects.create(
            nom=nom,
            description=description,
            site=SiteEngin.objects.get(id=site_id) if site_id else None,
            actif=actif
        )

        if engins_ids:
            flotte.engins.set(engins_ids)

        messages.success(request, "Flotte ajoutée avec succès.")
        return redirect("flotte:flotte_list")

    sites = SiteEngin.objects.all()
    all_engins = Engin.objects.all()

    context = {
        "flottes": flottes,
        "total_flottes": flottes.count(),
        "active_flottes": flottes.filter(actif=True).count(),
        "inactive_flottes": flottes.filter(actif=False).count(),
        "recent_flottes": flottes.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count(),
        "sites": sites,
        "all_engins": all_engins,
    }

    return render(request, "backend/pages/flotte/flotte_list.html", context)


# ===============================
# DETAIL D'UNE FLOTTES
# ===============================
@login_required
def flotte_detail(request, slug):
    flotte = get_object_or_404(
        Flotte.objects.select_related("site").prefetch_related("engins"),
        slug=slug
    )

    return render(
        request,
        "backend/pages/flotte/flotte_detail.html",
        {
            "flotte": flotte,
            "engins": flotte.engins.all(),
        }
    )

# ===============================
# MISE À JOUR D'UNE FLOTTES
# ===============================
@login_required
def flotte_update(request, slug):
    flotte = get_object_or_404(Flotte, slug=slug)

    if request.method == "POST":
        form = FlotteForm(request.POST, instance=flotte)
        if form.is_valid():
            form.save()
            messages.success(request, "Flotte modifiée avec succès.")
            return redirect("flotte:flotte_list")
        else:
            messages.error(request, "Erreur lors de la modification de la flotte.")
    else:
        form = FlotteForm(instance=flotte)

    return render(
        request,
        "backend/pages/flotte/flotte_update.html",
        {
            "form": form,
            "flotte": flotte
        }
    )

# ===============================
# SUPPRESSION D'UNE FLOTTES
# ===============================
@login_required
def flotte_delete(request, slug):
    flotte = get_object_or_404(Flotte, slug=slug)

    if request.method == "POST":
        flotte.delete()
        messages.success(request, "Flotte supprimée avec succès.")
        return redirect("flotte:flotte_list")

    return render(
        request,
        "backend/pages/flotte/flotte_delete.html",
        {"flotte": flotte}
    )

