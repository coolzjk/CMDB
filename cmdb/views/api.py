from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse,HttpResponse,HttpRequest
from itertools import chain
from django.shortcuts import render
from cmdb.views.permission import check_permission
from cmdb.models import *
from cmdb.utils.dbm import *
class post_asset(View):
    def get(self,request):
        pass
    def post(self,request):
        data = request.body
        Assetinfo = json.loads(str(data, encoding='utf-8'))
        hostname = json.loads(Assetinfo)['data']['hostname']
        host = Server.objects.filter(hostname=hostname).first()
        if not host:
            ret = {'code': '1002', 'message': '[%s]资产不存在，需要等待管理员审核' % hostname}
            Assets = NewAssets(Assetinfo)
            Assets.add()
        else:
            Assetinfo=json.loads(Assetinfo)['data']
            data={'administrator':request.user,'manufacturer':Assetinfo['Brand'],'model':Assetinfo['Model'],'IpAdress':Assetinfo['IpAdress'],'DiskInfo':Assetinfo['DiskInfo'],'os_platform':Assetinfo['os_platform'],'os_version':Assetinfo['os_version'],'cpu_count':Assetinfo['cpu']['cpu_count'],'cpu_physical_count':Assetinfo['cpu']['cpu_physical_count'],'cpu_model':Assetinfo['cpu']['cpu_model'],'MemNumber':Assetinfo['MemInfo']['MemNumber'],'MemSize':Assetinfo['MemInfo']['MemSize'],}
            Server.objects.filter(hostname=hostname).update(**data)
            ret = {'code': '1000', 'message': '[%s]更新成功' % hostname}
        # '''
        return JsonResponse(ret)
class AuditAsset(View):
    def Auditcheck(self,approve_host=all):
        result = []
        Assets = NewAssets()
        if approve_host == all:#这段逻辑是为了给资产审核页面展示用。
            Newinfo = Assets.check(all=True)
            for i in Newinfo:
                res = json.loads(i.replace("'", '"'))
#这种写法老版dbm传来的数据用，新版直接过来就是字符串了用上面的写法                res = json.loads(str(i, encoding='utf-8').replace("'", '"'))
#json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)报错的解决，通过utf-8编码
                result.append(res)
            return result
        else:
            Newinfo = Assets.check(approve_host=approve_host)
            for i in Newinfo:
                result = json.loads(str(i,'utf-8').replace("'", '''"'''))
                return result
    def get(self,request):
        datacenter = IDC.objects.all()
        result = self.Auditcheck()
        Assetinfo = Asset.objects.all()
        return render(request,'audit.html',locals())
    @method_decorator(check_permission)
    def post(self,request):
        data = request.POST
        if not data.get('Approve_hostname'):#这个Approve_hostname在前端Ajax发起的时候添加到<option>里的发到后端来，写死的。如果没有就代表可能是拒绝过来的数据。
            if data.get('operator') == 'reject':#拒绝审核逻辑
                reject_host = self.Auditcheck(approve_host=data.get('hostname'))
                reject_host['operation'] = 'reject'
                Assets = NewAssets(json.dumps(reject_host))#把这里的str去掉往里面传就不报错了，饿了想不出为什么
                Assets.add()#这里的kwargs在方法里传，和之前客户端汇报后在类里传不一样
            elif data.get('operator')== 'remove':#删除拒绝后的置灰资产逻辑
                NewAssets().remove(data.get('hostname'))
            else:#资产通过审核写库
                cabinetnum = Rack.objects.filter(cabinet_num=data.get('Cabinet')).first()
                if data.get('AssetType')=='1':
                    ids = Asset.objects.create(TypeId=data.get('AssetType'),
                                               AssetNumber=data.get('Asset_num'),
                                               device_status=data.get('DeviceStatus'),
                                               cabinet_num=cabinetnum,
                                               form=data.get('RackmountSize'),
                                               position=data.get('Postion'),
                                               administrator=request.user,)
                    Server.objects.create(asset=ids,
                                          hostname=data.get('Asset_num'),
                                          sn=' ',
                                          manufacturer=' ',
                                          model=' ',
                                          IpAdress="",
                                          DiskInfo=" ",
                                          os_platform=' ',
                                          os_version='',
                                          cpu_count='1',
                                          cpu_physical_count='1',
                                          cpu_model= ' ',
                                          # uptime=' ',
                                          MemNumber='6',
                                          MemSize='2', )
                elif data.get('AssetType') == '2':
                    ids = Asset.objects.create(TypeId= data.get('AssetType'),
                                               AssetNumber= data.get('Asset_num'),
                                               device_status= data.get('DeviceStatus'),
                                               cabinet_num= cabinetnum,
                                               form= data.get('RackmountSize'),
                                               position= data.get('Postion'),
                                               administrator=request.user,)
                    NetworkDevice.objects.create(asset=ids,
                                                 port_num='24',)
                elif data.get('AssetType') == '3':#这个是之前写的逻辑，现在存储和网络设备合并了
                    ids = Asset.objects.create(TypeId=data.get('AssetType'),
                                               AssetNumber=data.get('Asset_num'),
                                               device_status=data.get('DeviceStatus'),
                                               cabinet_num=cabinetnum,
                                               form=data.get('RackmountSize'),
                                               position=data.get('Postion'),
                                               administrator=request.user,)
                    NetworkDevice.objects.create(asset=ids,
                                                 port_num='4', )
        else:#通过资产审核页面同意后添加资产的逻辑
            cabinetnum = Rack.objects.filter(cabinet_num=data.get('Cabinet')).first()
            AssetType = Asset.objects.filter(cabinet_num__cabinet_num=data.get('Cabinet')).first()
            approve_host = self.Auditcheck(approve_host=data.get('Approve_hostname'))
            if data.get('AssetType') == '1':
                ids = Asset.objects.create(TypeId=data.get('AssetType'),
                                    device_status=data.get('DeviceStatus'),
                                    cabinet_num=cabinetnum,
                                    position=data.get('position'),
                                    administrator=request.user,
                                   form=data.get('form'),)
                Server.objects.create(asset = ids,
                                    hostname = approve_host['hostname'],
                                    sn = approve_host['ProductNumbers'],
                                    manufacturer = approve_host['Brand'],
                                    model = approve_host['Model'],
                                    IpAdress = approve_host['IpAdress'],
                                    DiskInfo = approve_host['DiskInfo'],
                                    os_platform = approve_host['os_platform'],
                                    os_version = approve_host['os_version'],
                                    cpu_count = approve_host['cpu']['cpu_count'],
                                    cpu_physical_count = approve_host['cpu']['cpu_physical_count'],
                                    cpu_model = approve_host['cpu']['cpu_model'],
                                    #uptime = approve_host['Uptime'],
                                    MemNumber = approve_host['MemInfo']['MemNumber'],
                                    MemSize = approve_host['MemInfo']['MemSize'],)
                NewAssets().remove(data.get('Approve_hostname'))
        return HttpResponse('ok')

# 以下代码作用及使用方法参考/python/Django笔记/django框架-写一个接口返回json
from rest_framework.views import APIView
from dss.Serializer import serializer

def response_as_json(data, foreign_penetrate=False):
    jsonString = serializer(data=data, output_type="json", foreign=foreign_penetrate)
    response = HttpResponse(
            jsonString,
            content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200, foreign_penetrate=False, **kwargs):
    data = {
        "code": code,
        "msg": "成功",
        "data": data,
    }
    return response_as_json(data, foreign_penetrate=foreign_penetrate)


def json_error(error_string="", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)
JsonError = json_error

class ReturnJson(APIView,View):#返回机柜信息及设备信息的API
    def get(self, request, *args, **kwargs):
        Infos = {}
        ret = {#这个字典是供get_idc接口使用的
            "code": "200",
            "data": Infos,
        }
        if request.path == '/api/get_idc':
            for idc in IDC.objects.all():
                for cabinet in idc.r_i.values('cabinet_num'):
                    Infos.setdefault(idc.name, []).append(cabinet['cabinet_num'])
            return HttpResponse(json.dumps(ret))# 间接采用oldboy的方法，直接把数据序列化给前端了
        elif request.path == '/api/get_asset':
            room_id = request.GET.get('nid')
            ret = {
                "data": [],
                "EmptyRack":[]#接口里告诉前端哪些机柜坐标为空的，前端碰到后直接就走创建空机柜的逻辑了
            }
            CabinetNum = []

            IDCinfo = IDC.objects.filter(id=room_id).all()
            for idc in IDCinfo:#获取当前数据中心下面的所有信息，一个IDC对象
                for rack in idc.r_i.all():#获取该IDC下面的所有机柜信息，一个机柜对象
                    CabinetNum.append(rack.cabinet_order)
                    for item in rack.R_A.all():#这里是一个Asset表对象。
                        IpAdress = []
                        server = Server.objects.filter(asset=item.id).all()#根据asset表记录的id号去server表取关联的服务器信息记录
                        network = NetworkDevice.objects.filter(asset=item.id).all()
                        for i in server:
                            try:
                                CabinetNum.remove(i.asset.cabinet_num.cabinet_order)#如果有assetinfoQ对象，就在CabinetNum列表删除assetinfoQ对应的机柜编号坐标，CabinetNum列表里都是空的机柜坐标。
                            except:
                                pass
                            if i.IpAdress:#if not ipadress will report error,so add this judgment
                                for k, v in eval(i.IpAdress).items():
                                    IpAdress.append(v)
                            # else:
                                # IpAdress.append('null')
                        for i in network:
                            try:
                                CabinetNum.remove(i.asset.cabinet_num.cabinet_order)#如果有assetinfoQ对象，就在CabinetNum列表删除assetinfoQ对应的机柜编号坐标，CabinetNum列表里都是空的机柜坐标。
                            except:
                                pass
                            if i.management_ip:
                                for ip in i.management_ip:
                                    IpAdress.append(ip)
                        assetinfo_server = serializer(data=server, output_type="dict")#这里拿到的对象是一个列表，列表里是服务器系统信息的字典
                        assetinfo_network = serializer(data=network, output_type="dict")
                        assetinfo = chain(assetinfo_server,assetinfo_network)#这里用到chain,后面还查到一种extend方法。
                        for info in assetinfo:#循环这个列表拿到里面的字典添加到ret['data']里面去
                            info.update({'AssetNumber':item.AssetNumber,'TypeID':item.TypeId,'IpAdress':IpAdress,'comment':item.comment,'cabinet_num':rack.cabinet_num,'cabinet_order':rack.cabinet_order,"cabinet_pos":item.position,"device_status":item.device_status,"form":item.form})#哪个RACK的Order被记录控制在assetinfo变量过滤的值
                            ret['data'].append(info)
            ret['EmptyRack'].append(CabinetNum)
            return json_response(json.dumps(ret))#发现用python自带的json返回库就可以了。
# class layoutview(View):
#     def get(self, request, *args, **kwargs):
#         return render(request,'layout.html',locals())
class header(View):
    def get(self, request, *args, **kwargs):
        return render(request,'header_menu.html',locals())