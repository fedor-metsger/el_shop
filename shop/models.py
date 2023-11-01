
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator

# Create your models here.
STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

USER_TYPE_CUSTOMER = "customer"
USER_TYPE_SHOP = "shop"

USER_TYPE_CHOICES = (
    (USER_TYPE_SHOP, 'Магазин'),
    (USER_TYPE_CUSTOMER, 'Покупатель'),
)


class UserManager(BaseUserManager):
    """
    Миксин для управления пользователями
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Стандартная модель пользователей
    """
    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(
        _('адрес email'), unique=True,
        error_messages = {
            'unique': _("Пользователь с таким e-mail адресом уже существует.")
        }
    )
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Необходимо не более 150 символов. Только буквы, цифры и знаки @/./+/-/_'),
        validators=[username_validator],
        error_messages={
            'unique': _("Пользователь с таким именем уже существует."),
        },
        unique=True
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Обозначает, должен ли этот пользователь считаться активным. '
            'Снимите выделение вместо удаления пользователя.'
        ),
    )
    type = models.CharField(verbose_name='тип пользователя',
                            choices=USER_TYPE_CHOICES, max_length=8, default='customer')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = "список пользователей"
        ordering = ('email',)


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    url = models.URLField(verbose_name='ссылка', null=True, blank=True)
    user = models.OneToOneField(User, verbose_name='пользователь',
                                blank=True, null=True,
                                on_delete=models.CASCADE)
    state = models.BooleanField(verbose_name='статус получения заказов', default=True)

    # filename

    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = "список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='название')
    shops = models.ManyToManyField(Shop, verbose_name='магазины', related_name='categories', blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = "список категорий"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=80, verbose_name='название')
    category = models.ForeignKey(Category, verbose_name='категория', related_name='products', blank=True,
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = "список продуктов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    model = models.CharField(max_length=80, verbose_name='модель', blank=True)
    external_id = models.PositiveIntegerField(verbose_name='внешний ID')
    product = models.ForeignKey(Product, verbose_name='продукт', related_name='product_infos', blank=True,
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='магазин', related_name='product_infos', blank=True,
                             on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество')
    price = models.PositiveIntegerField(verbose_name='цена')
    price_rrc = models.PositiveIntegerField(verbose_name='рекомендуемая розничная цена')

    class Meta:
        verbose_name = 'информация о продукте'
        verbose_name_plural = "информационный список о продуктах"
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop', 'external_id'], name='unique_product_info'),
        ]


class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name='название')

    class Meta:
        verbose_name = 'имя параметра'
        verbose_name_plural = "список имен параметров"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name='информация о продукте',
                                     related_name='product_parameters', blank=True,
                                     on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='параметр', related_name='product_parameters', blank=True,
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name='значение', max_length=100)

    class Meta:
        verbose_name = 'параметр'
        verbose_name_plural = "список параметров"
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
        ]


class Contact(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь',
                             related_name='contacts', blank=True,
                             on_delete=models.CASCADE)

    city = models.CharField(max_length=50, verbose_name='город')
    street = models.CharField(max_length=100, verbose_name='улица')
    house = models.CharField(max_length=15, verbose_name='дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='корпус', blank=True)
    building = models.CharField(max_length=15, verbose_name='строение', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='телефон')

    class Meta:
        verbose_name = 'контакты пользователя'
        verbose_name_plural = "список контактов пользователя"

    def __str__(self):
        return f'{self.city} {self.street} {self.house}'


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь',
                             related_name='orders', blank=True,
                             on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name='статус', choices=STATE_CHOICES, max_length=15)
    contact = models.ForeignKey(Contact, verbose_name='контакт',
                                blank=True, null=True,
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = "список заказов"
        ordering = ('-dt',)

    def __str__(self):
        return str(self.dt)

    # @property
    # def sum(self):
    #     return self.ordered_items.aggregate(total=Sum("quantity"))["total"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', related_name='ordered_items', blank=True,
                              on_delete=models.CASCADE)

    product_info = models.ForeignKey(ProductInfo, verbose_name='информация о продукте', related_name='ordered_items',
                                     blank=True,
                                     on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество')

    class Meta:
        verbose_name = 'заказанная позиция'
        verbose_name_plural = "список заказанных позиций"
        constraints = [
            models.UniqueConstraint(fields=['order_id', 'product_info'], name='unique_order_item'),
        ]

# class Basket(models.Model):
#     user = models.ForeignKey(User, verbose_name='пользователь',
#                              related_name='basket_items', blank=True,
#                              on_delete=models.CASCADE)
#     dt = models.DateTimeField(auto_now_add=True)
#     product_info = models.ForeignKey(ProductInfo, verbose_name='продукт',
#                                      related_name='baskets_items', blank=True,
#                                      on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(verbose_name='количество')
#
#
#     class Meta:
#         verbose_name = 'корзина'
#         verbose_name_plural = "список товаров в корзине"
#         ordering = ('-dt',)
#
#     def __str__(self):
#         return str(self.dt)
