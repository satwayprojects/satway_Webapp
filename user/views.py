from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
from django.http.response import JsonResponse

from django.shortcuts import redirect, render
from .forms import CreateSubUserForm1, CreateSubUserForm2
from django.urls import reverse
from accounts.models import User,vehicleDetails,live_location_table,device_data_database
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from geopy.geocoders import GoogleV3
import datetime

from math import cos, asin, sqrt, pi

def distance(lat1, lon1, lat2, lon2):
    if (lat1 == 0 and lon1 == 0) or (lat2 == 0 and lon2 == 0):
        return 0
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    result = 12742 * asin(sqrt(a))
    if result > 10:
        return 0
    else:
        return result

# Create your views here.
@login_required
def dashboard(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    latitude=[] 
    longitude=[]
    timestamp=[]
    speed=[]
    vehicle_mode=[]
    vehicle_no=[]
    imeiList = []
  
    deviceobject = vehicleDetails.objects.filter(username_id = username)
    print(deviceobject)
    try:
        for rec in deviceobject:
            vehicle_no.append(rec.vehicle_no)
            try:
                live_location_object = live_location_table.objects.get(imei_id = rec.imei.imei)

                latitude.append(float(live_location_object.latitude))
                longitude.append(float(live_location_object.longitude))
                timestamp.append(str(live_location_object.ctime))
                speed.append(float(live_location_object.latitude))
                vehicle_mode.append(live_location_object.vehicle_mode)
            except:
                continue

            print(vehicle_no)
    except Exception as e:
        return render(request,'user/dashboard.html')    

    subuserlist = User.objects.filter(added_by = username,user_type = "SU").values('username','phone')[:10]
    context = {"vehicle_no":vehicle_no, "latitude" : latitude, "longitude" : longitude,"time_stamp" :timestamp, "speed" : speed, "vehicle_mode" : vehicle_mode ,"username":username,"subuserlist":subuserlist}
    return render(request,'user/dashboard.html',context)


# history for a vehicle
def load_history(request):
    geolocator = GoogleV3(api_key="AIzaSyBuIUlchZeES76eY3eNz94jboBMlBEIZDE")
    if(request.POST.get('start_date') != None):

        vehicle_start_time =[]
        vehicle_start_point =[]
        vehicle_end_time =[]
        vehicle_end_point =[]
        total_distance=[]
        imei =request.POST['imei']
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')

        end_time = request.POST.get('end_time')
        end_date = request.POST.get('end_date')

        start = start_date + " " + start_time
        end = end_date + " " + end_time

        start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M')
        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M')

        while(start < end):
            try:
                start_object = device_data_database.objects.filter(imei = imei,vehicle_mode = "M",ctime__gt= start).order_by('ctime').values('ctime','latitude','longitude').first()
                vehicle_start_time.append(start_object['ctime'])
                locations = geolocator.reverse((start_object['latitude'],start_object['longitude']))
                vehicle_start_point.append(locations)
                end_object = device_data_database.objects.filter(imei=imei,vehicle_mode = "S",ctime__gt= start_object['ctime']).order_by('ctime').values('ctime','latitude','longitude').first()
                vehicle_end_time.append(end_object['ctime'])
                locations = geolocator.reverse((end_object['latitude'],end_object['longitude']))
                vehicle_end_point.append(locations)
                start = end_object['ctime']
                all_data = device_data_database.objects.filter(ctime__gte= start_object['ctime'], ctime__lte=end_object['ctime'], vehicle_mode='M').order_by('ctime')



                lat = []
                lon = []
                N = 0
                for record in all_data:
                    lat.append(float(record.latitude))
                    lon.append(float(record.longitude))
                    N += 1

                dist = 0
                total = 0
                for i in range(1,N):
                    if lat[i-1] != lat[i] and lon[i-1] != lon[i]:
                        dist = abs(distance(lat[i-1],lon[i-1],lat[i],lon[i]))
                        total +=  dist
                total_distance.append(total)


            except Exception as e:
                break 
        context = zip(vehicle_start_time,vehicle_start_point,vehicle_end_time,vehicle_end_point,total_distance)
        return render(request,'user/history.html',{"imei":imei,"context" : context})
    else:
        imei =request.POST['imei']
    return render(request,'user/history.html',{"imei":imei})


@login_required
def history_live_view(request):
    latitude =[]
    longitude =[]
    speed =[]
    start_date= datetime.datetime.strptime(request.POST.get('startdate'),'%B %d, %Y, %I:%M %p')
    end_date = datetime.datetime.strptime(request.POST.get('enddate'),'%B %d, %Y, %I:%M %p')
    imei = request.POST.get('imei')
    
    live_object = device_data_database.objects.filter(imei = imei,ctime__gt=start_date).order_by('ctime').values('latitude','longitude','speed') & device_data_database.objects.filter(imei = imei,ctime__lt=end_date).order_by('ctime').values('latitude','longitude','speed')
    
    for rec in live_object:
        if(float(rec['latitude']) == 0.0 or float(rec['longitude']) == 0.0):
            continue
        else:
            latitude.append(float(rec['latitude']))
            longitude.append(float(rec['longitude']))
            speed.append(float(rec['speed']))
    return render(request,'user/history_data_plot.html',{"latitude":latitude,"longitude":longitude,"speed" : speed})


 #Live location
@login_required
def ajax_load_live(request):
    currentUser = request.user
    
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    imei = request.POST['imei']

    imeiobject = vehicleDetails.objects.get(imei_id = imei)
    vehicle_no = imeiobject.vehicle_no
    live_object =live_location_table.objects.get(imei_id=imei)

    context = {"latitude" : live_object.latitude, "longitude" : live_object.longitude,"time_stamp" :live_object.ctime, "speed" : live_object.speed, "vehicle_mode" : live_object.vehicle_mode,"imei":imei,"vehicle_no" : vehicle_no }
    return JsonResponse(context)


@login_required
def load_live_view(request):
    currentUser = request.user
    
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')

    imei = request.POST['imei']
   
    imeiobject = vehicleDetails.objects.get(imei_id = imei)
    vehicle_no = imeiobject.vehicle_no
    live_object =live_location_table.objects.get(imei_id=imei)

    context = {"vehicle_no":vehicle_no, "latitude" : live_object.latitude, "longitude" : live_object.longitude,"time_stamp" :live_object.ctime, "speed" : live_object.speed, "vehicle_mode" : live_object.vehicle_mode,"imei":imei }
    return render(request,'user/liveview.html',context)


@login_required
def subUserRegisteration(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    form2 = CreateSubUserForm1()
    form2 = CreateSubUserForm1()
    if request.method =='POST':
        
        form1 = CreateSubUserForm1(request.POST)
        form2 = CreateSubUserForm2(request.POST)
        if form1.is_valid() and form2.is_valid():
            current_user = request.user  #retuens User Object [username = Amal, user_type = US]

            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            firstName = request.POST['first_name']
            email= request.POST['email']
            phone = request.POST['phone']
            company = request.POST['company']
            if company == '':
                company = None
           
            # Creating User Object
            user = User.objects.create_user(username=username,first_name=firstName,email=email,password=password,user_type='SU',added_by=current_user.username,phone=phone,company_details=company)
            user.save()
            form1 = CreateSubUserForm1()
            form2 = CreateSubUserForm2()
            context = {'form1':form1,'form2':form2,'success_message': 'Sub-User Registration Successful.'}             
            return render(request,'user/subuserregisteration.html',context)

        else:
            context = {'form1':form1,'form2':form2}
            return render(request,'user/subuserregisteration.html',context)       
   
    form1 = CreateSubUserForm1()
    form2 = CreateSubUserForm2()
    context = {"status" : "",'form1':form1,'form2':form2}
    return render(request,'user/subuserregisteration.html',context)  


@login_required
def allVehicles(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'US'):
            # return 404
        return render(request,'user/error404.html')

    
    address = []
    latitude=[]
    longitude=[]
    timestamp=[]
    speed=[]
    vehicle_mode=[]
    vehicle_no=[]
    imei=[]
    imeiList = {}
    geolocator = GoogleV3(api_key="AIzaSyBuIUlchZeES76eY3eNz94jboBMlBEIZDE")
    
    
    try:
        if(request.POST['vehicle_no']):
            deviceobject = vehicleDetails.objects.get(vehicle_no = request.POST['vehicle_no'])
            
            
            vehicle_no.append(request.POST['vehicle_no'])
            imeiList[0] = deviceobject.imei.imei
            imei.append(deviceobject.imei.imei)
            live_location_object = live_location_table.objects.get(imei_id = deviceobject.imei.imei)
            latitude.append(float(live_location_object.latitude))
            longitude.append(float(live_location_object.longitude))
            timestamp.append(str(live_location_object.ctime))
            speed.append(float(live_location_object.speed))
            vehicle_mode.append(live_location_object.vehicle_mode)
            locations = geolocator.reverse((float(live_location_object.latitude),float(live_location_object.longitude)))
            if locations:
                address.append(locations[0])
                
            context = zip(vehicle_no, latitude,longitude,timestamp,speed,vehicle_mode,address,imei)
            return render(request,'user/vehiclepage.html', {"context":context})

    except:
        deviceobject = vehicleDetails.objects.filter(username_id = username)
        i=0
        for rec in deviceobject:
            vehicle_no.append(rec.vehicle_no)
            imeiList[i] = rec.imei.imei
            imei.append(rec.imei.imei)
            try:
                live_location_object = live_location_table.objects.get(imei_id = rec.imei.imei)
                latitude.append(float(live_location_object.latitude))
                longitude.append(float(live_location_object.longitude))
                timestamp.append(str(live_location_object.ctime))
                speed.append(float(live_location_object.speed))
                vehicle_mode.append(live_location_object.vehicle_mode)
                locations = geolocator.reverse((float(live_location_object.latitude),float(live_location_object.longitude)))
                if locations:
                    address.append(locations[0])
                i+=1
            except:
                continue
    
        context = zip(vehicle_no, latitude,longitude,timestamp,speed,vehicle_mode,address,imei)
        return render(request,'user/vehiclepage.html', {"context":context})

        
@login_required
def allocateSubUser(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    
    if request.method == 'POST':
        subuser = request.POST['subuser']
        phone = request.POST['phone']
        count = request.POST['count']
        try:
            user = User.objects.get(username=subuser,phone=phone,added_by=username)
            #User exist
            vehiclelist = request.POST['vehiclelist'].split(',')
            print(vehiclelist)
            print(len(vehiclelist))
            if vehiclelist[0] == '':
                status = "Vehicle Details Incorrect."
                context = {'count': count,'status':status,'subuser':subuser,'phone':phone}
                return render(request,'user/allocationpage.html',context)
            for vehicle in vehiclelist:
                try:
                    # Allocating Vehicles
                    vehicleDetails.objects.filter(vehicle_no=vehicle,username_id=username,handled_by=None).update(handled_by=subuser)
                except Exception as e:
                    print(e)
                    status = "Vehicle Details Incorrect."
                    context = {'count': count,'status':status,'subuser':subuser,'phone':phone}
                    return render(request,'user/allocationpage.html',context)
            #Vehicles Allocated
            status = "Vehicles are allocated."
            context = {'count': count,'status1':status,'subuser':subuser,'phone':phone}
            return render(request,'user/allocationpage.html',context)     

        except User.DoesNotExist:
            count = 0
            status = "Sub-User doest not exist. Check username."
            context = {'count': count,'status':status,'subuser':subuser,'phone':phone}
            return render(request,'user/allocationpage.html',context)
    else:
        count = 0
    
    context = {'count': count}
    return render(request,'user/allocationpage.html',context)


@login_required
def reallocation(request):
    return render(request,'user/reallocationpage.html')

# Reallocate
@login_required
def rellocatevehicle(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    status = ''
    alert = ''

    if request.method == 'POST':
        user = User.objects.get(username=username)
        success = user.check_password(request.POST['password'])
        if success:
            vehicle = request.POST['vehicle2'].strip()
            vehicleDetails.objects.filter(vehicle_no=vehicle,username_id=username).update(handled_by=None)
            status = 'Vehicle {} has been reallocated.'.format(request.POST['vehicle2'])
            alert = ''  
        else:
            alert = 'Password Incorrect.'
            status = ''      
    context = {'status':status,'alert':alert}
    return render(request,'user/reallocationpage.html',context)


@login_required
def delete_subuser(request):
    currentUser = request.user
    username = currentUser.username

    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    
    subuser = request.POST['subuser']
    phone = request.POST['phone']
    password = request.POST['password']

    if request.method == 'POST':
        user = User.objects.get(username=username)
        success = user.check_password(password)
        print(success)
        if success:
            try:
                
                vehicleDetails.objects.filter(username_id=username,handled_by=subuser).update(handled_by=None)
                userObj =  User.objects.get(username=subuser,phone=phone)
                userObj.delete()
                context = {'status':"The Sub-User {} has been deleted.\nAll vehiches handled by {} has been transferred.".format(subuser,subuser)} 
                return render(request,'user/reallocationpage.html',context)
            except User.DoesNotExist:
                
                context = {'status':"The Sub-User {} is not present.".format(subuser)}
                return render(request,'user/reallocationpage.html',context)
        else:
            
            context = {'alert':"Password Incorrect."}
            return render(request,'user/reallocationpage.html',context)

    return render(request,'user/reallocationpage.html')


@login_required
def editprofile(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    profile_details =  User.objects.get(username = username)
    if request.method=="GET":
        return render(request,'user/profile.html',{'data': profile_details})
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
        return render(request,'user/profile.html',context)


@login_required
def change_password(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    profile_details =  User.objects.get(username = username)
    
    if request.method == 'GET':
        return render(request,'user/profile.html',{'data': profile_details}) 
    else:
        pswd =  User.objects.get(username = username)
        password1 = request.POST.get('new_password')
        password2 = request.POST.get('confirm_password')
        if password1 == password2:
            pswd.password = make_password(password1)
            pswd.save()
            context = {'success_message': 'Password changing Successful.','data': profile_details} 
            return render(request,'user/profile.html',context)
        else:
            context = {'error_message': 'Password doesnot match','data': profile_details}             
            return render(request,'user/profile.html',context)


@login_required
def allocationstatus(request):
    currentUser = request.user
    username = currentUser.username
    
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')

    vehiclesObj = vehicleDetails.objects.filter(username_id=username)[:15]
    context = {'vehicles':vehiclesObj}
    return render(request,'user/allocationstatus.html',context)


@login_required
def load_subuser(request):
    currentUser = request.user
    user = currentUser.username
    
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')

    if 'username' in request.POST:
        userObj = User.objects.filter(username__icontains=request.POST['username'],user_type='SU',added_by=user).values('username','phone')[:5]
        return JsonResponse({"userObject" :  list(userObj)}, safe=False)


@login_required
def password_reset(request):
    currentuser=request.user
    currentusername = currentuser.username
    if(currentuser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    try: 
        user_exist = User.objects.get(username = request.POST['username'],added_by=currentusername)
        if user_exist:
            user_exist.set_password(request.POST['password'])
            user_exist.save()

        return JsonResponse({"status" :"success"})
    except:
        return JsonResponse({"status" :"Some error occured"})


@login_required
def load_subuser_phone(request):
    currentUser = request.user
    username = currentUser.username
    print(request.GET.get('term'))
    if 'term' in request.GET:
        qs = User.objects.filter(username__icontains=request.GET.get('term'),user_type='SU',added_by=username).values('username','phone')[:5]
        listUser = []
        for record in qs:
            r = record['username'] +',' + record['phone']
            listUser.append(r)
        print(listUser)
        return JsonResponse(listUser, safe=False)


@login_required
def loadvehicle(request):
    currentUser = request.user
    username = currentUser.username
    
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    print(request.GET.get('term'))
    vehicleObject = vehicleDetails.objects.filter(vehicle_no__icontains=request.POST.get('vehicle'), username_id=username).values('vehicle_no','imei_id','handled_by')
    print(vehicleObject)
    return JsonResponse({"vehicleObject" :  list(vehicleObject)}, safe=False)

  
@login_required
def load_vehicle_no(request):
    currentUser = request.user
    username = currentUser.username

    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    try:
        vehicleObject = vehicleDetails.objects.filter(vehicle_no__icontains=request.GET.get('term'), username_id=username).values('vehicle_no')
        vehicleList = list()

        for vehicle in vehicleObject:
            vehicleList.append(vehicle['vehicle_no'])
        return JsonResponse(vehicleList, safe=False)
    except:
        return JsonResponse({"state" : "F"})


@login_required
def ajax_fetch_graphs_data(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
        
    from datetime import datetime
    from django.db.models import FloatField
    from django.db.models.functions import Cast
    from django.db.models import Avg
    currentUser = request.user
    username = currentUser.username
    now = datetime.now()
    start_time = now.replace(hour=00, minute=1)
    print(start_time)
    vehicle_no=[]
    coordinates_list=[]
    avg_speed=[]
    avg_engine_on_time=[]
    deviceobject = vehicleDetails.objects.filter(username_id = username)
    # i=0

    for rec in deviceobject:

        vehicle_no.append(rec.vehicle_no)
        device_data_object = device_data_database.objects.filter(imei_id = rec.imei_id,ctime__gt= start_time,vehicle_mode = "M").annotate(latitude1=Cast('latitude', FloatField()),longitude1=Cast('longitude', FloatField())).values('latitude1','longitude1').order_by('ctime')
        # print(device_data_object)
        coordinates_list.append(list(device_data_object))
        device_avg_speed_object = device_data_database.objects.filter(imei_id = rec.imei_id,ctime__gt= start_time).aggregate(Avg('speed'))

        avg_speed.append(device_avg_speed_object['speed__avg'])
        device_engine_object = device_data_database.objects.filter(imei_id = rec.imei_id,ctime__gt= start_time,vehicle_mode = "M") | device_data_database.objects.filter(imei_id = rec.imei_id,ctime__gt= start_time,vehicle_mode = "H")

        total_seconds = (device_engine_object.count() * 30 / 60)/60
        avg_engine_on_time.append(total_seconds)
    context = {"avg_engine_time" : avg_engine_on_time,"avg_speed": avg_speed,"vehicle_no" : vehicle_no,"coordinates" : coordinates_list}
    return JsonResponse(context)

@login_required
def load_vehicle_subuser(request):
    currentUser = request.user
    username = currentUser.username

    if(currentUser.user_type != 'US'):
        # return 404
        return render(request,'user/error404.html')
    try:
        vehicleObject = vehicleDetails.objects.filter(vehicle_no__contains=request.GET.get('term'), username_id=username).values('vehicle_no','handled_by').exclude(handled_by__isnull=True).exclude(handled_by__exact='')
        vehicleList = list()

        for vehicle in vehicleObject:
            vehicleList.append(vehicle['vehicle_no']+'  ,  '+vehicle['handled_by'])
        
        return JsonResponse(vehicleList, safe=False)
    except Exception as e:
        return JsonResponse({"state" : "F"})


@login_required
def check_vehicleno(request):
    currentUser = request.user
    username = currentUser.username
    vehicle= request.POST['vehicle']
    
    try:
        vehicleObject = vehicleDetails.objects.get(vehicle_no = vehicle, username_id = username,handled_by=None)
        return JsonResponse({"vehicleObject" :  model_to_dict(vehicleObject)})
    except:
        return JsonResponse({"state" : "F" , "vehicle" : vehicle})


def ajax_vehicle_no_load(request):
    currentUser = request.user
    username = currentUser.username
    vehicle_no = []
    vehicle_no_object = vehicleDetails.objects.filter(username_id=username,vehicle_no__icontains = request.GET.get('term')).values('vehicle_no')
    for record in vehicle_no_object:
        vehicle_no.append(record['vehicle_no'])

    return JsonResponse(vehicle_no, safe=False)