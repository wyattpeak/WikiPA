from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path('', views.index, name='index'),
    path('page/', views.PageListView.as_view(), name='page-index'),
    path('page/create/', views.PageCreateView.as_view(), name='page-create'),
    path('page/<int:pk>/delete/', views.PageDeleteView.as_view(), name='page-delete'),
    path('page/<int:pk>/push/', views.page_push, name='page-push'),
]
