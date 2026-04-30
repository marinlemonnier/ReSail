from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.title
    
class TradeType(models.Model):
    type = models.CharField(max_length=50, unique=True)  # Exemple: Selling, Giving away
    def __str__(self):
        return self.type        

class Status(models.Model):
    status = models.CharField(max_length=50, unique=True) # Exemple disponible, réservé, vendu
    def __str__(self):
        return self.status

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Relation Many-to-One vers User
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='NOK')
    item_quality = models.CharField(max_length=100)
    date_publication = models.DateTimeField(auto_now_add=True)

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100, null=True, blank=True)
    
    trade_type = models.ForeignKey(TradeType, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class ItemImage(models.Model): # Support multi-images (One-to-Many)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='items/') # Pour les photos des annonces