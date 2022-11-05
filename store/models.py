from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50 , blank=True,null=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_all_category():
        return Category.objects.all()

    
# Customer Model


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=16, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,max_length=50,on_delete=models.CASCADE, null=True)
    images = models.ImageField(null=True, blank=True)
    descriptions = models.CharField(max_length=500 , null=True)


    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_product_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    def __str__(self):
        return self.name

    @property
    def imagesURL(self):
        try:
            url = self.images.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200)
    total = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitmes =self.orderitem_set.all()
        total = sum([item.get_total() for item in orderitmes])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return str(self.product.name)

    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def save(self, *args, **kwargs):
        if self.quantity and self.product:
            self.total = self.product.price * self.quantity

        super().save(*args, **kwargs)

class OrderDetail(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)

    mobile = models.CharField(max_length=14, null=True)
    emailaddress = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class HomepageSlideshow(models.Model):
    image = models.ImageField(null=True, blank=True)
    heading = models.CharField(max_length=200, null=True)
    
    @property
    def imagesURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def __str__(self):
        return self.heading
    
class Province(models.Model):
    name = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=20, null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Area(models.Model):
    name = models.CharField(max_length=20, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.name

class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.customer.name
    