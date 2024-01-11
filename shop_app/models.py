from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категорія")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Image(models.Model):
    img_url = models.ImageField(verbose_name="Посилання на зображення" )
    def __str__(self):
        return f"{self.img_url}"

    class Meta:
        verbose_name = "Зображення"
        verbose_name_plural = "Зображення"



class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ім'я товару")
    price = models.FloatField(verbose_name="Вартість")
    discription = models.TextField(verbose_name="Опис")
    image = models.ManyToManyField(Image, verbose_name="Зображення")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    video = models.CharField(max_length=255, verbose_name="відео", blank=True)

    ram = models.IntegerField(verbose_name="ОЗП", blank=True, null=True)
    rom = models.IntegerField(verbose_name="ПЗП", blank=True, null=True)
    display = models.IntegerField(verbose_name="Діагональ дисплея", blank=True, null=True)
    brand = models.CharField(max_length=255, verbose_name="Бренд", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач", null=True, blank=True)
    products = models.ManyToManyField(Product, verbose_name="Товари", through="CartItem")

    class Meta:
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"

    def items(self):
        """Надає продукт та його айтем"""
        products = self.products.all()
        items  = CartItem.objects.all().filter(cart_id=self.id)
        data_set = []
        for product in products:
            for item in items:
                if product.id == item.product_id:
                    data_set.append([item.id, item.cart_id, product.name, item.amount, product.price])

        return data_set

class CartItem(models.Model):
    """Кастомна проміжна таблиця, потрібна для підрахунку кількості товарів"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Кошик")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    amount = models.IntegerField(default=1, verbose_name="Кількість")

    class Meta:
        verbose_name = "Об'єкт корзини"
        verbose_name_plural = "Об'єкти корзини"

class Order(models.Model):
    """Це модель вже оформленного замовлення"""


    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    name = models.CharField(max_length=255, verbose_name="Ім'я отримувача")
    surname = models.CharField(max_length=255, verbose_name="Прізвище отримувача")
    patronymic = models.CharField(max_length=255, verbose_name="Побатькові отримувача")
    phone = models.CharField(max_length=255, verbose_name="Телефон отримувача")
    selectedcity = models.CharField(max_length=255, verbose_name="Місто отримувача")
    selectedwarehouse = models.CharField(max_length=255, verbose_name="Пункт отримання")
    products = models.TextField(verbose_name="Замовлені товари")
    status = models.CharField(max_length=255, verbose_name="Статус замовлення")

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"