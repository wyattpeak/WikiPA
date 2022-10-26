from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path('', views.index, name='index'),
    path('page/', views.PageListView.as_view(), name='page-index'),
    path('page/create/', views.PageCreateView.as_view(), name='page-create'),
    path('page/<int:pk>/delete/', views.PageDeleteView.as_view(), name='page-delete'),
    path('page/<int:pk>/push/', views.page_push, name='page-push'),
    path('page/bulk-import/', views.PageBulkImportView.as_view(), name='page-bulk-import'),
    path('backup/dump/', views.backup_dump, name='backup-dump'),
    path('backup/load/', views.BackupLoadView.as_view(), name='backup-load'),
    path('category/', views.CategoryListView.as_view(), name='category-index'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('pa/request/', views.RequestListView.as_view(), name='pa-request-index'),
    path('pa/create/', views.pa_create, name='pa-create')
]
