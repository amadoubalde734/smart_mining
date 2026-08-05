from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect

# Redirection depuis la racine vers /dashboard/
def root_redirect(request):
    return redirect('/dashboard/')

urlpatterns = [
    path('', root_redirect),
    path('portail/', include('front.urls')),
    path('dashboard/', include('backend.urls', namespace='backend')),
    path('flotte/', include('flotte.urls', namespace='flotte')),
    path('engins/', include('engins.urls', namespace='engins')),
    path('parametrage/', include('parametrage.urls', namespace='parametrage')),
    path('personnel/', include(('personnel.urls', 'personnel'), namespace='personnel')),
    path('habilitation/', include('habilitation.urls', namespace='habilitation')),
    path('fournisseurs/', include('fournisseurs.urls', namespace='fournisseurs')),
    path('documents/', include('documents.urls', namespace='documents')),   
    path('production/', include('production.urls', namespace='production')),
    path('clients/', include('clients.urls', namespace='clients')),
    path('commercial/', include('commercial.urls', namespace='commercial')),
]

# URLs internationalisées et admin
urlpatterns += i18n_patterns(
    # Inclusion de l'application accounts
    path('accounts/', include('accounts.urls', namespace='accounts')),
    
    # Gestion i18n
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Admin Django
    path('admin/', admin.site.urls),
)

# Fichiers médias en mode DEBUG
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
