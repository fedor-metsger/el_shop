
from django.conf import settings
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from shop.forms import UserRegisterForm, UserPasswordForm
from shop.models import User

class LoginView(BaseLoginView):
    template_name = "shop/login.html"

class LogoutView(BaseLogoutView):
    next_page = "shop:login"

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "shop/register.html"
    success_url = reverse_lazy("shop:login")

    def form_valid(self, form):
        self.object = form.save()
        # self.object.activated = False
        # code = User.objects.make_random_password()
        # self.object.activation_code = code
        # self.object.save(update_fields=['activation_code'])
        # send_mail(
        #     subject='Поздравляем с регистрацией',
        #     message='Вы зарегистрировались на нашей платформе, добро пожаловать!\n'
        #     f'Для активации пользовательского эккаунта введите код: {code}\n'
        #     f'или перейдите по ссылке: {reverse_lazy("shop:activation")}/{self.object.id}/'
        #     f'?code={code}',
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[self.object.email]
        # )
        send_mail(
            subject='Поздравляем с регистрацией',
            message='Вы зарегистрировались на нашей платформе, добро пожаловать!\n'
            f'Ваше имя пользователя: {self.object.username}\n',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )
        return super().form_valid(form)

# class UserActivationView(UpdateView):
#     model = User
#     form_class = UserActivationForm
#     template_name = reverse_lazy("shop:activation")
#
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             ret = reverse("catalog:index")
#         else:
#             ret = reverse("user:login")
#
#         return ret
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         def_code = self.request.GET.get("code", '')
#         kwargs.update({"initial": {"user_code": def_code}})
#         return kwargs
#
#     def form_valid(self, form):
#         if self.request.method == 'POST':
#             user_code = self.request.POST.get("user_code")
#         # user_code = form.cleaned_data['user_code']
#             self.object = form.save()
#             if user_code == self.object.activation_code:
#                 self.object.activated = True
#                 self.object.save(update_fields=['activated'])
#                 send_mail(
#                     subject="Активация эккаунта",
#                     message="Эккаунт активирован!\n",
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[self.object.email]
#                 )
#             else:
#                 form.add_error("user_code", "Неправильный код!")
#                 return super().form_invalid(form)
#         return super().form_valid(form)
#
# class UserUpdateView(UpdateView):
#     model = User
#     fields = ("email", "phone", "telegram", "avatar", "country")
#     success_url = reverse_lazy("catalog:index")

class UserPasswordView(TemplateView):
    model = User
    form_class = UserPasswordForm
    success_url = reverse_lazy("shop:login")
    template_name = 'shop/password.html'

    def form_valid(self, form):
        self.object = form.save()

        new_password = User.objects.make_random_password()
        self.object.set_password(new_password)
        self.object.save(update_fields=['password'])
        send_mail(
            subject="Восстановление пароля",
            message=f"Ваш новый пароль: {new_password}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )
        return super().form_valid(form)