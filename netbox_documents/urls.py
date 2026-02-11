from django.urls import path
from . import models, views
from netbox.views.generic import ObjectChangeLogView

urlpatterns = (
    path('documents/', views.DocumentListView.as_view(), name='document_list'),
    path('documents/add/', views.DocumentEditView.as_view(), name='document_add'),
    path('documents/<int:pk>/', views.DocumentView.as_view(), name='document'),
    path('documents/<int:pk>/edit/', views.DocumentEditView.as_view(), name='document_edit'),
    path('documents/<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document_delete'),
    path('documents/delete/', views.DocumentBulkDeleteView.as_view(), name='document_bulk_delete'),
    path('documents/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='document_changelog', kwargs={
        'model': models.Document
    }),
)
