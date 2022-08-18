from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Appointment)
admin.site.register(AppointmentSlot)
admin.site.register(Notification)
admin.site.register(Review)
admin.site.register(Contact)
