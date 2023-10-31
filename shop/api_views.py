
from yaml import load as load_yaml, Loader
from requests import get

from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import URLValidator
from django.http import JsonResponse

from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from shop.models import User, Category, Shop, ProductInfo, Product, Parameter, ProductParameter
from shop.permissions import UserPermission, IsShop, IsActive
from shop.serializers import UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Служит для работы с объектом "пользователь"
    """
    queryset = User.objects.all()
    # serializer_class = UserCreateSerializer
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
        # serializer = UserPwdSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.data["username"], email=request.data["email"])
        new_password = User.objects.make_random_password()
        user.set_password(new_password)
        user.save()

        send_mail(
            subject="Восстановление пароля",
            message=f"Ваш новый пароль: {new_password}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return Response(request.data, status=status.HTTP_200_OK)


class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика
    """
    permission_classes = [IsAuthenticated, IsShop, IsActive]
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        #
        # if request.user.type != 'shop':
        #     return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = get(url).content

                data = load_yaml(stream, Loader=Loader)

                shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()
                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                    product_info = ProductInfo.objects.create(product_id=product.id,
                                                              external_id=item['id'],
                                                              model=item['model'],
                                                              price=item['price'],
                                                              price_rrc=item['price_rrc'],
                                                              quantity=item['quantity'],
                                                              shop_id=shop.id)
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)

                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})