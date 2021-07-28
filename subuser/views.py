from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User, device_data_database, live_location_table, vehicleDetails
from geopy.geocoders import GoogleV3

# Create your views here.

@login_required
def dashboard(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'SU'):
        # return 404
        return render(request,'subuser/error404.html')
    latitude=[] 
    longitude=[]
    timestamp=[]
    speed=[]
    vehicle_mode=[]
    vehicle_no=[]
    imeiList = []
  
    deviceobject = vehicleDetails.objects.filter(username_id = username)

    for rec in deviceobject:
        vehicle_no.append(rec.vehicle_no)

        live_location_object = live_location_table.objects.get(imei = rec.imei.imei)

        latitude.append(float(live_location_object.latitude))
        longitude.append(float(live_location_object.longitude))
        timestamp.append(str(live_location_object.ctime))
        speed.append(float(live_location_object.latitude))
        vehicle_mode.append(live_location_object.vehicle_mode)

    subuserlist = User.objects.filter(added_by = username,user_type = "SU").values('username','phone')[:10]
    context = {"vehicle_no":vehicle_no, "latitude" : latitude, "longitude" : longitude,"time_stamp" :timestamp, "speed" : speed, "vehicle_mode" : vehicle_mode ,"username":username,"subuserlist":subuserlist}
    return render(request,'subuser/dashboard.html',context)


 #Live location
@login_required
def ajax_load_live(request):
    currentUser = request.user
    if(currentUser.user_type != 'SU'):
        # return 404
        return render(request,'subuser/error404.html')
    
    imei = request.POST['imei']

    imeiobject = vehicleDetails.objects.get(imei_id = imei)
    vehicle_no = imeiobject.vehicle_no
    live_object =live_location_table.objects.get(imei_id=imei)

    context = {"latitude" : live_object.latitude, "longitude" : live_object.longitude,"time_stamp" :live_object.ctime, "speed" : live_object.speed, "vehicle_mode" : live_object.vehicle_mode,"imei":imei,"vehicle_no" : vehicle_no }
    return JsonResponse(context)


#Live location
@login_required
def load_live_view(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'SU'):
        # return 404
        return render(request,'subuser/error404.html')
    
    imei = request.POST['imei']
   
    imeiobject = vehicleDetails.objects.get(imei_id = imei)
    vehicle_no = imeiobject.vehicle_no
    live_object =live_location_table.objects.get(imei_id=imei)

    context = {"vehicle_no":vehicle_no, "latitude" : live_object.latitude, "longitude" : live_object.longitude,"time_stamp" :live_object.ctime, "speed" : live_object.speed, "vehicle_mode" : live_object.vehicle_mode,"imei":imei }

    return render(request,'subuser/liveview.html',context)


@login_required
def allVehicles(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'SU'):
        # return 404
        return render(request,'subuser/error404.html')
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
    
        context = zip(vehicle_no, latitude,longitude,timestamp,speed,vehicle_mode,address,imei)
    return render(request,'subuser/vehiclepage.html', {"context":context})


@login_required
def editprofile(request):
    currentUser = request.user
    username = currentUser.username
    if(currentUser.user_type != 'SU'):
        # return 404
        return render(request,'user/error404.html')
    profile_details =  User.objects.get(username = username)
    if request.method=="GET":
        return render(request,'subuser/profile.html',{'data': profile_details})
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
        return render(request,'subuser/profile.html',context)
    

@login_required
def ajax_fetch_graphs_data(request):
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


def ajax_vehicle_no_load(request):
    currentUser = request.user
    username = currentUser.username
    vehicle_no = []
    vehicle_no_object = vehicleDetails.objects.filter(username_id=username,vehicle_no__icontains = request.GET.get('term')).values('vehicle_no')
    for record in vehicle_no_object:
        vehicle_no.append(record['vehicle_no'])

    return JsonResponse(vehicle_no, safe=False)