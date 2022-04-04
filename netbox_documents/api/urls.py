from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_documents'

router = NetBoxRouter()
router.register('site-documents', views.SiteDocumentViewSet)
router.register('device-documents', views.DeviceDocumentViewSet)
router.register('circuit-documents', views.CircuitDocumentViewSet)

urlpatterns = router.urls