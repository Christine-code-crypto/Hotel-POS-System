from django.urls import path
from .import views
from .views import generate_popular_rooms_pdf 

#app_name = 'HotelApp'  # Add this line to define the namespace

urlpatterns = [
    path('', views.Home,name="Home"),
    path('all', views.all),
    path('OnlineBooking/<int:user_id>/', views.OnlineBooking, name='OnlineBooking'),
    path('Aothur_login', views.Aothur_login, name='Aothur_login'),
    path('auth_logout', views.auth_logout, name='auth_logout'),
    path('Aothur_Reg', views.Aothur_Reg, name='Aothur_Reg'),
    path('Aothur_Fotpass', views.Aothur_Fotpass, name='Aothur_Fotpass'),
    path('all_admin', views.all_admin),
    path('Adminpage', views.Admin, name='Adminpage'),
    path('Addemployee', views.Addemployee, name='Addemployee'),
    path('Editemployee/<id>', views.Editemployee, name='Editemployee'),
    path('Allemployee', views.Allemployee, name='Allemployee'),
    path('online_Booking_info', views.online_Booking_info, name='online_Booking_info'),
    path('Edit_online_Booking/<id>', views.Edit_online_Booking, name='Edit_online_Booking'),
    path('AddCustomer', views.AddCustomer, name='AddCustomer'),
    path('AllCustomer', views.AllCustomer, name='AllCustomer'),
    path('EditCustomer/<id>', views.EditCustomer, name='EditCustomer'),
    path('delete/<id>', views.Delete, name='delete'),
    path('Search', views.Search, name='Search'),
    path('AddCustpage_Delete/<id>', views.AddCustpage_Delete, name='AddCustpage_Delete'),
    path('AllCustpage_Delete/<id>', views.AllCustpage_Delete, name='AllCustpage_Delete'),
    path('AddEmplopage_Delete/<id>', views.AddEmplopage_Delete, name='AddEmplopage_Delete'),
    path('Add_Employee_Search', views.Add_Employee_Search, name='Add_Employee_Search'),
    path('AllEmployee_Delete/<id>', views.AllEmployee_Delete, name='AllEmployee_Delete'),
    path('Add_room', views.Add_room, name='Add_room'),
    path('Add_Room_Search', views.Add_Room_Search, name='Add_Room_Search'),
    path('AddRooms_Delete/<id>', views.AddRooms_Delete, name='AddRooms_Delete'),
    path('EditRooms/<id>', views.EditRooms, name='EditRooms'),
    path('All_Room', views.All_Room, name='All_Room'),
    path('AllRooms_Delete/<id>', views.AllRooms_Delete, name='AllRooms_Delete'),
    path('AddEmployeeSalary', views.AddEmployeeSalary, name='AddEmployeeSalary'),
    path('EmployeeShow', views.EmployeeShow, name='EmployeeShow'),


    path('inventory/', views.inventory_management, name='inventory_management'),
    path('inventory/add/', views.add_inventory_item, name='add_inventory_item'),
    path('inventory/update/<int:item_id>/', views.update_inventory_item, name='update_inventory_item'),
    path('inventory/delete/<int:item_id>/', views.delete_inventory_item, name='delete_inventory_item'),

    # URL for placing an order (either room service or table service)
    path('place_order/<int:user_id>/', views.place_order, name='place_order'),

    # URL for updating the order status
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),

    # URL for managing the inventory
    path('manage_inventory/', views.manage_inventory, name='manage_inventory'),

    path('order_success/', views.order_success, name='order_success'),

    path('generate_invoice/<int:reservation_id>/', views.generate_invoice, name='generate_invoice'),
    path('process_payment/<int:invoice_id>/', views.process_payment, name='process_payment'),
    path('report/occupancy/', views.generate_occupancy_report, name='generate_occupancy_report'),
    path('report/revenue/', views.generate_revenue_report, name='generate_revenue_report'),
    path('report/popular-rooms/pdf/', generate_popular_rooms_pdf, name='popular-rooms-pdf'),

    path('payment/<int:invoice_id>/', views.payment_page, name='payment_page'),
    path('payment/success/', views.payment_success_page, name='payment_success_page'),
    path('payment/failure/', views.payment_failure_page, name='payment_failure_page'),
    
]