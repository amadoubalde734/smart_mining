from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Notification
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required  # Importer login_required

# Vue pour afficher les notifications de l'utilisateur connecté
@login_required
def notification_view(request):
    # Récupérer toutes les notifications non lues de l'utilisateur connecté
    unread_notifications = Notification.objects.filter(user=request.user, read=False).order_by('-timestamp')

    # Vérifier si nous avons des notifications non lues
    print(f"Nombre de notifications non lues : {unread_notifications.count()}")

    # Récupérer toutes les notifications de l'utilisateur pour la pagination
    all_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')

    # Pagination des notifications (par exemple 10 par page)
    paginator = Paginator(all_notifications, 10)  # Affiche 10 notifications par page
    page_number = request.GET.get('page')  # Récupérer le numéro de la page depuis l'URL
    page_obj = paginator.get_page(page_number)

    # Passer les notifications non lues et paginées au template
    return render(request, 'backend/notifications/notification_list.html', {
        'page_obj': page_obj,
        'unread_notifications': unread_notifications
    })


# Vue pour effacer toutes les notifications non lues
@login_required
def clear_all(request):
    # Assurez-vous que l'utilisateur est connecté
    if request.user.is_authenticated:
        # Effacer toutes les notifications non lues de l'utilisateur
        Notification.objects.filter(user=request.user, read=False).delete()

    # Rediriger vers la liste des notifications
    return redirect('notifications:notification_list')


# Vue pour marquer une notification comme lue
def mark_as_read(request, notification_id):
    # Récupérer la notification par son ID
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    
    # Marquer comme lue
    notification.read = True
    notification.save()

    # Rediriger vers la liste des notifications
    return redirect('notifications:notification_list')
