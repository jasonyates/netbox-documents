from rest_framework.routers import APIRootView
from netbox.api.routers import NetBoxRouter
from . import views


class NetboxDocumentsRootView(APIRootView):
    """
    Netbox Documents API root view
    """
    def get_view_name(self):
        return 'Netbox Documents'


app_name = 'netbox_documents'

router = NetBoxRouter()
router.APIRootView = NetboxDocumentsRootView
router.register('documents', views.DocumentViewSet)

urlpatterns = router.urls
