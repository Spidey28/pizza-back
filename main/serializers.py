from rest_framework import serializers

from .models import Category, Crust, Discount, Product, Size, Topping


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "image",
        )


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = (
            "id",
            "coupon_code",
            "name",
            "amount",
            "image",
        )


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = (
            "id",
            "name",
            "amount",
        )


class CrustSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crust
        fields = (
            "id",
            "name",
            "amount",
        )


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = (
            "id",
            "name",
            "amount",
            "image",
            "food_category",
            "category",
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "image",
            "food_category",
            "size",
            "crust",
            "toppings",
        )
