from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Debtor(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Ism va familiyasi")
    social_link = models.TextField(blank=True, null=True, verbose_name="Ijtimoiy tarmoqdagi manzili")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon nomeri")
    address = models.TextField(blank=True, null=True, verbose_name="Manzili")

    def __str__(self):
        return self.full_name
    
class Debt(models.Model):
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, related_name="debts")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.debtor.full_name} - {self.amount} so'm"

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class ProductRequest(models.Model):

    CATEGORY_CHOICES = [
        ('sabzavot', 'Sabzavotlar'),
        ('meva', 'Meva'),
        ('gosht', "Go'sht mahsulotlari"),
    ]

    UNIT_CHOICES = [
        ('kg', 'kg'),
        ('dona', 'dona'),
        ('litr', 'litr'),
    ]

    STATUS_CHOICES = [
        ('kutilyapti', 'Kutilyapti'),
        ('qabul_qilingan', 'Qabul qilindi'),
        ('bekor_qilingan', 'Bekor qilindi'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot Nomi")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Kategoriya")
    required_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kerakli Miqdor")
    measurement_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="O'lchov Birligi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Holati")
    note = models.TextField(blank=True, verbose_name="Qo'shimcha Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    def __str__(self):
        return self.product.name

from django.db import models

class Warehouse(models.Model):
    CATEGORY_CHOICES = [
        ('Sabzavot', 'Sabzavot'),
        ('Meva', 'Meva'),
        ('Ichimliklar', 'Ichimliklar'),
        ('Go`sht Mahsulotlari', 'Go`sht Mahsulotlari'),
        ('Sut Mahsulotlari', 'Sut Mahsulotlari'),
    ]

    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('dona', 'Dona'),
        ('litr', 'Litr'),
    ]

    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name="Mahsulot Nomi")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Kategoriya")
    quantity = models.PositiveIntegerField(verbose_name="Boshlang'ich Miqdor")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="Oʻlchov Birligi")
    arrival_date = models.DateField(verbose_name="Kelgan Sana")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Olingan Narxi (so'mda)")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (so'mda)")
    expiry_date = models.DateField(verbose_name="Saqlash Muddat")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha Ma'lumot")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.category}"
