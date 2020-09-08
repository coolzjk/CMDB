#/usr/bin/env python
#-*- coding: utf-8 -*-
from django.views import View
from cmdb.forms import *
from django.contrib import auth
from django.shortcuts import render,HttpResponse,redirect
from cmdb import models
# from cmdb import check_code
from io import BytesIO

def getcheck_code(request):
    code = check_code.getCheckChar()
    img = check_code.getImg(code)
    f = BytesIO()
    img.save(f, 'PNG')
    request.session['check_code']=code
    return HttpResponse(f.getvalue())

from django import forms
class FM(forms.Form):       #这里要接受后端需要的，不需要的数据不会关注
    teacher_id=forms.CharField(error_messages={'required':"不能为空"})  #表单中的name要与变量名一样
    password=forms.CharField(
        min_length=5,
        error_messages={'required':"不能为空",
                        'min_length':'密码长度不小于5',},
    )
class LoginView(View):
    def get(self, request):
        if request.GET.get('action') == 'login':
            userinfo = Login()
            return render(request, 'login.html', locals())
        elif request.GET.get('action') == 'logout':
            auth.logout(request)
            return redirect('/index/')
    def post(self, request):
        login_form = Login(request.POST)#根据forms里的定义验证post数据是否合规
        if login_form.is_valid():#通过forms里的类型判断post数据是否合规
            logined = login_form.cleaned_data
            user = auth.authenticate(username=logined['username'], password=logined['password'])#这里通过django admin验证模块验证用户名密码是否正确
            if user is not None and user.is_active:#没有验证成功会得到一个None的对象,并且账号是active状态
               auth.login(request, user)#将登录信息存储到django自身的 login模块 中
               return redirect("/index/")
            else:
                return render(request, "login.html", {"msg": u"用户名或者密码错误!"})
        else:
            return render(request, "login.html", {"userinfo": login_form})


