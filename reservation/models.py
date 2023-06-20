from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Tabella Ristorante

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100, null=True, blank=True)
    quarter = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    opening_hours = models.CharField(max_length=100)
    cuisine_type = models.CharField(max_length=100, null=True, blank=True)
    restaurant_type = models.CharField(max_length=100, null=True, blank=True)
    number_of_rooms = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
    
# Tabella Tavoli (Chiave esterna Tabella Ristorante)

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE) # SE IL RISTORANTE VIENE ELIMINATO, VIENE ELIMINATO ANCHE IL TAVOLO
    table_number = models.CharField(max_length=20) 
    capacity = models.IntegerField() # Posti a sedere massimi per il tavolo
    is_available = models.BooleanField(default=True)  # Indica se il tavolo è disponibile per prenotazioni
    description = models.TextField(blank=True, null=True)  # Descrizione del tavolo
    location = models.CharField(max_length=100, blank=True, null=True)  # Posizione del tavolo nel ristorante (es. "Interno", "Esterno")
    is_private = models.BooleanField(default=True)  # Indica se il tavolo è privato o condiviso
    image = models.ImageField(upload_to='table_images/', blank=True, null=True)  # Immagine del tavolo

    def __str__(self):
        return f"Table {self.table_number} - Capacity: {self.capacity} - Description {self.description}"
    
# Tabella Menù (Chiave esterna Tabella Ristorante)

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

# Tabella Customer

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    telephone_number = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.user.username
    
# Tabella Reservation (chiave esterna tabella Ristorante)
    
class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    num_of_guests = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.customer_name} - {self.reservation_date} {self.reservation_time}"

# Tabella Ordinazioni

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_time = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer} - {self.menu_item} - {self.quantity}x"

    class Meta:
        verbose_name_plural = "Orders"

# Tabella Pagamenti

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order: {self.order}"

    class Meta:
        verbose_name_plural = "Payments"

# Tabella Recensioni

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.restaurant} by {self.customer}"
    
# Tabella Promozioni

class Promotion(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title
    
# Tabella Programma Fedeltà

class LoyaltyProgram(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.PositiveIntegerField()

    def __str__(self):
        return self.name






    

