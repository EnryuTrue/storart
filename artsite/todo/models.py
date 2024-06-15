from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Custom validator for the username (at least 8 characters)
username_validator = RegexValidator(
    regex=r'^.{8,}$',
    message='Username must contain at least 8 characters.',
    code='invalid_username'
)

# Custom validator for the phone number (exactly 10 digits)
phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Phone number must contain exactly 10 digits.',
    code='invalid_phone'
)

# Custom validator for the password (at least 8 characters)
password_validator = RegexValidator(
    regex=r'^.{8,}$',
    message='Password must contain at least 8 characters.',
    code='invalid_password'
)


class User(AbstractUser):
    username = models.CharField(max_length=24, validators=[username_validator])
    full_name = models.CharField(max_length=50)
    address = models.CharField(max_length=25)
    email = models.EmailField(null=True)
    bio = models.TextField(max_length=300)
    password = models.CharField(max_length=100, validators=[password_validator])
    phone = models.CharField(max_length=10, validators=[phone_validator], null=True, )
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default_profile.jpg')
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    status_choices = [
        ('basic_user', 'basic user'),
        ('pending_seller_approval', 'Pending Seller Approval'),
        ('seller', 'Seller')
    ]
    status = models.CharField(max_length=23, choices=status_choices, default='basic_user')

    def __str__(self):
        return self.username


class ArtPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='art_posts/')
    title = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    CATEGORY_CHOICES = [
        ('painting', 'Painting'),
        ('photography', 'Photography'),
        ('sculpture', 'Sculpture'),
        ('digital_art', 'Digital Art'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    ART_TYPES = [
        ('physical', 'Physical'),
        ('digital', 'Digital'),
        ('nft', 'NFT')
    ]
    type = models.CharField(max_length=20, choices=ART_TYPES)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.description


class File(models.Model):
    art = models.ForeignKey(ArtPost, on_delete=models.CASCADE, null=False)
    file = models.ImageField(upload_to='art_posts/')


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    art = models.ForeignKey(ArtPost, on_delete=models.CASCADE, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_user1', null=False)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_user2', null=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)


class Message(models.Model):
    msg = models.TextField()
    fk_sender = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    fk_msg = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art = models.ForeignKey(ArtPost, on_delete=models.CASCADE)
    review = models.TextField(max_length=600)
    timestamp = models.DateTimeField(auto_now_add=True)


class SubscriberList(models.Model):
    email = models.EmailField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart({self.user.username})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    art_post = models.ForeignKey(ArtPost, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.art_post.title} ({self.quantity})"


class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=4)
    cvv = models.CharField(max_length=3)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name
