#/usr/bin/env python
#-*- coding: utf-8 -*-
from django.views import View
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
class Index(View):
    def get(self,request):
        return render(request,'dcroom_popover_ok.html',locals())