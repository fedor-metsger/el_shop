
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import viewsets, status
from rest_framework.response import Response

from shop.models import User
from shop.permissions import UserPermission
from shop.serializers import UserPwdSerializer, UserCreateSerializer


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