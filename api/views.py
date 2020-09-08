from django.shortcuts import render
from cmdb.models import *
from django.views.generic.base import View
# def business(request):
#     v1 = models.Django_Test.objects.all()
#     v2 = models.Django_Test.objects.values('id','caption')
#     v3 = models.Django_Test.objects.values_list('id','caption')
#     return render(request,'business.html',{'v1':v1,'v2':v2,'v3':v3})
class post_asset(View):
    def get(self,request):
        pass
    def post(self,request):

# Create your views here.
