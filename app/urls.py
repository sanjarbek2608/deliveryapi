from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RestaurantViewSet, MenuViewSet, OrderViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('restaurants', RestaurantViewSet)
router.register('menu', MenuViewSet)
router.register('order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls))
]

