from django.contrib import admin
from accounts.models import User, deviceTable, vehicleDetails ,transactionTable
# Register your models here.
admin.site.register(User)
admin.site.register(deviceTable)
admin.site.register(vehicleDetails)
admin.site.register(transactionTable)
