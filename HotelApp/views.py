from django.shortcuts import render,redirect
import sqlite3
from django.contrib.auth import authenticate,logout,login as auth_login
from .import models
from .forms import Online_Booking_form,offline_Booking_form,Add_Employee_form,Add_Room_form,Add_salary_form
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import Add_Room, Online_Booking, Payment
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from .models import MenuItem, RestaurantOrder, OrderItem, Add_Room, Inventory

from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from io import BytesIO
from django.utils.dateparse import parse_date
from django.utils.dateparse import parse_date
from django.db.models import Sum, Count
from .models import Reservation, Add_Room, Invoice  # Import the Reservation model
from django.template.loader import get_template


def generate_occupancy_report(request):
    # Fetch reservations from the database
    from .models import Reservation
    reservations = Reservation.objects.all()

    # Render the HTML template with context
    html = render_to_string('occupancy_report.html', {'reservations': reservations})

    # Convert HTML to PDF
    buffer = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=buffer)
    
    # Check for errors
    if pdf.err:
        return HttpResponse("Error generating PDF")

    # Get PDF data from buffer
    pdf_data = buffer.getvalue()
    buffer.close()

    # Create a response to serve the PDF file
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="occupancy_report.pdf"'
    return response

def generate_revenue_report(request):
    # Define the date range for the report
    start_date = parse_date(request.GET.get('start_date', '2024-01-01'))
    end_date = parse_date(request.GET.get('end_date', '2024-12-31'))
    
    # Fetch orders within the date range
    orders = RestaurantOrder.objects.filter(created_at__range=[start_date, end_date])
    
    # Calculate total revenue
    total_revenue = sum(order.total_price for order in orders)

    # Render the HTML template with context
    html = render_to_string('revenue_report.html', {
        'orders': orders,
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': total_revenue,
    })

    # Convert HTML to PDF
    buffer = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=buffer)
    
    # Check for errors
    if pdf.err:
        return HttpResponse("Error generating PDF")

    # Get PDF data from buffer
    pdf_data = buffer.getvalue()
    buffer.close()

    # Create a response to serve the PDF file
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="revenue_report.pdf"'
    return response

def generate_popular_rooms_pdf(request):
    # Annotate rooms with the number of reservations
    rooms = Add_Room.objects.annotate(
        num_reservations=Count('reservations')
    ).order_by('-num_reservations')
    
    # Load the HTML template
    template_path = 'popular_rooms_report.html'
    context = {'rooms': rooms}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="popular_rooms_report.pdf"'
    
    # Render the HTML to a string
    template = get_template(template_path)
    html = template.render(context)
    
    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Check for errors
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response


@login_required
def check_in(request, booking_id):
    booking = models.Online_Booking.objects.get(Id=booking_id)
    room = models.Add_Room.objects.get(Room_Number=booking.Select_Room)
    
    if room.status == 'Available':
        room.status = 'Occupied'
        room.save()
        booking.Check_in = datetime.now()
        booking.save()
        return HttpResponse('Check-in successful')
    else:
        return HttpResponse('Room is not available for check-in')


@login_required
def check_out(request, booking_id):
    booking = models.Online_Booking.objects.get(Id=booking_id)
    room = models.Add_Room.objects.get(Room_Number=booking.Select_Room)
    
    if room.status == 'Occupied':
        room.status = 'Available'
        room.save()
        booking.Check_out = datetime.now()
        booking.save()
        return HttpResponse('Check-out successful')
    else:
        return HttpResponse('Room was not occupied')






# Create your views here.
def Home(request):
    return render(request,'Home.html')
def all(request):
    return render(request,'allinclude.html')

from django.utils import timezone
from datetime import timedelta
from .models import Add_Room, Online_Booking

from django.utils import timezone
from datetime import timedelta
from .models import Add_Room, Online_Booking
from django.http import HttpResponse
from django.shortcuts import render, redirect

@login_required
def OnlineBooking(request, user_id):
    if request.method == 'POST':
        # Get the uploaded image
        upload_image = request.FILES.get('Img')

        # Get the selected room from the form
        selected_room_number = request.POST.get('Select_Room')

        if not selected_room_number:
            return HttpResponse('Room number is missing.')

        # Check if the room is available
        try:
            room = Add_Room.objects.get(Room_Number=selected_room_number)
        except Add_Room.DoesNotExist:
            return HttpResponse(f'No room found with number {selected_room_number}.')

        if room.status != 'Available':
            return HttpResponse(f'Room {room.Room_Number} is not available for booking.')

        # Initialize the Online_Booking model
        booking = Online_Booking()

        # Automatically set check-in time to current date and time
        check_in = timezone.now()

        # Get the stay duration from the user input (or default to 1 night)
        stay_duration = int(request.POST.get('stay_duration', 1))

        # Calculate the check-out date based on stay duration
        check_out = check_in + timedelta(days=stay_duration)

        # Populate booking details
        booking.Check_in = check_in
        booking.Check_out = check_out
        booking.ADULT = request.POST.get('ADULT')
        booking.CHILDREN = request.POST.get('CHILDREN')
        booking.Name = request.POST.get('Name')
        booking.Surname = request.POST.get('Surname')
        booking.Email = request.POST.get('Email')
        booking.Phone_Number = request.POST.get('Phone_Number')
        booking.Nid_No = request.POST.get('Nid_No')
        booking.City = request.POST.get('City')
        booking.Country = request.POST.get('Country')
        booking.Img = upload_image
        booking.Address = request.POST.get('Address')
        booking.Date = request.POST.get('Date')
        booking.Time = request.POST.get('Time')

        # Assign selected room to booking
        booking.Select_Room = room.Room_Number

        # Ensure that the logged-in user's ID matches the URL parameter
        if request.user.id == user_id:
            booking.user = request.user
        else:
            return HttpResponse("You are not authorized to make this booking.")

        # Save the booking
        booking.save()

        # Update room status to "Occupied"
        room.status = 'Occupied'
        room.save()

        return redirect('place_order', user_id=request.user.id)


    # If GET request, display available rooms only
    available_rooms = Add_Room.objects.filter(status='Available')
    return render(request, 'online_booking_page.html', {'available_rooms': available_rooms})




def Aothur_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            # Check user group
            if user.groups.filter(name='Admin').exists():
                return redirect('Adminpage')  # Redirect to the admin page
            else:
                return redirect('OnlineBooking', user_id=user.id)  # Redirect to the online booking page with user_id
        else:
            return HttpResponse('Invalid username or password')
    return render(request, 'Athur_login_page.html')


@login_required
def auth_logout(request):
    logout(request)
    return redirect('Home')



#right one
def Aothur_Reg(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('Aothur_login')
        else:
            print(form.errors)  # Log form errors
    else:
        form = CustomUserCreationForm()
    return render(request, 'Athur_Register_Page.html', {'form': form})

def Aothur_Fotpass(request):
    return render(request,'Author_forgetpass_page.html')

def all_admin(request):
    return render(request,'admin/AdminAllinclude.html')

@login_required
@permission_required('HotelApp.view_online_booking', raise_exception=True)
def Admin(request):
    data = models.Online_Booking.objects.all().order_by('-Id')
    return render(request,'admin/Admin.html',{'data':data})

@login_required
@permission_required('HotelApp.add_add_employee', raise_exception=True)
@permission_required('HotelApp.change_add_employee', raise_exception=True)
@permission_required('HotelApp.delete_add_employee', raise_exception=True)
@permission_required('HotelApp.view_add_employee', raise_exception=True)
def Addemployee(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Upload_Image')
        # fname = upload_image.name
        # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
        #     for ch in upload_image.chunks():
        #         location.write(ch)
        if request.method == 'POST':
            Data = models.Add_Employee()
            Data.Employee_Id = request.POST.get('Employee_Id')
            Data.First_Name = request.POST.get('First_Name')
            Data.Last_Name = request.POST.get('Last_Name')
            Data.Email = request.POST.get('Email')
            Data.Mobile_Number = request.POST.get('Mobile_Number')
            Data.Joining_Date = request.POST.get('Joining_Date')
            Data.Dateof_Birth = request.POST.get('Dateof_Birth')
            Data.Departments = request.POST.get('Departments')
            Data.Gender = request.POST.get('Gender')
            Data.Blood_Group = request.POST.get('Blood_Group')
            Data.Education = request.POST.get('Education')
            Data.Personal_Identity = request.POST.get('Personal_Identity')
            Data.Guardian = request.POST.get('Guardian')
            Data.Guardian_Number = request.POST.get('Guardian_Number')
            Data.Upload_Image = upload_image
            Data.Address = request.POST.get('Address')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('Addemployee')
        else:
            return HttpResponse("Failed")

    data = models.Add_Employee.objects.all().order_by('-Employee_Id')
    return render(request,'admin/addemployee.html',{'data':data})

@login_required
@permission_required('HotelApp.change_add_employee', raise_exception=True)  
def Editemployee(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    if request.method == 'POST':
        data = Add_Employee_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Upload_Image')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('Allemployee')
        else:
            return HttpResponse("Failed")

    select = data.Departments
    if select == 'Departments':
        select = 1
    elif select == 'Housekeeping':
        select = 2
    elif select == 'Manager':
        select = 3
    elif select == 'Chef':
        select = 4
    elif select == 'Food and Beverage':
        select = 5
    elif select == 'Kitchen':
        select = 6
    elif select == 'Security':
        select = 7
    else:
        select = 8

    select = data.Gender
    if select == 'Gender':
        select = 1
    elif select == 'MALE':
        select = 2
    else:
        select = 3

    return render(request,'admin/Editemployee.html',{'data': data,"select": select})

def Allemployee(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Add_Employee.objects.filter(Employee_Id=Serch) or models.Add_Employee.objects.filter(First_Name=Serch)
        return render(request, 'admin/allemployee.html', {"data": data})
    data = models.Add_Employee.objects.all().order_by('-Employee_Id')
    return render(request,'admin/allemployee.html',{'data': data})


def online_Booking_info(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        show = models.Online_Booking.objects.filter(Country =Serch) or models.Online_Booking.objects.filter(Name=Serch)
        return render(request,'admin/Online_Booking.html',{"data":show})

    data = models.Online_Booking.objects.all().order_by('-Id')
    return render(request,'admin/Online_Booking.html',{'data':data})


def Edit_online_Booking(request,id):
    data = models.Online_Booking.objects.get(Id=id)
    if request.method == 'POST':
        data = Online_Booking_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Img')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('online_Booking_info')
        else:
            return HttpResponse("Failed")

    select = data.ADULT
    if select == 'ADULT':
        select = 1
    elif select == '1 ADULT':
        select = 2
    elif select == '2 ADULT':
        select = 3
    elif select == '3 ADULT':
        select = 4
    else:
        select = 5

    select = data.CHILDREN
    if select == 'CHILDREN':
        select = 1
    elif select == '1 CHILDREN':
        select = 2
    elif select == '2 CHILDREN':
        select = 3
    elif select == '3 CHILDREN':
        select = 4
    else:
        select = 5
    return render(request,'admin/EditonlineBooking.html',{'data': data,"select":select})

@login_required
def AddCustomer(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Upload_Image')
        # fname = upload_image.name
        # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
        #     for ch in upload_image.chunks():
        #         location.write(ch)
        if request.method == 'POST':
            Data = models.Offline_Booking()
            Data.Customer_Id = request.POST.get('Customer_Id')
            Data.Check_in = request.POST.get('Check_in')
            Data.Check_out = request.POST.get('Check_out')
            Data.First_Name = request.POST.get('First_Name')
            Data.Last_Name = request.POST.get('Last_Name')
            Data.Email = request.POST.get('Email')
            Data.Mobile_Number = request.POST.get('Mobile_Number')
            Data.ADULT = request.POST.get('ADULT')
            Data.CHILDREN = request.POST.get('CHILDREN')
            Data.Total_Person = request.POST.get('Total_Person')
            Data.Select_Room = request.POST.get('Select_Room')
            Data.Room_Number = request.POST.get('Room_Number')
            Data.Gender = request.POST.get('Gender')
            Data.Personal_Identity = request.POST.get('Personal_Identity')
            Data.Upload_Image = upload_image
            Data.Country = request.POST.get('Country')
            Data.Address = request.POST.get('Address')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('AddCustomer')
        else:
            return HttpResponse("Failed")

    data = models.Offline_Booking.objects.all().order_by('-Customer_Id')
    return render(request,'admin/AddCustomer.html',{'data': data})

@login_required
def AllCustomer(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Offline_Booking.objects.filter(First_Name=Serch) or models.Offline_Booking.objects.filter( Email=Serch)
        return render(request, 'admin/AllCustomer.html', {"data": data})
    data = models.Offline_Booking.objects.all().order_by('-Customer_Id')
    return render(request,'admin/AllCustomer.html',{'data': data})


def EditCustomer(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    if request.method == 'POST':
        data = offline_Booking_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Upload_Image')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('AllCustomer')
        else:
            return HttpResponse("Failed")

    select = data.ADULT
    if select == 'ADULT':
        select = 1
    elif select == '1 ADULT':
        select = 2
    elif select == '2 ADULT':
        select = 3
    elif select == '3 ADULT':
        select = 4
    else:
        select = 5

    select = data.CHILDREN
    if select == 'CHILDREN':
        select = 0
    elif select == '1 CHILDREN':
        select = 1
    elif select == '2 CHILDREN':
        select = 2
    elif select == '3 CHILDREN':
        select = 3
    else:
        select = 4

    select = data.Select_Room
    if select == 'Select Room':
        select = 1
    elif select == 'Delux':
        select = 2
    elif select == 'Super Delux':
        select = 3
    elif select == 'Single':
        select = 4
    else:
        select = 5

    select = data.Room_Number
    if select == 'Room Number':
        select = 1
    elif select == 'Room101':
        select = 2
    elif select == 'Room102':
        select = 3
    elif select == 'Room103':
        select = 4
    else:
        select = 5

    select = data.Gender
    if select == 'Gender':
        select = 1
    elif select == 'MALE':
        select = 2
    else:
        select = 3

    return render(request,'admin/EditCustomer.html',{'data': data,"select": select})


def Delete(request,id):
    data = models.Online_Booking.objects.get(Id=id)
    data.delete()
    return redirect('online_Booking_info')

def Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        data = models.Offline_Booking.objects.filter(First_Name=Serch) or models.Offline_Booking.objects.filter(Email=Serch)
        return render(request, 'admin/AddCustomer.html', {"data": data})

def AddCustpage_Delete(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    data.delete()
    return redirect('AddCustomer')


def AllCustpage_Delete(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    data.delete()
    return redirect('AllCustomer')

def AddEmplopage_Delete(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    data.delete()
    return redirect('Addemployee')

def Add_Employee_Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        data = models.Add_Employee.objects.filter(Employee_Id=Serch) or models.Add_Employee.objects.filter(First_Name=Serch)
        return render(request,'admin/addemployee.html', {"data": data})

def AllEmployee_Delete(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    data.delete()
    return redirect('Allemployee')


def Add_room(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Room_Image')
        # fname = upload_image.name
        # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
        #     for ch in upload_image.chunks():
        #         location.write(ch)
        if request.method == 'POST':
            Data = models.Add_Room()
            Data.Room_Number = request.POST.get('Room_Number')
            Data.Room_Type = request.POST.get('Room_Type')
            Data.Room_Price = request.POST.get('Room_Price')
            Data.Room_Image = upload_image
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.status = request.POST.get('status')
            Data.save()
            return redirect('Add_room')
        else:
            return HttpResponse("Failed")

    data = models.Add_Room.objects.all().order_by('-Room_Number')
    return render(request, 'admin/AddRoom.html',{'data': data})

def Add_Room_Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        data = models.Add_Room.objects.filter(Room_Number=Serch) or models.Add_Rooms.objects.filter(Room_Type=Serch)
        return render(request, 'admin/AddRoom.html',{"data": data})

def AddRooms_Delete(request,id):
    data = models.Add_Room.objects.get(Id=id)
    data.delete()
    return redirect('Add_room')

def EditRooms(request,id):
    data = models.Add_Room.objects.get(Id=id)
    if request.method == 'POST':
        form = Add_Room_form(request.POST, request.FILES, instance=data)
        if form.is_valid():
            # upload_image = request.FILES.get('Room_Image')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            form.save()
            return redirect('All_Room')
        else:
            return HttpResponse("Failed")

    
    # Define room types and status choices
    ROOM_TYPES = dict(models.Add_Room.ROOM_TYPES)
    ROOM_STATUS = dict(models.Add_Room.ROOM_STATUS)
    ROOM_NUMBERS = [
        ('Room Number', 'Room Number'),
        ('Room101', 'Room101'),
        ('Room102', 'Room102'),
        ('Room103', 'Room103'),
        ('Room104', 'Room104'),
        ('Room105', 'Room105'),
        ('Room106', 'Room106')
    ]

    context = {
        'data': data,
        'ROOM_TYPES': ROOM_TYPES,
        'ROOM_STATUS': ROOM_STATUS,
        'ROOM_NUMBERS': ROOM_NUMBERS
    }

    

    return render(request, 'admin/EditRooms.html', context)

def All_Room(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Add_Room.objects.filter(Room_Number=Serch) or models.Add_Room.objects.filter(Room_Type=Serch)
        return render(request, 'admin/AllRooms.html',{"data": data})

    data = models.Add_Room.objects.all().order_by('-Id')
    return render(request, 'admin/AllRooms.html',{'data': data})

def AllRooms_Delete(request,id):
    data = models.Add_Room.objects.get(Id=id)
    data.delete()
    return redirect('All_Room')

@login_required
def AddEmployeeSalary(request):
    if request.method == 'POST':
        if request.method == 'POST':
            Data = models.Add_Salarys()
            Data.Employee_Id = request.POST.get('Employee_Id')
            Data.Employee_Name = request.POST.get('Employee_Name')
            Data.Email = request.POST.get('Email ')
            Data.Mobile_Number = request.POST.get('Mobile_Number')
            Data.Departments = request.POST.get('Departments')
            Data.Salary = request.POST.get('Salary')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('AddEmployeeSalary')
        else:
            return HttpResponse("Failed")

    return render(request, 'admin/AddEmployeeSalary.html')

def EmployeeShow(request):

    return render(request, 'admin/EmployeeShow.html')

# View to place an order (for room or table)



def place_order(request, user_id):
    # Fetch the user based on the passed user_id
    user = get_object_or_404(User, id=user_id)
    
    if not user.is_authenticated:
        return HttpResponse("You need to be logged in to place an order.")

    if request.method == 'POST':
        order = None  # Initialize the order object

        if 'room_number' in request.POST:
            room_number = request.POST.get('room_number').strip()
            room_number_with_prefix = f"Room{room_number}"
            try:
                room = Add_Room.objects.get(Room_Number=room_number_with_prefix)
                order = RestaurantOrder(order_type="Room Service", room_number=room, user=user)
            except Add_Room.DoesNotExist:
                return HttpResponse(f'Room number "{room_number_with_prefix}" does not exist.')

        elif 'table_number' in request.POST:
            table_number = request.POST.get('table_number').strip()
            order = RestaurantOrder(order_type="Table Service", table_number=table_number, user=user)

        if order:
            order.save()

            total_price = 0
            for item_id, quantity in request.POST.items():
                if item_id.startswith('item_'):
                    menu_item_id = item_id.split('_')[1]
                    menu_item = MenuItem.objects.get(id=menu_item_id)

                    try:
                        quantity = int(quantity.strip())
                    except ValueError:
                        quantity = 0

                    if menu_item.stock >= quantity:
                        order_item = OrderItem(order=order, menu_item=menu_item, quantity=quantity)
                        total_price += menu_item.price * quantity
                        menu_item.stock -= quantity
                        order_item.save()
                        menu_item.save()
                    else:
                        return HttpResponse(f"Insufficient stock for {menu_item.name}.")

            order.total_price = total_price
            order.save()

            return redirect('order_success')

    menu_items = MenuItem.objects.all()
    return render(request, 'place_order.html', {'menu_items': menu_items, 'user': user})




# View to manage order status
@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(RestaurantOrder, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [status[0] for status in RestaurantOrder.ORDER_STATUS]:
            order.status = new_status
            order.save()
            return redirect('order_detail', order_id=order.id)
    
    return render(request, 'update_order_status.html', {'order': order})

# View to manage inventory
@login_required
def manage_inventory(request):
    inventory_items = Inventory.objects.all()

    if request.method == 'POST':
        for item in inventory_items:
            new_quantity = request.POST.get(f'quantity_{item.id}')
            if new_quantity:
                item.quantity = int(new_quantity)
                item.save()

    return render(request, 'manage_inventory.html', {'inventory_items': inventory_items})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory

# View to display the inventory management page
def inventory_management(request):
    inventory_items = Inventory.objects.all()
    return render(request, 'inventory_management.html', {'inventory_items': inventory_items})

# View to handle adding a new inventory item
def add_inventory_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        quantity = request.POST['quantity']
        price = request.POST['price']
        Inventory.objects.create(name=name, quantity=quantity, price=price)
        return redirect('inventory_management')

# View to handle updating an inventory item
def update_inventory_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Inventory, id=item_id)
        new_quantity = request.POST['quantity']
        item.quantity = new_quantity
        item.save()
        return redirect('inventory_management')

# View to handle deleting an inventory item
def delete_inventory_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Inventory, id=item_id)
        item.delete()
        return redirect('inventory_management')


def order_success(request):
    return render(request, 'order_success.html')


def generate_invoice(request, reservation_id):
    # Fetch reservation details
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    # Calculate room charge (assuming total_price already contains room charges)
    room_charge = reservation.total_price
    
    # Fetch restaurant order, if any
    restaurant_order = RestaurantOrder.objects.filter(room_number=reservation.room).first()
    restaurant_charge = restaurant_order.total_price if restaurant_order else 0.00
    
    # Add additional services if needed
    additional_services = 50.00  # Example additional services charge
    
    # Calculate total amount
    total_amount = room_charge + Decimal(restaurant_charge) + Decimal(additional_services)
    
    # Create and save invoice
    invoice = Invoice.objects.create(
        reservation=reservation,
        room_charge=room_charge,
        restaurant_order=restaurant_order,
        additional_services=additional_services,
        total_amount=total_amount,
        payment_method="Pending",
        payment_status="Pending"
    )
    
    return render(request, 'billing-invoice.html', {'invoice': invoice})

def process_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        # Get payment details from form
        payment_method = request.POST['payment_method']
        amount_paid = invoice.total_amount
        
        # Create payment record
        payment = Payment.objects.create(
            invoice=invoice,
            amount_paid=amount_paid,
            payment_method=payment_method
        )
        
        # Mark invoice as paid
        invoice.payment_status = 'Paid'
        invoice.payment_method = payment_method
        invoice.save()
        
        return HttpResponse("Payment successful!")
    
    return render(request, 'billing-payment.html', {'invoice': invoice})



@login_required
def payment_page(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id, payment_status='Pending')
    except Invoice.DoesNotExist:
        # Handle the case where the invoice does not exist or is already paid
        return HttpResponse('Page does not exist', status=404)

    if request.method == 'POST':
        # Handle the form submission to process payment
        payment_method = request.POST.get('payment_method')
        # Add your logic to handle payment here, including integration with Mpesa or PayPal
        # Example: payment_response = process_payment(payment_method, invoice.total_amount)
        # On success:
        Payment.objects.create(
            invoice=invoice,
            amount_paid=invoice.total_amount,
            payment_method=payment_method,
        )
        invoice.payment_status = 'Paid'
        invoice.save()
        return redirect('payment_success_page')

    return render(request, 'payment_page.html', {'invoice': invoice})

def payment_success_page(request):
    return render(request, 'payment_success.html')

def payment_failure_page(request):
    return render(request, 'payment_failure.html')

