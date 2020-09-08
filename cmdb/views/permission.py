from cmdb import models
from django.core.urlresolvers import resolve
from django.shortcuts import render,HttpResponse
def perm_check(request,*args,**kwargs):
    url_obj = resolve(request.path)
    url_name = url_obj.url_name
    matched = models.Per.objects.filter(url=url_name).all()
    hit = {}
    if matched:
        for url in matched:
            if request.method == url.get_PerMethod_display():#匹配请求和权限表里的字段是否匹配
                args_list = url.argument_list.split(',')#权限表参数字段里的内容变成列表
                for arg in args_list:#循环这个列表，post请求里有的就匹配，没有说明这个请求不需要权限管理
                    if arg in request.POST:
                        hit[url.name]='True'
                        break
                    else:#循环获得第二个参数是一个空格，走到这个逻辑是POST被false
                        hit[url.name] ='False'
            else:
                return True
    else:
        return True
    for k,v in hit.items():
        if v == 'True':
            perm_str = "cmdb.%s" %k  # 此处url.name为请求url里的name属性匹配到的一个权限库里的name字段值，url及name只会匹配到一个，请求参数会有多个。
            if request.user.has_perm(perm_str):
                return True
            else:  # 否则代表上面的用户权限匹配不成功，不能执行这个操作。
                return False

def check_permission(fun):    #定义一个装饰器，在views中应用
    def wapper(request, *args, **kwargs):
        if perm_check(request, *args, **kwargs):  #调用上面的权限验证方法
            return fun(request, *args, **kwargs)
        return HttpResponse('no permission')
    return wapper