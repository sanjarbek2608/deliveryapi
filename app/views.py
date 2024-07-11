from rest_framework import viewsets
from .serializers import UserSerializer, RestaurantSerializer, MenuSerializer, OrderSerializer
from .models import CustomUser, Restaurant, Menu, Order
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from .permissions import IsOrderOwnerOrAdmin,IsAdmin
import logging

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAdmin()]
    
    
    
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [AllowAny()]
    

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'update', 'partial_update','destroy']:
            return [IsAdminUser()]
        if self.action in ['retrieve']:
            return [IsOrderOwnerOrAdmin()]
        return [IsAuthenticated()]
       
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    
    def perform_create(self, serializer):
        items = self.request.data.get('items')
        total_price = 0
        for item_id in items:
            item = Menu.objects.get(id=item_id)
            total_price += item.price
        
        logger.info('New order created')    
        serializer.save(user = self.request.user, total_price = total_price) 
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.status = 'canceled'
        order.save()
        logger.info('Order canceled')
        return Response({"status": "canceled"})   
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        order = self.get_object()
        order.status = 'accepted'
        order.save()
        logger.info('Order accepted')
        return Response({
            "status": "Order accepted"
        })
        
    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):
        order = self.get_object()
        order.status = 'delivered'
        order.save()
        return Response({
            "status": "Order delivered"
        })
 
    
    @action(detail=True, methods=['post'])
    def delivery_time(self, request, pk=None):
        order = self.get_object()
        if order.status == 'pending':
            return Response({"status": "Order is in the process of confirmation"})
        if order.status == 'canceled':
            return Response({"status": "Order has been canceled"})
        if order.status == 'delivered':
            return Response({"status": "Order already delivered"})
        if order.status == 'accepted':
            distance = round(order.get_distance(), 1)
            order_count = Order.objects.filter(status='accepted').count()
            order_items = order.items.count()
            food_cooking_time = order_items * (5/4)

            delivery_road_time = round(distance * 3)
            
            total = round(food_cooking_time + delivery_road_time)
            
            return Response({
                "id": order.id,
                "distance": distance,
                "road_time": delivery_road_time,
                "order_items": order_items,
                "food_cooking_time": food_cooking_time,
                "delivery_time": total
            })