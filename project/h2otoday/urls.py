from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    path('wiki/', include('wiki.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('wiki:index')))
]
