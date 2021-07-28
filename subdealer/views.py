from django.shortcuts import render
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from accounts.models import User, deviceTable, live_location_table, transactionTable, vehicleDetails
from .forms import CreateUserForm1, CreateUserForm2, DeviceVehicleAllocationForm, AllocateDeviceUser
from django.contrib.auth.decorators import login_required
import ast, traceback
from django.db import connections
import datetime
import time
from datetime import date
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.



@login_required
def dashboard(request):
    currentuser = request.user
    username = currentuser.username
    if(currentuser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
      # start = datetime.now()
    total_count = transactionTable.objects.filter(sold_to_id = username).count()
    sold_count = transactionTable.objects.filter(held_by = username).count()

    usercount = User.objects.filter(added_by = username,user_type = "US").count()
    
    # Renewal Date
    renewal = date.today() - datetime.timedelta(days=365)
    readyToSell = deviceTable.objects.filter(current_owner = username,activation_date__gte=renewal).count()

    #query to determine activated and deactivated device
    #active = deviceTable.objects.filter(current_owner = username,activation_date__gt=renewal).count()
    deactive_stock = deviceTable.objects.filter(current_owner = username,activation_date__lt=renewal).count()
    deactive_sold = deviceTable.objects.filter(transactiontable__held_by = username,activation_date__lt=renewal).count()

    users = User.objects.filter(added_by = username,user_type = "US").values('username','phone')[:10]

    context = {"total":total_count, "sold":sold_count,"user":usercount,"ready":readyToSell,'deactive_stock':deactive_stock,'deactive_sold':deactive_sold,"userslist" : users}
    return render(request,'subdealer/dashboard.html',context)


############################################################

@login_required
def userRegisteration(request):
    currentuser = request.user
    dealer = currentuser.username
    if(currentuser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
    if request.method =='POST':
        form1 = CreateUserForm1(request.POST)
        form2 = CreateUserForm2(request.POST)
        #print("Here1")
        if form1.is_valid() and form2.is_valid():
            
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            firstName = request.POST['first_name']
            email= request.POST['email']
            phone = request.POST['phone']
            company = request.POST['company']
            if company == '':
                company=None         
            
            # Creating User Object
            User.objects.create_user(username=username,
                                     first_name=firstName,
                                     email=email,
                                     password=password,
                                     user_type='US',
                                     added_by=dealer,
                                     phone=phone,
                                     company_details=company)
            form1 = CreateUserForm1()
            form2 = CreateUserForm2()
            context = {'form1':form1,'form2':form2,'success_message': 'User Registration Successful.'}             
            return render(request,'subdealer/add_user.html',context)

        else:
            context = {'form1':form1,'form2':form2}
            return render(request,'subdealer/add_user.html',context)

    form1 = CreateUserForm1()
    form2 = CreateUserForm2()
    context = {"status" : "",'form1':form1,'form2':form2}
    return render(request,'subdealer/add_user.html',context)

################################################################################################

@login_required
def deviceAllocationUser(request):
    currentuser=request.user
    currentusername = currentuser.username
    if(currentuser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
    if request.method =='POST':


        form = AllocateDeviceUser(request.POST)
        form2 = DeviceVehicleAllocationForm(request.POST)
        print(form.errors.as_data())
        if form.is_valid():
            #print(">>succes<<")
            userCustomer = request.POST['username'].strip()
            dateOfAllocation  = request.POST['allocate_date']
            imei = request.POST['imei']
            try:
                # print(imei)
                # print(len(imei))
                
                imei_heldBy = imei+currentusername
                try:

                    get_transaction =  transactionTable.objects.get(imei_held_by = imei_heldBy)
                    #print("Try 2:",get_transaction)
                    form = AllocateDeviceUser()
                    form2 = DeviceVehicleAllocationForm()
                    context = {"status" : "This transaction has already been made.",'form':form,'form2':form2}
                    return render(request,'subdealer/allocation_user.html',context)
                except transactionTable.DoesNotExist:
                    #print("Ex 2:")
                    #print(userCustomer)
                    transactionObj = transactionTable( sold_to_id = userCustomer,
                                                        held_by = currentusername ,
                                                        imei_held_by = imei_heldBy,
                                                        imei_id = imei ,
                                                        transaction_date = dateOfAllocation,
                                                        last_transaction = True)
                    #print(transactionObj)
                    vehicle_number = request.POST['vehicle_no'].replace(" ","")
                    try:
                        vehicleObject = vehicleDetails.objects.create(imei_id = imei,
                                                          username_id = userCustomer,
                                                          vehicle_no = vehicle_number,
                                                          installation_date = request.POST['installation_date'],
                                                          odometer = request.POST['odometer'])
                    except:
                        form = AllocateDeviceUser(request.POST)
                        form2 = DeviceVehicleAllocationForm(request.POST) 
                        _mutable = request.POST._mutable
                        request.POST._mutable = True
                        # form2.data.update(vehcile_no = "" )
                        form2.data['vehicle_no'] = None
                        print(form2.data)
                        request.POST._mutable = _mutable
                        context = {'form':form,'form2':form2, "status" : "Vehicle Number Exists"}
                        return render(request,'dealer/allocation_user.html',context)


                    deviceTable.objects.filter(imei = imei).update(current_owner_id = userCustomer)
                    
                    liveObject = live_location_table.objects.create(imei_id = imei,username_id=userCustomer)
                   


                    if(currentuser.user_type != "AD"):
                        transactionTable.objects.filter(imei =imei,sold_to = currentusername).update(last_transaction = False)
                    try:
                        vehicleObject.save()
                        liveObject.save()
                        transactionObj.save()
                    except:
                        vehicleDetails.objects.filter(vehicle_no = vehicle_number).delete()
                        transactionTable(imei_held_by = imei_heldBy).delete()
                form = AllocateDeviceUser()
                form2 = DeviceVehicleAllocationForm()
                context = {"status" : "Successfully Allocated",'form':form,'form2':form2}
                return render(request,'subdealer/allocation_user.html',context)
            except Exception as e:
                #print("Error = ",e)
                
                form = AllocateDeviceUser()
                form2 = DeviceVehicleAllocationForm()
                context = {"status" :"Invalid Transaction",'form':form,'form2':form2}
                return render(request,'subdealer/allocation_user.html',context)
            
    else:
        form = AllocateDeviceUser()
        form2 = DeviceVehicleAllocationForm()
    
    context = {'form':form,'form2':form2}
    return render(request,'subdealer/allocation_user.html',context)


#####################################################################################


@login_required
def reallocateDevice(request):
    currentuser=request.user
    currentusername = currentuser.username
    if(currentuser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
    if request.method == 'POST':       
        imei = request.POST.get('imei')
        try:
            if(currentuser.user_type == 'AD'):
                transactionTable.objects.filter(imei = imei, held_by = currentusername,last_transaction = True).delete()
                deviceTable.objects.filter(imei= imei).update(current_owner=currentusername)
            else:
                transactionTable.objects.filter(imei = imei, held_by = currentusername,last_transaction = True).delete()
                transactionTable.objects.filter(imei = imei, sold_to = currentusername,last_transaction = False).update(last_transaction = True)
                deviceTable.objects.filter(imei= imei).update(current_owner=currentusername)
                try:
                    live_location_table.objects.filter(imei_id = imei).delete()
                except:
                    print("Device not held  by user")
            return JsonResponse({"status" : "Successfully Reallocated"})
        except:
            return JsonResponse({"status" :"Invalid Transaction"})

    else:
        return render (request,'subdealer/reallocation.html')


#invetory search
@login_required
def transactionsearch(request):
        currentuser=request.user
        currentusername = currentuser.username
        if(currentuser.user_type != 'SD'):
        # return 404
            return render(request,'subdealer/error404.html')
        transactionobject = transactionTable.objects.filter(held_by = currentusername, imei__imei__icontains = request.POST['imei']).values('imei_id','sold_to_id','transaction_date')[:5]
        #print(transactionobject)
        return JsonResponse({"imeiObject" :  list(transactionobject)})

#####################################################################################################


@login_required
def editprofile(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
    profile_details =  User.objects.get(username = username)
    if request.method=="GET":
        return render(request,'subdealer/profile.html',{'data': profile_details})
    else:
        # for object in profile_details:
        if request.POST.get('email') !=None:
            profile_details.email=request.POST.get('email')
        if request.POST.get('phone') !=None:
            profile_details.phone=request.POST.get('phone')
        if request.POST.get('company_details') !=None:
            profile_details.company_details=request.POST.get('company_details')
        profile_details.save()
        context = {'success_message': 'Profile editing Successful.','data': profile_details} 
        return render(request,'subdealer/profile.html',context)



@login_required
def change_password(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
    profile_details =  User.objects.get(username = username)
    
    if request.method == 'GET':
        return render(request,'subdealer/profile.html',{'data': profile_details}) 
    else:
        pswd =  User.objects.get(username = username)
        password1 = request.POST.get('new_password')
        password2 = request.POST.get('confirm_password')
        if password1 == password2:
            pswd.password = make_password(password1)
            pswd.save()
            context = {'success_message': 'Password changing Successful.','data': profile_details} 
            return render(request,'subdealer/profile.html',context)
        else:
            context = {'error_message': 'Password doesnot match','data': profile_details}             
            return render(request,'subdealer/profile.html',context)


# dashboard password reset
@login_required
def ajax_password_reset(request):
    currentuser = request.user
    username = currentuser.username
    if(currentuser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
    try:
        user_exist = User.objects.get(username = request.POST['username'])
        if user_exist:
            user_exist.set_password(request.POST['password'])
            user_exist.save()
        return JsonResponse({"status" :"success"})
    except:
        return JsonResponse({"status" :"Some error occured"})


#dashboard loaduser
@login_required
def ajax_load_user(request):
    currentuser = request.user
    username = currentuser.username
    userobject = User.objects.filter(username__istartswith=request.POST['username'],added_by = username,user_type = "US").values('username','phone')[:10]
    return JsonResponse({"imeiObject" :  list(userobject)})

  
@login_required
def inventory(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
    if(request.GET.get('search')):
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),current_owner_id = currentUsername)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"stock"}
        return render(request,'subdealer/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(current_owner_id = currentUsername)
        stock_paginator = Paginator(device_object, 10)
        try:
            
            stock_page = stock_paginator.page(page_num)
        except:
           
            stock_page = stock_paginator.page(1)
        
        context = {"device_data" : stock_page,"term":"stock"}
    return render(request,'subdealer/inventory.html',context)
 

@login_required
def inventory_active(request):
    renewal = date.today() - datetime.timedelta(days=365)
    print(renewal)
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
    if(request.GET.get('search')):
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),activation_date__gt=renewal,current_owner_id = currentUsername) | deviceTable.objects.filter(imei__contains = request.GET.get('search'), transactiontable__held_by = currentUsername,activation_date__gt=renewal)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"active"}
        return render(request,'subdealer/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(activation_date__gt=renewal,current_owner_id = currentUsername) | deviceTable.objects.filter(transactiontable__held_by = currentUsername,activation_date__gt=renewal)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"active"}
    return render(request,'subdealer/inventory.html',context)
   

@login_required
def inventory_deactive(request):
    renewal = date.today() - datetime.timedelta(days=365)
    print(renewal)
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
    if(request.GET.get('search')):
        
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),activation_date__lt=renewal)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"deactive"}
        return render(request,'subdealer/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(activation_date__lt=renewal,current_owner_id = currentUsername).distinct() | deviceTable.objects.filter(transactiontable__held_by = currentUsername,activation_date__lt=renewal).distinct()
        print(device_object)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"deactive"}
    return render(request,'subdealer/inventory.html',context)


@login_required
def inventory_sold(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'SD'):
        # return 404
        return render(request,'subdealer/error404.html')
    if(request.GET.get('search')):
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),transactiontable__held_by = currentUsername)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"sold"}
        return render(request,'subdealer/inventory.html',context)
    else:

        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(transactiontable__held_by = currentUsername)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"sold"}
    return render(request,'subdealer/inventory.html',context)