# Create your views here.
import logging

from django.shortcuts import render
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from main.base import response
from main.base.viewsets import GenericViewSet as ViewSet

from .models import Category, Crust, Discount, Product, Size, Topping
from .serializers import (
    CategorySerializer,
    CrustSerializer,
    OfferSerializer,
    ProductSerializer,
    SizeSerializer,
    ToppingSerializer,
)


class RequestViewSet(ViewSet):
    permission_classes = (AllowAny,)

    @action(methods=["GET"], detail=False)
    def homepage(self, request, *args, **kwargs):
        categories = CategorySerializer(Category.objects.all(), many=True)
        offers = OfferSerializer(Discount.objects.all(), many=True)
        return response.Ok({"categories": categories.data, "offers": offers.data})

    @action(methods=["GET"], detail=False)
    def menu(self, request, *args, **kwargs):
        serializer = ProductSerializer(Product.objects.all(), many=True)

        return response.Ok(serializer.data)


class ServicesViewSet(ViewSet):
    permission_classes = (AllowAny,)

    @action(methods=["GET"], detail=False)
    def size(self, request, *args, **kwargs):
        serializer = SizeSerializer(Size.objects.all(), many=True)

        return response.Ok(serializer.data)

    @action(methods=["GET"], detail=False)
    def crust(self, request, *args, **kwargs):
        serializer = CrustSerializer(Crust.objects.all(), many=True)

        return response.Ok(serializer.data)

    @action(methods=["GET"], detail=False)
    def toppings(self, request, *args, **kwargs):
        serializer = ToppingSerializer(Topping.objects.all(), many=True)

        return response.Ok(serializer.data)
