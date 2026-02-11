from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_documents'

router = NetBoxRouter()
router.register('documents', views.DocumentViewSet)

urlpatterns = router.urls
