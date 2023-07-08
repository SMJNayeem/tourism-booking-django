from django.contrib import admin

# Register your models here.

from .models import Packages, Bookings

admin.site.register(Packages)
admin.site.register(Bookings)
