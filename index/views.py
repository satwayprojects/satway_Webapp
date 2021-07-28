from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls.base import reverse
from accounts.models import User, deviceTable, transactionTable
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AllocateDevice
from django.contrib import messages

# Create your views here.


# For already logged In users
def loginUser(request):
    user = request.user

    if user.is_authenticated:
        if user.user_type == 'US':
            # app_name: in urls.py of app and view name
            return HttpResponseRedirect(reverse('user:Dashboard'))
        elif user.user_type == 'SU':
            return HttpResponseRedirect(reverse('subuser:Dashboard'))
        elif user.user_type == 'DI':
            return HttpResponseRedirect(reverse('distributer:Dashboard'))
        elif user.user_type == 'AD':
            return HttpResponseRedirect(reverse('master:Dashboard'))
        elif user.user_type == 'DE':
            return HttpResponseRedirect(reverse('dealer:Dashboard'))
        elif user.user_type == 'SD':
            return HttpResponseRedirect(reverse('subdealer:Dashboard'))

    return render(request,'index/login.html')


def forgot_password(request):
    if request.method=='GET':
        return render(request,'index/forgotpassword.html')
    else:
        phone= request.POST.get('phone')
        try:
            userdata = User.objects.get(phone=phone)
            addedbydata = userdata.added_by
            addeduser = User.objects.get(username = addedbydata)
            return render(request,'index/forgotpassword.html',{'data': addeduser})
                
        except:
            context = {'error_message': ' Contact your dealer'}
            return render(request,'index/forgotpassword.html',context)


@login_required
def loadUser(request):
   
    currentUser = request.user
    currentUserType = currentUser.user_type
    username = currentUser.username
    if(currentUserType == 'AD'):
        allocationUserType = "DI"
    elif(currentUserType == 'DI'):
        allocationUserType = "DE"
    elif(currentUserType == 'DE'):
        allocationUserType = "SD"
    userObject = User.objects.filter(username__istartswith=request.GET.get('term'), user_type = allocationUserType, added_by=username).values('username')
    userList = list()
    for obj in userObject:
        userList.append(obj['username'])
    return JsonResponse(userList, safe=False)


@login_required
def allocationimeiCheck(request):
    currentUser = request.user
    currentUserName = currentUser.username
    imei = request.POST.get('imei')
    print(imei)
    try:
        imeiObject = deviceTable.objects.get(imei = imei, current_owner_id = currentUserName)
        #print(imeiObject.version)
        return JsonResponse({"imeiObject" :  model_to_dict(imeiObject)})
    except:
        return JsonResponse({"state" : "F" , "imei" : imei})


@login_required
def inventory(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if request.method == "POST":
        deviceobject = deviceTable.objects.filter(current_owner_id = currentUsername,imei__contains = request.POST['imei']).values('imei','primary_contact','secondary_contact','activation_date')[:10]
        return JsonResponse({"imeiObject" :  list(deviceobject)})
    else:
        deviceobject = deviceTable.objects.filter(current_owner_id = currentUsername).values('imei','primary_contact','secondary_contact','activation_date')[:5]
        transactionobject = transactionTable.objects.filter(held_by = currentUsername).values('imei_id','sold_to_id','transaction_date')[:10]
        return render(request,'index/inventory.html',{"device":deviceobject,"transaction" : transactionobject})


#invetory search
@login_required
def transactionsearch(request):
        currentuser=request.user
        currentUsername = currentuser.username
        transactionobject = transactionTable.objects.filter(held_by = currentUsername, imei__imei__icontains = request.POST['imei']).values('imei_id','sold_to_id','transaction_date')[:10]
        print(transactionobject)
        return JsonResponse({"imeiObject" :  list(transactionobject)})


@login_required
def checkReallocationStatus(request):
    currentuser=request.user
    currentUsername = currentuser.username
    imei = request.POST.get('imei')
    try:
        deviceObject = transactionTable.objects.filter(imei = imei, held_by = currentUsername,last_transaction = True).values('sold_to')
        userobject = User.objects.filter(username = deviceObject[0]['sold_to']).values('phone')
        print(userobject)
        return JsonResponse({"status":deviceObject[0]['sold_to'],"phone" : userobject[0]['phone']})
    except Exception as e: 
        return JsonResponse({"status" :"F"})


@login_required
def ajax_check_user_username(request):
    currentUser = request.user
    username = currentUser.username
    if 'term' in request.GET:
        qs = User.objects.filter(username__icontains=request.GET.get('term'),user_type='US',added_by=username).values('username','phone')[:5]
        listUser = []
        for record in qs:
            r = record['username'] +',' + record['phone']
            listUser.append(r)
        print(listUser)
        return JsonResponse(listUser, safe=False)


@login_required
def ajax_check_subuser_name(request):
    currentUser = request.user
    username = currentUser.username
    if 'term' in request.GET:
        qs = User.objects.filter(username__startswith=request.GET.get('term'),user_type='SU',added_by=username).values('username','phone')[:5]
        listUser = []
        for record in qs:
            r = record['username'] +',' + record['phone']
            listUser.append(r)
        print(listUser)
        return JsonResponse(listUser, safe=False)


@login_required
def ajax_load_user_imei(request):
    currentUser = request.user
    username = currentUser.username
    if 'term' in request.GET:
        qs = deviceTable.objects.filter(current_owner=username,imei__contains = request.GET.get('term')).values('imei')[:5]
    listImei = []
    for record in qs:
        r = record['imei']
        listImei.append(r)
    return JsonResponse(listImei, safe=False)



@login_required
def ajax_loaddealer(request):
    if 'term' in request.GET:
        qs =User.objects.filter(username__contains = request.GET.get('term'),user_type = 'DE') | User.objects.filter(username__contains = request.GET.get('term'),user_type = 'DI') .values('username')[:5]
    listImei = []
    for record in qs:
        r = record.username
        listImei.append(r)
    return JsonResponse(listImei, safe=False)


@login_required
def ajax_loaddealer_users(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if 'term' in request.GET:
        qs = User.objects.filter(username__contains = request.GET.get('term'),user_type = 'DE',added_by = currentUsername).values('username')[:5]
    listImei = []
    for record in qs:
        r = record['username']
        listImei.append(r)
    return JsonResponse(listImei, safe=False)


@login_required
def ajax_loaddealer_subdealer(request):
    currentuser=request.user
    currentUsername = currentuser.username
    if 'term' in request.GET:
        qs = User.objects.filter(username__contains = request.GET.get('term'),user_type = 'SD',added_by = currentUsername).values('username')[:5]
    listImei = []
    for record in qs:
        r = record['username']
        listImei.append(r)
    return JsonResponse(listImei, safe=False)




