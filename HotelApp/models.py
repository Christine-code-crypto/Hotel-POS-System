from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from datetime import datetime
from django.utils import timezone

# Create your models here.


class Online_Booking(models.Model):
    Id = models.AutoField(primary_key=True)
    Check_in = models.DateField()
    Check_out = models.DateField()
    ADULT = models.CharField(max_length=255)
    CHILDREN = models.CharField(max_length=255)
    Name = models.CharField(max_length=255)
    Surname = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    Phone_Number = models.IntegerField()
    City = models.CharField(max_length=255)
    Country = models.CharField(max_length=255)
    Img = models.ImageField(upload_to='')
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.Name
    class Meta:
        db_table = 'Online_Booking_table'

class Offline_Booking(models.Model):
    Customer_Id = models.AutoField(primary_key=True)
    Check_in = models.CharField(max_length=255)
    Check_out = models.CharField(max_length=255)
    First_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    Mobile_Number = models.IntegerField()
    ADULT = models.CharField(max_length=255)
    CHILDREN = models.CharField(max_length=255)
    Total_Person = models.IntegerField()
    Select_Room = models.CharField(max_length=255)
    Room_Number = models.CharField(max_length=255)
    Gender = models.CharField(max_length=255)
    Personal_Identity = models.CharField(max_length=255)
    Upload_Image = models.ImageField(upload_to='')
    Country = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.First_Name
    class Meta:
        db_table = 'Offline_Booking_Customer'


class Add_Employee(models.Model):
    Employee_Id = models.CharField(max_length=255,primary_key=True)
    First_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    Email = models.CharField(max_length=255,unique=True)
    Mobile_Number = models.IntegerField(unique=True)
    Joining_Date = models.CharField(max_length=255)
    Dateof_Birth = models.CharField(max_length=255)
    Departments = models.CharField(max_length=255)
    Gender = models.CharField(max_length=255)
    Blood_Group = models.CharField(max_length=255)
    Education = models.CharField(max_length=255)
    Personal_Identity = models.CharField(max_length=255,unique=True)
    Guardian = models.CharField(max_length=255)
    Guardian_Number = models.IntegerField()
    Upload_Image = models.ImageField(upload_to='')
    Address = models.CharField(max_length=255)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.First_Name
    class Meta:
        db_table = 'Add_Employees'

class Add_Room(models.Model):

    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    ]

    ROOM_STATUS = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Maintenance', 'Maintenance'),
    ]

    Id = models.AutoField(primary_key=True)
    Room_Number = models.CharField(max_length=10, unique=True)
    Room_Type = models.CharField(max_length=10, choices=ROOM_TYPES)
    Room_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Room_Image = models.ImageField(upload_to='')
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=ROOM_STATUS, default='Available')
    def __str__(self):
        return f"Room {self.Room_Number} ({self.Room_Type})"
    class Meta:
        db_table = 'Add_Room'

class Add_Salarys(models.Model):
    Employee_Id = models.ForeignKey(Add_Employee,on_delete=models.CASCADE)
    Employee_Name = models.CharField(max_length=255)
    Mobile_Number = models.CharField(max_length=255)
    Email = models.CharField(max_length=500)
    Departments = models.CharField(max_length=255)
    Salary = models.CharField(max_length=255)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.Employee_Id
    class Meta:
        db_table = 'Add_Employee_salarys'




class Reservation(models.Model):
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=15)
    room = models.ForeignKey('Add_Room', on_delete=models.CASCADE, related_name='reservations')  # Added related_name
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.IntegerField()
    children = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')])
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Reservation by {self.guest_name} for Room {self.room.Room_Number}'

# Model for Restaurant Menu Items
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)  # For inventory tracking

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class RestaurantOrder(models.Model):
    ROOM_SERVICE = 'Room Service'
    TABLE_SERVICE = 'Table Service'
    ORDER_TYPES = [
        (ROOM_SERVICE, 'Room Service'),
        (TABLE_SERVICE, 'Table Service'),
    ]

    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    ORDER_STATUS = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    order_type = models.CharField(max_length=50, choices=ORDER_TYPES)
    room_number = models.ForeignKey('Add_Room', on_delete=models.SET_NULL, null=True, blank=True)  # For room service
    table_number = models.IntegerField(null=True, blank=True)  # For table service
    items = models.ManyToManyField(MenuItem, through='OrderItem')  # Many items per order
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the logged-in user

    def __str__(self):
        return f"Order {self.id} - {self.order_type} by {self.user.username}"


# Model for Order Items (to handle the quantity of each menu item)
class OrderItem(models.Model):
    order = models.ForeignKey(RestaurantOrder, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.menu_item.price * self.quantity

# Model for Restaurant Inventory
class Inventory(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.item.name} - {self.quantity} left"

PAYMENT_METHODS = [
    ('Credit Card', 'Credit Card'),
    ('Debit Card', 'Debit Card'),
    ('Cash', 'Cash'),
    ('Mobile Payment', 'Mobile Payment'),
]

class Invoice(models.Model):
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    room_charge = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Make this not editable
    restaurant_order = models.ForeignKey('RestaurantOrder', on_delete=models.SET_NULL, null=True, blank=True)
    additional_services = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # This will be calculated
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    mpesa_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    mpesa_status = models.CharField(max_length=50, blank=True, null=True)

    paypal_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    paypal_status = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically update the room charge from the reservation's room price
        self.room_charge = self.reservation.room.Room_Price

        # Calculate the total amount: room charge + additional services
        self.total_amount = self.room_charge + (self.restaurant_order.total_price if self.restaurant_order else 0) + self.additional_services

        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"Invoice for Reservation {self.reservation.id} - {self.payment_status}"


class Payment(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)  # Use the same external variable
    payment_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Payment of {self.amount_paid} for Invoice {self.invoice.id}"








    
    
    
    

    
