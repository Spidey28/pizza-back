from django.db import models
from main.base.models import TimeStampedModel
from .types import FoodCategory, OrderStatus, PAYMENTINSTRUMENT, PAYMENTSTATUS


class Category(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    image = models.FileField(blank=True, null=True)
    config = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategory(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.name


class Size(TimeStampedModel):
    name = models.CharField(max_length=20, unique=True)
    amount = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def __str__(self):
        return self.name


class Crust(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    amount = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Crust"
        verbose_name_plural = "Crusts"

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    FOOD_CATEGORY_CHOICES = (
        (FoodCategory.VEG, "Veg"),
        (FoodCategory.NON_VEG, "Non Veg"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="category"
    )
    sub_category = models.ForeignKey(SubCategory,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     )
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0.0)
    image = models.FileField(blank=True, null=True)
    food_category = models.PositiveSmallIntegerField(
        choices=FOOD_CATEGORY_CHOICES,
        default=FoodCategory.VEG,
    )
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, null=True, blank=True)
    crust = models.ForeignKey(
        Crust, on_delete=models.CASCADE, null=True, blank=True)
    meta_data = models.JSONField(blank=True, null=True)


class Address(TimeStampedModel):
    line_1 = models.CharField(max_length=255, null=True, blank=True)
    line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Customer(TimeStampedModel):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=13, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Discount(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=50)
    name = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(default=0.0)
    valid_till_date = models.DateTimeField()
    image = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    ORDER_STATUS_CHOICES = (
        (OrderStatus.CART, "In Cart"),
        (OrderStatus.CHECKOUT, "Order Checkout"),
        (OrderStatus.SUCCESSFUL, "Order Successful"),
        (OrderStatus.FAILED, "Order Failed"),
    )

    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
    )
    status = models.PositiveSmallIntegerField(
        choices=ORDER_STATUS_CHOICES,
        default=OrderStatus.CART
    )
    amount = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0)
    total_amount = models.FloatField(default=0.0)
    reedeem_points = models.PositiveIntegerField(blank=True, null=True)
    discount = models.ForeignKey(
        Discount, on_delete=models.CASCADE, blank=True, null=True)
    discounted_amount = models.FloatField(default=0.0)


class OrderItem(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    quantity = models.PositiveIntegerField(default=1)
    amount = models.FloatField(default=0.0)


class Payment(TimeStampedModel):
    PAYMENT_STATUS_CHOICES = (
        (PAYMENTSTATUS.SUCCESS, 'Success'),
        (PAYMENTSTATUS.PENDING, 'Pending'),
        (PAYMENTSTATUS.FAILURE, 'Failure'),
        (PAYMENTSTATUS.PAYMENT_DEDUCTED, 'Payment Deducted')
    )
    PAYMENT_INSTRUMENT_CHOICES = (
        (PAYMENTINSTRUMENT.ONLINE, 'Online'),
        (PAYMENTINSTRUMENT.UPI, 'UPI'),
        (PAYMENTINSTRUMENT.CREDIT_CARD, 'Credit Card'),
        (PAYMENTINSTRUMENT.DEBIT_CARD, 'Debit Card')
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0)
    total_amount = models.FloatField(default=0.0)
    payment_order_id = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        unique=True
    )
    reference_id = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    status = models.PositiveSmallIntegerField(
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENTSTATUS.PENDING
    )
    instrument_type = models.PositiveSmallIntegerField(
        choices=PAYMENT_INSTRUMENT_CHOICES,
        default=PAYMENTINSTRUMENT.ONLINE
    )
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_success_date = models.DateField(blank=True, null=True)
    payment_url = models.URLField(max_length=2048, blank=True, null=True)
    payment_gateway_response = models.TextField(null=True, blank=True)
    payment_receipt = models.FileField(
        blank=True,
        null=True
    )


class FoodPoint(TimeStampedModel):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
    )
    gifted_points = models.PositiveIntegerField(blank=True, null=True)
    last_order_points = models.PositiveIntegerField(blank=True, null=True)
    referral_points = models.PositiveIntegerField(blank=True, null=True)


class AddOn(TimeStampedModel):
    FOOD_CATEGORY_CHOICES = (
        (FoodCategory.VEG, "Veg"),
        (FoodCategory.NON_VEG, "Non Veg"),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    amount = models.FloatField(default=0.0)
    image = models.FileField(null=True, blank=True)
    food_category = models.PositiveSmallIntegerField(
        choices=FOOD_CATEGORY_CHOICES,
        default=FoodCategory.VEG,
    )

    def __str__(self):
        return self.name


class Topping(TimeStampedModel):
    FOOD_CATEGORY_CHOICES = (
        (FoodCategory.VEG, "Veg"),
        (FoodCategory.NON_VEG, "Non Veg"),
    )
    name = models.CharField(max_length=50, unique=True)
    amount = models.FloatField(default=0.0)
    image = models.FileField(null=True, blank=True)
    food_category = models.PositiveSmallIntegerField(
        choices=FOOD_CATEGORY_CHOICES,
        default=FoodCategory.VEG,
    )

    def __str__(self):
        return self.name
