from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
#Extending User model
class User(AbstractUser):
    
    USER = 'US'
    SUBUSER = 'SU'
    DISTRIBUTER = 'DI'
    DEALER = 'DE'
    SUBDEALER = 'SD'
    ADMIN = 'AD'

    Type_of_User = [
        (USER, 'User'),
        (SUBUSER, 'Subuser'),
        (DISTRIBUTER  , 'Distributer'),
        (DEALER, 'Dealer'),
        (SUBDEALER, 'Subdealer'),
        (ADMIN, 'Admin'),
    ]
    
    user_type = models.CharField(
        max_length=2,
        choices=Type_of_User,
        default=ADMIN
    )

    
    id = models.BigIntegerField(default=10,primary_key=True)
    first_name = models.CharField(null=False,blank=False, max_length=100)
    email = models.EmailField(null=False,blank=False)

    phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], help_text="Phone number without Country Code")   
    added_by = models.CharField(max_length=50)
    company_details = models.CharField(max_length=150, null= True, blank= True)


    def __str__(self):
        return "username = {}, user_type = {}".format(self.username, self.user_type)

    class Meta:
        db_table = 'User'


#Device class
class deviceTable(models.Model):
    
    imei = models.CharField(max_length=15, null = False,primary_key = True)
    icc_id = models.CharField(max_length=30,null=False,unique=True)
    unique_id = models.CharField(max_length=30,null = False,unique = True)

    primary_contact = models.DecimalField(max_digits=13, unique = True, null = False, decimal_places=0)
    secondary_contact = models.DecimalField(max_digits=13, unique = True, null = False, decimal_places=0)

    version = models.CharField(max_length=20)
    activation_status = models.BooleanField(null=False)
    activation_date = models.DateField(null= True,blank=True)

    current_owner = models.ForeignKey(User, to_field="username", on_delete= models.CASCADE)
    added_date = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return "imei = {} Current Owner = {}".format(self.imei, self.current_owner)
    
    class Meta:
        db_table = 'deviceTable'


#Vehicle Table
class vehicleDetails(models.Model):

    imei = models.ForeignKey(deviceTable, to_field="imei", on_delete= models.CASCADE)
    username = models.ForeignKey(User, to_field="username", on_delete= models.CASCADE)

    vehicle_no = models.CharField(max_length=30, blank=True,unique=True)
    installation_date = models.DateTimeField(default=datetime.now, blank=True)

    handled_by = models.CharField(max_length=50, null= True, blank= True)
    odometer = models.BigIntegerField(help_text="Distance travelled by the vehicle",blank=True,default=0)
    
    def __str__(self):
        return "imei = {} username = {} vehicle no: = {}".format(self.imei, self.username, self.vehicle_no)

    class Meta:
        db_table = 'vehicleDetails'

class transactionTable(models.Model):

    imei = models.ForeignKey(deviceTable, to_field="imei", on_delete= models.CASCADE)
    held_by = models.CharField(max_length=50, null= False)

    imei_held_by = models.CharField(max_length=100, null = False,primary_key = True,default='imei+held_by')
    sold_to = models.ForeignKey(User, to_field="username", on_delete= models.CASCADE)

    transaction_date = models.DateField(default=datetime.now, null= True)
    last_transaction = models.BooleanField(null=False)

    def __str__(self):
        return "imei = {} held by = {} sold to = {}".format(self.imei, self.held_by, self.sold_to)
    
    class Meta:
        db_table = 'transactionTable'


class live_location_table(models.Model):

    imei = models.ForeignKey(deviceTable, to_field="imei", on_delete= models.CASCADE)
    username = models.ForeignKey(User, to_field="username", on_delete= models.CASCADE)
    ctime = models.DateTimeField(null=True,blank=True)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True)
    speed = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    
    ignition = models.IntegerField(null=True,blank=True)
    vehicle_mode = models.CharField(max_length=1,null=True,blank=True)
    
    power_status = models.IntegerField(null=True,blank=True)
    alert_data = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "IMEI  = {} Last Record Time = {} Latitude = {} Longitude = {}".format(self.imei,self.ctime,self.latitude,self.longitude)

    class Meta:
        db_table = 'live_location_table'
    

class device_data_database(models.Model):
    
    imei = models.ForeignKey(deviceTable, to_field="imei", on_delete= models.CASCADE)
    ctime = models.DateTimeField()
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.DecimalField(max_digits=5, decimal_places=2)
    
    ignition = models.IntegerField(null=True,blank=True)
    vehicle_mode = models.CharField(max_length=1,null=True,blank=True)
    
    power_status = models.IntegerField(null=True)
    alert_data = models.IntegerField(blank=True, null=True)
    packet_status = models.CharField(max_length=1)
    ventor_id = models.CharField(max_length=6,blank=True, null=True)

    def __str__(self):
        return "IMEI  = {} Last Record Time = {}".format(self.imei,self.ctime)

    class Meta:
        db_table = 'device_data_database'


class user_vehicle_services(models.Model):
    
    vehicle_no =  models.ForeignKey(vehicleDetails, to_field="vehicle_no", on_delete= models.CASCADE)
    renewal_of_data = models.DateField(null=True,blank=True)
    renewal_of_insurance = models.DateField(null=True,blank=True)
    renewal_of_fitness = models.DateField(null=True,blank=True)
    renewal_of_pollution = models.DateField(null=True,blank=True)
    renewal_of_tax = models.DateField(null=True,blank=True)
    driver_mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], help_text="Phone number without Country Code",null=True,blank=True)
    username = models.ForeignKey(User, to_field="username", on_delete= models.CASCADE)

    def __str__(self):
        return "vehicle No: = {} Data = {} Insurance = {} Fitness = {} Pollution = {} Tax = {}".format(self.vehicle_no, self.renewal_of_data, self.renewal_of_insurance,self.renewal_of_fitness, self.renewal_of_pollution,self.renewal_of_tax)

    class Meta:
        db_table = 'user_vehicle_services'

class commands_table(models.Model):

    imei = models.ForeignKey(deviceTable, to_field="imei", on_delete= models.CASCADE)
    command = models.CharField(max_length=1, null = False)
    def _str_(self):
        return "command = {}".format(self.command)
    class Meta:
        db_table = 'commands_table'
    