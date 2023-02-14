from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=False, default='')
    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Называние')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='product_image', verbose_name='Изображение')
    price = models.IntegerField(verbose_name='Цена')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)


# class Order(models.Model):

class Customer(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    number = models.CharField(max_length=1000)
    addres = models.CharField(max_length=500)
    message = models.TextField()


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    phone = models.IntegerField()
    addres = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True)

