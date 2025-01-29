from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Custom User Model
# Custom User Model
class CustomUser(AbstractUser):

    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)


    # Override the groups field to set a related_name
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related_name
        blank=True,
    )

    # Override the user_permissions field to set a related_name
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set_permissions',  # Custom related_name
        blank=True,
    )

    def __str__(self):
        return self.username






class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    description = models.TextField(default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True, blank=True)
    tags = models.CharField(max_length=255, default=None, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    weight = models.CharField(max_length=50, default=None, null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True, blank=True)
    # Add any additional fields here

    def __str__(self):
        return self.name
    



    

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart for {self.user.username}'

# CartItem Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('shipped', 'Shipped'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

# OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Order {self.order.id}'





# Blog Model (For Farmers)
class Blog(models.Model):
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title





# Forum post model
class ForumPost(models.Model):
    title = models.CharField(max_length=255)  # Title of the post
    content = models.TextField()  # Main content of the post
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Post author, linked to CustomUser
    created_at = models.DateTimeField(default=timezone.now)  # Post creation time
    updated_at = models.DateTimeField(auto_now=True)  # Post updated time
    views = models.IntegerField(default=0)  # Number of views

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Order by newest posts first





# Reply model for the forum post
class Reply(models.Model):
    post = models.ForeignKey(ForumPost, related_name='replies', on_delete=models.CASCADE)  # The post being replied to
    content = models.TextField()  # Content of the reply
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Author of the reply
    created_at = models.DateTimeField(default=timezone.now)  # Time the reply was created

    def __str__(self):
        return f"Reply by {self.author} on {self.post.title}"

    class Meta:
        ordering = ['created_at']  # Order replies by oldest first





class FarmerPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Donation(models.Model):
    farmer_post = models.ForeignKey(FarmerPost, on_delete=models.CASCADE, related_name='donations')
    donor_name = models.CharField(max_length=100)
    donor_phone = models.CharField(max_length=15)
    donor_email = models.EmailField()
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation by {self.donor_name} for {self.farmer_post.title}"






class Checkout(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    transaction_number = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.full_name} - {self.product.name}'