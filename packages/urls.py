from . import views
from django.urls import path

urlpatterns = [
    # path("", views.PackageList.as_view(), name="packages"),
    path("", views.packagesall, name="packages"),
    # path("<slug:slug>/", views.PackageDetail.as_view(), name="package_detail"),
    # path("<slug:slug>/", views.PackageDetail.as_view(), name="package_detail"),
]
