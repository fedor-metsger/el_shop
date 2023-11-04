
from django.db.models import Sum, F, Count
from rest_framework import serializers

from backend.models import User, Category, Shop, Product, ProductParameter, ProductInfo, Contact, OrderItem, Order


class UserPwdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "company", "position", "type"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'company', 'position', 'contacts')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'state',)
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value',)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters',)
        read_only_fields = ('id',)


class ProductSimpleSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    shop = serializers.CharField(source='shop.name')
    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'shop', 'quantity']
        read_only_fields = ('id',)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity', 'order',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }


class OrderItemCreateSerializer(OrderItemSerializer):
    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'ordered_items', 'state', 'dt', 'contact',)
        read_only_fields = ('id',)

class OrderSimpleSerializer(serializers.ModelSerializer):
    count_items = serializers.SerializerMethodField()
    total_sum = serializers.SerializerMethodField()

    def get_count_items(self, obj):
        cnt = Order.objects.filter(id=obj.id).annotate(
            count_items=Sum("ordered_items__quantity")).first().count_items
        return cnt

    def get_total_sum(self, obj):
        s = Order.objects.filter(id=obj.id).annotate(
            count_items=Sum(
                F('ordered_items__quantity') * F('ordered_items__product_info__price')
            )
        ).first().count_items
        return s

    class Meta:
        model = Order
        fields = ["id", "state", "dt", "count_items", "total_sum"]
        read_only_fields = ['id']