
from django.conf import settings
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from frontend.forms import UserLoginForm

class LoginView(BaseLoginView):
    template_name = "frontend/login.html"
    authentication_form = UserLoginForm

class LogoutView(BaseLogoutView):
    next_page = "frontend:login"


class UserRegisterView(TemplateView):
    template_name = "frontend/register.html"
    success_url = reverse_lazy("frontend:login")


class UserPasswordView(TemplateView):
    success_url = reverse_lazy("frontend:login")
    template_name = 'frontend/password.html'

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
