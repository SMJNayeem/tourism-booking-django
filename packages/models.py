from django.db import models
from django.conf import settings

from accounts.models import User

# Create your models here.


class Packages(models.Model):
    pkg_name = models.CharField(
        verbose_name="Package Name", max_length=200, blank=True, null=True
    )
    pkg_desc = models.CharField(
        verbose_name="Package Description", max_length=250, blank=True, null=True
    )
    pkg_img = models.ImageField(
        upload_to="packages/package_images", blank=True, null=True
    )
    pkg_beg_date = models.DateTimeField(verbose_name="Package Starting Date and Time")
    pkg_end_date = models.DateTimeField(verbose_name="Package Ending Date and Time")
    pkg_location = models.CharField(
        verbose_name="Package Location", max_length=200, blank=True, null=True
    )
    pkg_seat = models.IntegerField(
        verbose_name="Package Total Seat", null=True, blank=True
    )
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    pkg_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.pkg_name


class Bookings(models.Model):
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pkg_info = models.ForeignKey(Packages, on_delete=models.CASCADE, null=True)
    user_seat = models.IntegerField(
        verbose_name="User Total Seat", null=True, blank=True
    )
    available_seat = models.IntegerField(
        verbose_name="Available Seat", null=True, blank=True
    )
    booking_details = models.CharField(
        verbose_name="Preference or comment by User",
        max_length=200,
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.available_seat
