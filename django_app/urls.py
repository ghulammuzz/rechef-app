
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    # admin site
    path('admin/', admin.site.urls),
    
    # sub apps
    path('auth/', include("account.urls")),
    path('api/', include("recipe.urls")),
    
    # path media
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
