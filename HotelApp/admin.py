from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from .models import Online_Booking, Offline_Booking, Add_Employee, Add_Room, Add_Salarys, MenuItem, RestaurantOrder, OrderItem, Inventory, Reservation,Invoice, Payment


admin.site.unregister(User)
admin.site.register(User, UserAdmin)



@admin.register(Online_Booking)
class Online_BookingAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Surname', 'Check_in', 'Check_out', 'City', 'Country', 'Date', 'Time')
    search_fields = ('Name', 'Surname', 'Email')
    list_filter = ('City', 'Country', 'Date')

@admin.register(Offline_Booking)
class Offline_BookingAdmin(admin.ModelAdmin):
    list_display = ('First_Name', 'Last_Name', 'Check_in', 'Check_out', 'Select_Room', 'Country', 'Date', 'Time')
    search_fields = ('First_Name', 'Last_Name', 'Email')
    list_filter = ('Country', 'Select_Room', 'Date')

@admin.register(Add_Employee)
class Add_EmployeeAdmin(admin.ModelAdmin):
    list_display = ('Employee_Id', 'First_Name', 'Last_Name', 'Email', 'Mobile_Number', 'Departments', 'Date', 'Time')
    search_fields = ('First_Name', 'Last_Name', 'Email', 'Employee_Id')
    list_filter = ('Departments', 'Date', 'Time')

@admin.register(Add_Room)
class Add_RoomAdmin(admin.ModelAdmin):
    list_display = ('Room_Number', 'Room_Type', 'Room_Price', 'Date', 'Time')
    search_fields = ('Room_Number', 'Room_Type')
    list_filter = ('Room_Type', 'Date')

@admin.register(Add_Salarys)
class Add_SalarysAdmin(admin.ModelAdmin):
    list_display = ('Employee_Id', 'Employee_Name', 'Mobile_Number', 'Email', 'Departments', 'Salary', 'Date', 'Time')
    search_fields = ('Employee_Name', 'Email', 'Employee_Id')
    list_filter = ('Departments', 'Salary', 'Date')

# Registering the new models
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('price', 'stock')

@admin.register(RestaurantOrder)
class RestaurantOrderAdmin(admin.ModelAdmin):
    list_display = ('order_type', 'room_number', 'table_number', 'status', 'total_price', 'created_at', 'updated_at')
    search_fields = ('room_number__Room_Number', 'table_number')
    list_filter = ('order_type', 'status', 'created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity')
    search_fields = ('order__id', 'menu_item__name')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')
    search_fields = ('item__name',)
    list_filter = ('quantity',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'guest_email', 'guest_phone', 'room', 'check_in', 'check_out', 'adults', 'children', 'total_price', 'payment_status', 'date_created')
    search_fields = ('guest_name', 'guest_email', 'guest_phone', 'room__Room_Number')
    list_filter = ('payment_status', 'check_in', 'check_out')
    date_hierarchy = 'date_created'


# Invoice Admin
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'room_charge', 'restaurant_order', 'additional_services', 'total_amount', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('reservation__id',)
    list_filter = ('payment_method', 'payment_status', 'created_at')
    date_hierarchy = 'created_at'

# Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount_paid', 'payment_method', 'payment_date')
    search_fields = ('invoice__id',)
    list_filter = ('payment_method',)
    date_hierarchy = 'payment_date'






