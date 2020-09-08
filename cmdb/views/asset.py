#/usr/bin/env python
#-*- coding: utf-8 -*-

from django.views import View
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from cmdb.models import *
from cmdb.forms import *
from cmdb.views.permission import check_permission
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
class Location(View):
    def get(self,request):
        data=request.GET
        if request.path == '/dcroom/':
            nid = data.get('nid')
            IDCinfo = IDC.objects.filter(id=nid).all()
            return render(request,'dcroom.html',locals())
        elif request.path == '/location/':
            datacenter = IDC.objects.all()
            return render(request, 'datacenter.html', {'datacenter':datacenter})
    @method_decorator(check_permission)
    def post(self,request):
        data = request.POST
        print(data)
        if request.path == '/dcroom/':
            Rack.objects.create(cabinet_num=data.get('RackNum'),cabinet_order=data.get('cabinet_order'),IDC_id=data.get('idc_id'))
            return HttpResponse('ok')
        else:
            if data.get('status') == 'update':
                XY = data.getlist('XY[]')[1]+'*'+data.getlist('XY[]')[0]
                obj_idc = IDC.objects.filter(id=data.get('id'))
                obj_idc.update(name=data.get('name'),floor=data.get('floor'),address=data.get('address'),RackNum=XY)
            else:
                cabinet_order = data.get('X')+'*'+data.get('Y')
                IDC.objects.create(name=data.get('name'),floor=data.get('floor'),address=data.get('address'),RackNum=cabinet_order)
            return HttpResponse('ok')
class AssetInfo(View):
    def __init__(self):
        self.dic = []
    @method_decorator(check_permission)
    # @login_required()
    def get(self,request):
        server = Server.objects.all()
        networkdeviceinfo = NetworkDevice.objects.all()
        serverinfo = []
        serverinfo.extend(server)
        serverinfo.extend(networkdeviceinfo)
        AssetSearchFields = AssetSearchField()#搜索框参数
        paginator = Paginator(serverinfo,20)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'asset.html', {'ServerInfo':contacts,'AssetSearchFields':AssetSearchFields})
    @method_decorator(check_permission)
    def post(self, request):
        if request.POST.get('RemoveAsset')=='True':
            remove_server = Server.objects.filter(id=request.POST.get('nid')).all()
            remove_other = NetworkDevice.objects.filter(id=request.POST.get('nid')).all()
            if remove_server:
                for i in remove_server:
                    Asset.objects.filter(id=i.asset_id).delete()
                    Server.objects.filter(id=i.id).delete()
            elif remove_other:
                for i in remove_other:
                    Asset.objects.filter(id=i.asset_id).delete()
                    NetworkDevice.objects.filter(id=i.id).delete()
        return HttpResponse('ok')
class AssetDetail(View):
    def get(self,request):
        nid = request.GET.get('nid')
        data = Server.objects.filter(id=nid).all()
        nic = []
        address=[]
        try:
            for i in data:
                if i.IpAdress:
                   for k,v in (eval(i.IpAdress)).items():
                       nic.append(k)
                       address.append(v)
        except:
            pass
        return render(request,'detail.html',locals())
class CRM(View):
    def __init__(self):
        self.v1 = Django_test.objects.all()
        self.classess = Classes.objects.all()
        self.Teacheress = Teacheres.objects.all()
        self.Studentss = Students.objects.all()
    def get(self, request):
        if request.path == '/muotai/':
            return render(request,'muotai.html')
        elif request.path == '/set_teacher/':
            nid = request.GET.get('nid')
            teacher_list = Teacheres.objects.all()
            return render(request, 'set_teacher.html', {'teacher_list':teacher_list, 'nid':nid})
            # return render(request,'set_teacher.html',{'cls_teacher':cls_teacher})
        else:
            v1 =Classes.objects.all()
            return render(request,'students.html',{'v11':self.v1,'v1': self.classess, 'v2': self.Teacheress, 'v3': self.Studentss})
    def post(self,request):
        data = request.POST
        for i in data:
            if data.get('status') == 'delete':
                if not data.get('select'):
                    pass
                else:
                    for i in data.getlist('select',''):#getlist方法可以在同时删除多个id的时候循环获取列表里的每一项
                        Django_test.objects.filter(id=i).delete()
                        return redirect('/students/')
            elif data.get('status') == 'setup':
                nid = data.get('nid')
                teacher = data.getlist('teacher')
                obj = Classes.objects.filter(id=nid).first()

                obj.teacher.set(teacher)
                return redirect('/students/')
            elif data.get('status') == 'update':
                pass
            elif data.get('status') == 'submit':
                if request.path == '/students/':
                    if(data.get('name') == '' or data.get('age') == ''):
                        pass
                    else:
                        Students.objects.create(name=data.get('name'), age=data.get('age'),
                                                class_name_id=data.get('classes'), gender=data.get('gender'))
                    return redirect('/crm/')
                elif request.path == '/classes/':
                    if (data.get('captioin')=='' or data.get('code')==''):
                        pass
                    else:
                        Classes.objects.create(classname=data.get('caption'))
                        cls_obj = Classes.objects.filter(classname=data.get('caption')).first()
                        for i in data.get('teachers_id'):
                            cls_obj.teacher.add(i)
                    return redirect('/crm/')
                elif request.path == '/teachers/':
                    Teacheres.objects.create(name=data.get('TeacherName'))
                    return redirect('/crm/')
            else:
                return redirect('/students/')