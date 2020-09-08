#/usr/bin/env python
#-*- coding: utf-8 -*-
from django.views import View
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
class Userinfo(View):
    def get(self,request):
        return HttpResponse('User_profile')