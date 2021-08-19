from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
from accounts.models import User, deviceTable, transactionTable ,device_data_database
import time
from .forms import CreateDistributerForm1,CreateDistributerForm2,AllocateDevice
import openpyxl
import time
from datetime import date,datetime
import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime, timedelta


# Create your views here.
@login_required
def dashboard(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')

    purchase_count = deviceTable.objects.all().count()
    transaction_count = transactionTable.objects.filter(held_by = username).count()
    distributorcount = User.objects.filter(added_by = username,user_type = "DI").count()
    
    renewal = date.today() - timedelta(days=365)
    #query to determine deactivated device
    deactivated_in_sold = deviceTable.objects.filter(activation_date__lt=renewal).exclude(current_owner=username).count()

    #ready to sell
    readyToSell = deviceTable.objects.filter(current_owner = username,activation_date__gte=renewal).count()
    distributor = User.objects.filter(added_by = username,user_type = "DI").values('username','phone').order_by('-date_joined')[:10]

    return render(request,'master/dashboard.html',{"stock" : purchase_count,"sale":transaction_count,"userslist" : distributor ,"ready_to_sell":readyToSell,"dealer":distributorcount,"deactivated_in_sold":deactivated_in_sold})

##############################################################################################################################################################################################

@login_required
def addDevice(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if request.method == 'POST':
        # for key,value in request.POST.items():
        #     print(key,value)
        imei = request.POST.get('imei')
        iccid = request.POST.get('iccid')
        uniqueId = request.POST.get('uid')
        primaryNumber = request.POST.get('primaryNumber')
        secondaryNumber = request.POST.get('secondaryNumber')
        version = request.POST.get('version')
        activationDate = request.POST.get('activationDate')
        
        if(activationDate != None):
            activationStatus = 1    
        else:
            activationStatus = 0
            today = datetime.utcnow().date()
            activationDate = today - timedelta(days=730)
            
        addDeviceObject = deviceTable(imei = imei, 
                                    icc_id = iccid,
                                    unique_id = uniqueId,
                                    primary_contact = primaryNumber,
                                    secondary_contact = secondaryNumber,
                                    version = version,
                                    activation_status = activationStatus,
                                    activation_date = activationDate,
                                    current_owner_id= username)
        addDeviceObject.save()
        context = {"status" : "Device added successfully"}
        time.sleep(2)
    
    # Get Request
    context = {"status1" : ""}  
    return render(request,'master/add_device.html',context)


@login_required
def bulkadd(request):
    import datetime
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')   
    objectarray = []
    excel_file = request.FILES["excel_file"]

    # you may put validations here to check extension or file size
    wb = openpyxl.load_workbook(excel_file)

    # getting a particular sheet by name out of many sheets
    worksheet = wb["Sheet1"]
    print(worksheet)

        # iterating over the rows and
        # getting value from each cell in row
    for row in worksheet.iter_rows():
        if(row[0].value == "IMEI"):
            continue
        row_data = list()
        for cell in row:
            row_data.append(str(cell.value))
        try:
            date_to_strp = time.strptime(row_data[7], '%Y-%m-%d %H:%M:%S')
            date_final = datetime.datetime.fromtimestamp(time.mktime(date_to_strp))
            # date_final = datetime.datetime.strptime(row_data[7],'%Y-%m-%d')
            addDeviceObject = deviceTable(imei = row_data[0], 
                                    icc_id = row_data[1],
                                    unique_id = row_data[2],
                                    primary_contact = row_data[3],
                                    secondary_contact = row_data[4],
                                    version = row_data[5],
                                    activation_status = int(row_data[6]),
                                    # Date should come in the format DD-MM-YYYY
                                    activation_date = date_final,
                                    current_owner_id = username)
            objectarray.append(addDeviceObject)
            row_data.clear()
            
        except Exception as e:
            status = {'status':e}
            print(e)
            return render(request,'master/add_device.html',status)
    deviceTable.objects.bulk_create(objectarray)

    status = {'status2':'Upload Successfull and Device registered in Database'}
    return render(request,'master/add_device.html',status)


@login_required
def addDistributerPage(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if request.method == 'POST':
        # for key,value in request.POST.items():
        #     print(key,value)
        form1 = CreateDistributerForm1(request.POST)
        form2 = CreateDistributerForm2(request.POST)
        if form1.is_valid() and form2.is_valid():
            distributerName = request.POST['username']
            phone = request.POST['phone']
            firstName = request.POST['first_name']
            email = request.POST['email']
            company = request.POST['company']
            password = request.POST['password']
            User.objects.create_user(username=distributerName,
                                     first_name=firstName,
                                     email=email,
                                     password=password,
                                     user_type='DI',
                                     added_by=username,
                                     company_details=company,
                                     phone=phone)
            form1 = CreateDistributerForm1()
            form2 = CreateDistributerForm2()

            context = {'form1':form1,'form2':form2,'success_message': 'User Registration Successful.'}             
            return render(request,'master/add_distributer.html',context)
            
            
        else:
            context = {'form1':form1,'form2':form2}
            return render(request,'master/add_distributer.html',context)

    # Get Request
    form1 = CreateDistributerForm1()
    form2 = CreateDistributerForm2()
    context = {"status" : "",'form1':form1,'form2':form2}  
    return render(request,'master/add_distributer.html',context)


@login_required
def checkUsernameValid(request):
    currentUser = request.user
    currentUserName = currentUser.username
    if(currentUser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')    
    userobject = User.objects.filter(username = request.POST.get('username'),addedBy = currentUserName)
    if(userobject):
        return JsonResponse({"status" : "T"})
    else:
        return JsonResponse({"status" : "F"})


@login_required
def deviceStatusPage(request):
    currentUser = request.user
    currentUserName = currentUser.username
    if(currentUser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')     
    return render(request,'master/device_status.html')


# @login_required
# def deallocateDevice(request):
#     currentuser=request.user
#     currentUsername = currentuser.username
#     if(currentuser.user_type != 'AD'):
#         # return 404
#         return render(request,'master/error404.html')    
#     imei = request.POST.get('imei')
#     try:
#         if(currentuser.user_type == 'AD'):
#             transactionTable.objects.filter(imei = imei, held_by = currentUsername,last_transaction = True).delete()
#             deviceTable.objects.filter(imei= imei).update(holdedBy=currentUsername)
#         else:
#             transactionTable.objects.filter(imei = imei, held_by = currentUsername,last_transaction = True).delete()
#             transactionTable.objects.filter(imei = imei, sold_to = currentUsername,last_transaction = False).update(last_transaction = True)
#             deviceTable.objects.filter(imei= imei).update(holdedBy=currentUsername)
#         return JsonResponse({"status" : "Successfully Deallocated"})
#     except:
#         return JsonResponse({"status" :"Invalid Transaction"})
    


@login_required
def allocateDevice(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if request.method =='POST':
        for key, value in request.POST.items():
                print(key,value)
        form = AllocateDevice(request.POST)
        if form.is_valid():
            
            buyerUsername = request.POST['username']
            dateOfAllocation  = request.POST['allocate_date']
            imeiList = request.POST['imeilist']
            imeiList = imeiList.split(',')
            count = request.POST['count']
            recordArray =[]
            try:
                for record in imeiList:
                    deviceTable.objects.filter(imei = record).update(current_owner = buyerUsername)
                    print("DeviceT updation Success")
                    imei_heldBy = record+currentUsername
                    try:
                        get_transaction =  transactionTable.objects.get(imei_held_by = imei_heldBy)
                        form = AllocateDevice()
                        context = {"status" : "This transaction has been made already.",'form':form,'count':count}
                        return render(request,'master/allocation_main.html',context)
                    except transactionTable.DoesNotExist:
                        transactionObj = transactionTable( sold_to_id = buyerUsername,
                                                        held_by = currentUsername ,
                                                        imei_held_by = imei_heldBy,
                                                        imei_id = record ,
                                                        transaction_date = dateOfAllocation,
                                                        last_transaction = True)

                    if(currentuser.user_type != "AD"):
                        transactionTable.objects.filter(imei = record,sold_to = currentUsername).update(last_transaction = False)
                    recordArray.append(transactionObj)
                
                transactionTable.objects.bulk_create(recordArray)

                form = AllocateDevice(request.POST)
                context = {"status" : "Successfully Allocated",'form':form,'count':count}
                return render(request,'master/allocation_main.html',context)
            except Exception as e:
                
                context = {"status" :"Invalid Transaction"}
                return render(request,'master/allocation_main.html',context)
                            
    else:
        count = 0
        form = AllocateDevice()

    context = {'form':form,'count':count}
    return render(request,'master/allocation_main.html',context)


@login_required
def reallocateDevice(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')    
    if request.method == 'POST':       
        imei = request.POST.get('imei')
        try:
            if(currentuser.user_type == 'AD'):
                transactionTable.objects.filter(imei = imei, held_by = currentUsername,last_transaction = True).delete()
                deviceTable.objects.filter(imei= imei).update(current_owner=currentUsername)
            else:
                transactionTable.objects.filter(imei = imei, held_by = currentUsername,last_transaction = True).delete()
                transactionTable.objects.filter(imei = imei, sold_to = currentUsername,last_transaction = False).update(last_transaction = True)
                deviceTable.objects.filter(imei= imei).update(current_owner=currentUsername)
            return JsonResponse({"status" : "Successfully Reallocated"})
        except:
            return JsonResponse({"status" :"Invalid Transaction"})

    else:
        return render (request,'master/reallocation.html')


@login_required
def inventory(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'))[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"stock"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.all()
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"stock"}
    return render(request,'master/inventory.html',context)

  
@login_required
def inventory_active(request):

    renewal = date.today() - datetime.timedelta(days=365)
    print(renewal)
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),activation_date__gt=renewal)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"active"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(activation_date__gt=renewal,current_owner_id = currentUsername)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"active"}
    return render(request,'master/inventory.html',context)
   

@login_required
def inventory_deactive(request):
    renewal = date.today() - datetime.timedelta(days=365)
    print(renewal)
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),activation_date__lt=renewal)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"deactive"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(activation_date__lt=renewal)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"deactive"}
    return render(request,'master/inventory.html',context)


@login_required
def inventory_deactive_stock(request):
    renewal = date.today() - datetime.timedelta(days=365)
    print(renewal)
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),activation_date__lt=renewal)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"deactive"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(activation_date__lt=renewal,current_owner_id = currentUsername).distinct() 
        print(device_object)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"deactive"}
    return render(request,'master/inventory.html',context)

  
@login_required
def inventory_deactive_sold(request):
    renewal = date.today() - datetime.timedelta(days=365)
    print(renewal)
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),activation_date__lt=renewal)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"deactive"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object =  deviceTable.objects.filter(transactiontable__held_by = currentUsername,activation_date__lt=renewal).distinct()
        print(device_object)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"deactive"}
    return render(request,'master/inventory.html',context)


@login_required
def inventory_sold(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search')).exclude(current_owner = currentUsername)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"sold"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.all()
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"stock"}
    return render(request,'master/inventory.html',context)
   
    
@login_required
def inventory_active(request):

    renewal = date.today() - timedelta(days=365)
    print(renewal)
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),activation_date__gt=renewal)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"active"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(activation_date__gt=renewal,current_owner_id = currentUsername)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"active"}
    return render(request,'master/inventory.html',context)
   

@login_required
def inventory_deactive(request):
    renewal = date.today() - timedelta(days=365)
    print(renewal)
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),activation_date__lt=renewal)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"deactive"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(activation_date__lt=renewal)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"deactive"}
    return render(request,'master/inventory.html',context)


@login_required
def inventory_deactive_stock(request):
    renewal = date.today() - timedelta(days=365)
    print(renewal)
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),activation_date__lt=renewal)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"deactive"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(activation_date__lt=renewal,current_owner_id = currentUsername).distinct() 
        print(device_object)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"deactive"}
    return render(request,'master/inventory.html',context)

  
@login_required
def inventory_deactive_sold(request):
    renewal = date.today() - timedelta(days=365)
    print(renewal)
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search'),activation_date__lt=renewal)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"deactive"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object =  deviceTable.objects.filter(transactiontable__held_by = currentUsername,activation_date__lt=renewal).distinct()
        print(device_object)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"deactive"}
    return render(request,'master/inventory.html',context)


@login_required
def inventory_sold(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('search')):
        device_object = deviceTable.objects.filter(imei__contains = request.GET.get('search')).exclude(current_owner = currentUsername)[:10]
        page_num = request.GET.get('page',1)
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"search" :  request.GET.get('search'),"term":"sold"}
        return render(request,'master/inventory.html',context)
    else:
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(~Q(current_owner = currentUsername))
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"sold"}
    return render(request,'master/inventory.html',context)



@login_required
def inventory_dealer(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    if(request.GET.get('term') == "P"):
        context = {"term":"dealer"}
        return render(request,'master/inventory.html',context)
    elif(request.GET.get('dealer')):
        page_num = request.GET.get('page',1)
        device_object = deviceTable.objects.filter(current_owner = request.GET.get('dealer'))
        stock_paginator = Paginator(device_object, 10)
        try:
            stock_page = stock_paginator.page(page_num)
        except:
            stock_page = stock_paginator.page(1)
        context = {"device_data" : stock_page,"term":"dealer"}
        return render(request,'master/inventory.html',context)
    context = {"term":"dealer"}
    return render(request,'master/inventory.html',context)


#invetory search
@login_required
def transactionsearch(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if(currentuser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    transactionobject = transactionTable.objects.filter(held_by = currentUsername, imei__imei__icontains = request.POST['imei']).values('imei_id','sold_to_id','transaction_date')[:5]
    print(transactionobject)
    return JsonResponse({"imeiObject" :  list(transactionobject)})


# dashboard password reset
@login_required
def ajax_password_reset(request):
    currentUser = request.user
    if(currentUser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
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
    currentUser = request.user
    username = currentUser.username
    userobject = User.objects.filter(username__istartswith=request.POST['username'],added_by = username,user_type = "DI").values('username','phone')[:10]
    return JsonResponse({"imeiObject" :  list(userobject)})


#profile
@login_required
def editprofile(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    profile_details =  User.objects.get(username = username)
    if request.method=="GET":
        return render(request,'master/profile.html',{'data': profile_details})
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
        return render(request,'master/profile.html',context)

     
@login_required
def change_password(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'AD'):
        # return 404
        return render(request,'master/error404.html')
    profile_details =  User.objects.get(username = username)
    
    if request.method == 'GET':
        return render(request,'master/profile.html',{'data': profile_details}) 
    else:
        pswd =  User.objects.get(username = username)
        password1 = request.POST.get('new_password')
        password2 = request.POST.get('confirm_password')
        if password1 == password2:
            pswd.password = make_password(password1)
            pswd.save()
            context = {'success_message': 'Password changing Successful.','data': profile_details} 
            return render(request,'master/profile.html',context)
        else:
            context = {'error_message': 'Password doesnot match','data': profile_details}             
            return render(request,'master/profile.html',context)