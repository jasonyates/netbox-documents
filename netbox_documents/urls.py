from django.urls import path
from . import models, views
from netbox.views.generic import ObjectChangeLogView

urlpatterns = (

    # SiteDocument
    path('site-document/', views.SiteDocumentListView.as_view(), name='sitedocument_list'),
    path('site-document/add/', views.SiteDocumentEditView.as_view(), name='sitedocument_add'),
    path('site-document/<int:pk>/', views.SiteDocumentView.as_view(), name='sitedocument'),
    path('site-document/<int:pk>/edit/', views.SiteDocumentEditView.as_view(), name='sitedocument_edit'),
    path('site-document/<int:pk>/delete/', views.SiteDocumentDeleteView.as_view(), name='sitedocument_delete'),
    path('site-document/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='sitedocument_changelog', kwargs={
        'model': models.SiteDocument
    }),

    # DeviceDocument
    path('device-document/', views.DeviceDocumentListView.as_view(), name='devicedocument_list'),
    path('device-document/add/', views.DeviceDocumentEditView.as_view(), name='devicedocument_add'),
    path('device-document/<int:pk>/', views.DeviceDocumentView.as_view(), name='devicedocument'),
    path('device-document/<int:pk>/edit/', views.DeviceDocumentEditView.as_view(), name='devicedocument_edit'),
    path('device-document/<int:pk>/delete/', views.DeviceDocumentDeleteView.as_view(), name='devicedocument_delete'),
    path('device-document/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='devicedocument_changelog', kwargs={
        'model': models.DeviceDocument
    }),

    # CircuitDocument
    path('circuit-document/', views.CircuitDocumentListView.as_view(), name='circuitdocument_list'),
    path('circuit-document/add/', views.CircuitDocumentEditView.as_view(), name='circuitdocument_add'),
    path('circuit-document/<int:pk>/', views.CircuitDocumentView.as_view(), name='circuitdocument'),
    path('circuit-document/<int:pk>/edit/', views.CircuitDocumentEditView.as_view(), name='circuitdocument_edit'),
    path('circuit-document/<int:pk>/delete/', views.CircuitDocumentDeleteView.as_view(), name='circuitdocument_delete'),
    path('circuit-document/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='circuitdocument_changelog', kwargs={
        'model': models.CircuitDocument
    }), 
    

)