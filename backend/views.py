import time

from ujson import loads as load_json

from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse

from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from celery.result import AsyncResult

from backend.models import User, Category, Shop, ProductInfo, Order, OrderItem, \
    Contact, STATE_CHOICE_BASKET, STATE_CHOICE_NEW
from backend.permissions import UserPermission, IsShop, IsActive, IsOwner
from backend.serializers import UserCreateSerializer, CategorySerializer, ShopSerializer, ProductInfoSerializer, \
    ProductSimpleSerializer, OrderItemSerializer, OrderSerializer, ContactSerializer, OrderSimpleSerializer
from backend.tasks import send_email, do_import


class UserViewSet(viewsets.ModelViewSet):
    """
    Служит для работы с объектом "пользователь"
    """
    queryset = User.objects.all()
    permission_classes = [UserPermission]

    def create(self, request):
        """
        Создание нового пользователя.
        """
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(username=serializer.data["username"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request):
        """
        Восстановление пароля.
        """
        try:
            user = User.objects.get(username=request.data["username"], email=request.data["email"])
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()
        except Exception as error:
            return JsonResponse({'Status': False, 'Errors': str(error)})

        send_email.delay(
            subject="Восстановление пароля",
            message=f"Ваш новый пароль: {new_password}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return Response(request.data, status=status.HTTP_200_OK)


class PartnerUpdate(RetrieveUpdateAPIView):
    """
    Класс для обновления прайса от поставщика
    """
    permission_classes = [IsAuthenticated, IsShop, IsActive]
    def post(self, request, *args, **kwargs):
        url = request.data.get('url')
        if not url:
            return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

        result = do_import.delay(url, request.user.id)
        time.sleep(2)
        return JsonResponse({'status': True, "task_id": result.id})

    def retrieve(self, request, task_id):
        result = AsyncResult(task_id)
        return JsonResponse({"task_id": result.id, "task_info": str(result.info)})


class CategoryView(ListAPIView):
    """
    Класс для просмотра категорий
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShopView(ListAPIView):
    """
    Класс для просмотра списка магазинов
    """
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer


class ProductInfoView(APIView):
    """
    Класс для поиска товаров
    """
    def get(self, request, *args, **kwargs):

        query = Q(shop__state=True)
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')

        if shop_id:
            query = query & Q(shop_id=shop_id)

        if category_id:
            query = query & Q(product__category_id=category_id)

        # фильтруем и отбрасываем дубликаты
        queryset = ProductInfo.objects.filter(
            query).select_related(
            'shop', 'product__category').prefetch_related(
            'product_parameters__parameter').distinct()

        serializer = ProductInfoSerializer(queryset, many=True)

        return Response(serializer.data)


class ProductSimpleView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = ProductInfo.objects.all().order_by("id")
        serializer = ProductSimpleSerializer(queryset, many=True)
        return Response(serializer.data)


class BasketView(ListAPIView):
    """
    Класс для работы с корзиной пользователя
    """
    permission_classes = [IsAuthenticated, IsActive]
    # Положить товары в корзину (сделать заказ со статусом "basket")
    def post(self, request, *args, **kwargs):
        items_string = request.data.get('items')
        if items_string:
            try:
                items_dict = load_json(items_string)
            except ValueError:
                return JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            try:
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
            except Exception as error:
                return JsonResponse({'Status': False, 'Errors': str(error)})

            OrderItem.objects.filter(order=basket.id).delete()
            objects_created = 0
            for order_item in items_dict:
                order_item.update({'order': basket.id})
                serializer = OrderItemSerializer(data=order_item)
                if serializer.is_valid():
                    try:
                        serializer.save()
                    except IntegrityError as error:
                        return JsonResponse({'Status': False, 'Errors': str(error)})
                    else:
                        objects_created += 1
                else:
                    return JsonResponse({'Status': False, 'Errors': serializer.errors})
            return JsonResponse({'Status': True, 'Создано объектов': objects_created})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

class OrderDetailView(RetrieveAPIView):
    """
    Класс для получения и размещения заказов пользователями
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsActive, IsOwner]
    # получить один мой заказ
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class OrderView(APIView):
    """
    Класс для получения и размещения заказов пользователями
    """
    permission_classes = [IsAuthenticated, IsActive]
    # получить мои заказы
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(
            user_id=request.user.id).exclude(state='basket').distinct()

        serializer = OrderSimpleSerializer(order, many=True)
        return Response(serializer.data)

    # разместить заказ из корзины
    def post(self, request, *args, **kwargs):
        if len(Order.objects.filter(user_id=request.user.id, state=STATE_CHOICE_BASKET)) == 0:
            return JsonResponse({"Status": False, "Error": "Корзина не сохранена"})
        basket = Order.objects.get(user_id=request.user.id, state=STATE_CHOICE_BASKET)
        if len(OrderItem.objects.filter(order=basket)) == 0:
            return JsonResponse({"Status": False, "Error": "Корзина пуста"})

        if {'contact'}.issubset(request.data) and request.data['contact']:
            try:
                basket.state = STATE_CHOICE_NEW
                basket.contact_id = request.data['contact']
                basket.save()
                send_email.delay(
                    subject=f'Заказ номер #{basket.id}',
                    message=f"Вы сделали заказ.\n" \
                            f'Дата заказа: {basket.dt}\n' \
                            f'Статус: {basket.state}\n' \
                            f'Контакт: {basket.contact}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[request.user.email]
                )
                return JsonResponse({'Status': True})
            except IntegrityError as error:
                print(error)
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указаны аргументы'})
        return JsonResponse({'Status': False, 'Errors': 'Не указан контакт'})

class ContactView(APIView):
    """
    Класс для работы с контактами покупателей
    """
    permission_classes = [IsAuthenticated, IsActive]
    # получить мои контакты
    def get(self, request, *args, **kwargs):
        contact = Contact.objects.filter(
            user_id=request.user.id)
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

    # добавить новый контакт
    def post(self, request, *args, **kwargs):
        if {'city', 'street', 'phone'}.issubset(request.data):
            if hasattr(request.data, "_mutable"):
                request.data._mutable = True
            request.data.update({'user': request.user.id})
            serializer = ContactSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': serializer.errors})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # удалить список контактов
    def delete(self, request, *args, **kwargs):
        items_string = request.data.get('items')
        if items_string:
            items_list = items_string.split(',')
            query = Q()
            objects_deleted = False
            for contact_id in items_list:
                if contact_id.isdigit():
                    query = query | Q(user_id=request.user.id, id=contact_id)
                    objects_deleted = True
            if objects_deleted:
                deleted_count = Contact.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Удалено объектов': deleted_count})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # редактировать контакт
    def put(self, request, *args, **kwargs):
        if 'id' in request.data:
            if request.data['id'].isdigit():
                contact = Contact.objects.filter(id=request.data['id'], user_id=request.user.id).first()
                print(contact)
                if contact:
                    serializer = ContactSerializer(contact, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'Status': True})
                    else:
                        return JsonResponse({'Status': False, 'Errors': serializer.errors})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
