from django.shortcuts import render
from .models import Bookings, Packages
from django.views import generic
from django.contrib.auth.decorators import login_required

# Create your views here.


# class PackageList(generic.ListView):
#     queryset = Packages.objects.filter(status=1).order_by("-created_on")
#     template_name = "packages.html"


# @login_required(login_url="login")
def packagesall(request):
    packages = Packages.objects.all()
    return render(request, "packages/packages.html", {"packages": packages})


# class PackageDetail(generic.DetailView):
#     model = Packages
#     template_name = "package_detail.html"


# @method_decorator(login_required(login_url='login'), name='dispatch')
# @method_decorator(guser_only, name='dispatch')
# class RequisitionCreate(SuccessMessageMixin, CreateView):
#     model = Requisition
#     form_class = RequisitionForm
#     template_name = 'vmsUser/userrequisition.html'

#     def form_valid(self, form):
#         request = self.request
#         form.save()
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)
