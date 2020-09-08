#/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime
from django.views.generic.base import View
from django.db.models import Q
from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from cmdb.models import *
from cmdb.utils.dbConnect import *
from cmdb.forms import *
def homepage(request):
    return redirect('http://glpi.imageco.cn/glpi')
def index(request):
    today = str(datetime.date.today()).split('-',1)[1]
    return render(request,'index.html',locals())
def popover(request):
    return render(request,'popover.html',locals())
class search(View):
    def search(self,query,args1=None,args=None):
        device = []
        ids = []
        if args:
            if query:
                if Rack.objects.filter(Q(cabinet_num__startswith=query)) or IDC.objects.filter(Q(name__startswith=query)):
                    for rack in Rack.objects.filter(Q(cabinet_num__startswith=query)):
                        if args1 == 'TypeId':
                            asset = Asset.objects.filter(cabinet_num=rack.id).filter(TypeId=args).all()
                        else:
                            asset = Asset.objects.filter(cabinet_num=rack.id).filter(device_status=args).all()
                        for info in asset:
                            device.extend(Server.objects.filter(asset=info.id).all())
                            device.extend(NetworkDevice.objects.filter(asset=info.id).all())
                    for idc in IDC.objects.filter(Q(name__startswith=query)):
                        rack = Rack.objects.filter(IDC=idc.id).all()
                        for asset in rack:
                            if args1 == 'TypeId':
                                asset = Asset.objects.filter(cabinet_num=asset.id).filter(TypeId=args).all()
                            else:
                                asset = Asset.objects.filter(cabinet_num=asset.id).filter(device_status=args).all()
                            for info in asset:
                                device.extend(Server.objects.filter(asset=info.id).all())
                                device.extend(NetworkDevice.objects.filter(asset=info.id).all())
                else:
                    values = dbconnect(query)  # 查询到匹配记录，之后通过循环获取该记录的id号
                    for i in values:
                        ids.append(i[0])  # 获取记录全部字段的值，拿第一个字段的值也就是id号，为一个元组对象。
                    server = Server.objects.filter(id__in=ids).all()  # __in方法根据ids列表值匹配id字段
                    networkdeviceinfo = NetworkDevice.objects.filter(id__in=ids).all()
                    device.extend(server)
                    device.extend(networkdeviceinfo)
            else:#没有文字根据高级搜索项搜索
                if Rack.objects.filter(Q(cabinet_num__startswith=query)) or IDC.objects.filter(Q(name__startswith=query)):
                        if args1 == 'TypeId':
                            asset = Asset.objects.filter(TypeId=args).all()
                        else:
                            asset = Asset.objects.filter(device_status=args).all()
                        for info in asset:
                            device.extend(Server.objects.filter(asset=info.id).all())
                            device.extend(NetworkDevice.objects.filter(asset=info.id).all())
        else:#没有高级项目，按照正常的搜索流程走一遍
            if query:#没有高级搜索，搜索框有输入
                if Rack.objects.filter(Q(cabinet_num__startswith=query)) or IDC.objects.filter(Q(name__startswith=query)):
                    for rack in Rack.objects.filter(Q(cabinet_num__startswith=query)):
                        asset = Asset.objects.filter(cabinet_num=rack.id)
                        for info in asset:
                            device.extend(Server.objects.filter(asset=info.id).all())
                            device.extend(NetworkDevice.objects.filter(asset=info.id).all())
                    for idc in IDC.objects.filter(Q(name__startswith=query)):
                        rack = Rack.objects.filter(IDC=idc.id).all()
                        for asset in rack:
                            asset = Asset.objects.filter(cabinet_num=asset.id).all()
                            for info in asset:
                                device.extend(Server.objects.filter(asset=info.id).all())
                                device.extend(NetworkDevice.objects.filter(asset=info.id).all())
                else:
                    values = dbconnect(query)  # 查询到匹配记录，之后通过循环获取该记录的id号
                    for i in values:
                        ids.append(i[0])  # 获取记录全部字段的值，拿第一个字段的值也就是id号，为一个元组对象。
                    server = Server.objects.filter(id__in=ids).all()  # __in方法根据ids列表值匹配id字段
                    networkdeviceinfo = NetworkDevice.objects.filter(id__in=ids).all()
                    device.extend(server)
                    device.extend(networkdeviceinfo)
            else:#没有高级搜索，什么都没输入，展示全部信息
                pass
        return device


    def get(self,request):#因为下一页或者选页码的时候没有wd参数传过来，走不进上面的search函数里的判断
        result = []
        action = ''
        if request.GET.get('wd'):
            if request.GET.get('DeviceType'):
                action = 'DeviceType='+request.GET.get('DeviceType')
                result.extend(self.search(request.GET.get('wd'),'TypeId',request.GET.get('DeviceType')))
            elif request.GET.get('DeviceStatus'):
                action = 'DeviceStatus='+request.GET.get('DeviceStatus')
                result.extend(self.search(request.GET.get('wd'), 'DeviceStatus', request.GET.get('DeviceStatus')))
            else:
                result.extend(self.search(request.GET.get('wd')))
        else:
            if request.GET.get('DeviceType'):
                action = 'DeviceType='+request.GET.get('DeviceType')
                result.extend(self.search('','TypeId',request.GET.get('DeviceType')))
            elif request.GET.get('DeviceStatus'):
                action = 'DeviceStatus='+request.GET.get('DeviceStatus')
                result.extend(self.search('', 'DeviceStatus', request.GET.get('DeviceStatus')))
            else:
                return redirect('/asset/')
        AssetSearchFields = AssetSearchField  # 把高级搜索框里的内容传给前端
        paginator = Paginator(result, 20)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'asset.html',{'ServerInfo': contacts, 'wd': request.GET.get('wd'),'action':action, 'AssetSearchFields': AssetSearchFields})


    def post(self,request):
        if request.POST.get('Searchindex'):
            if request.POST.get('q'):
                if request.POST.get('TypeId'):
                    url = '/search/?wd=' + request.POST.get('q') + '&DeviceType=' + request.POST.get('TypeId')
                else:
                    url = '/search/?wd=' + request.POST.get('q') + '&DeviceStatus=' + request.POST.get('device_status')
            else:
                if request.POST.get('TypeId'):
                    url = '/search/?&DeviceType=' + request.POST.get('TypeId')
                else:
                    url = '/search/?&DeviceStatus=' + request.POST.get('device_status')
        else:
            url = '/search/?wd=' + request.POST.get('q')
        return redirect(url)
    '''
    判断有没有高级搜索
 有：
  判断有没有wd
    有
      判断有没有机柜号和机房号
        有：
          先查机柜和机房对应的资产，服务器和网络设备表根据资产id过滤再匹配高级搜索
        没有:
          先根据wd匹配服务器和网络设备的表，再根据高级搜索匹配
     没有
       根据高级搜索要求匹配服务器和网络设备表字段
  没有:
    判断有没有wd
      有
        判断有没有机柜号和机房号
          有:
            先查机柜和机房对应的资产，服务器和网络设备表根据资产id过滤
          没有:
             服务器和网络设备表根绝关键字过滤
       没有
         选择全部设备
    '''