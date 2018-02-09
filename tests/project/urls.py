from rest_framework import routers

from .views import ChefViewSet, MenuItemViewSet, MenuItemOptionViewSet


router = routers.SimpleRouter()

router.register('chef', ChefViewSet)
router.register('menu-items', MenuItemViewSet)
router.register('menu-item-options', MenuItemOptionViewSet)

urlpatterns = router.urls
