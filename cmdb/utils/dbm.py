import dbm,json,sys
class NewAssets:
    SysPath = sys.path[0]
    def __init__(self,Assetinfo='null'):
        self.Assetinfo = Assetinfo

    def add(self,*arg,**kwargs):
        NewAssets = dbm.open(self.SysPath + '/cmdb/utils/newhost', 'c')
        data = json.loads(self.Assetinfo)
        if 'data' not in data:
            hostname = data['hostname']
            NewAssets[hostname] = str(data)
            NewAssets.close
        else:
            hostname = data['data']['hostname']
            NewAssets[hostname] = str(data['data'])
            NewAssets.close
    def check(self,*arg,**kwargs):
        dic = []
        Assetinfo = dbm.open(self.SysPath+'/cmdb/utils/newhost','r')
        if kwargs:
            for k,v in kwargs.items():
                if k == 'all':#判断传参all是否为True
                    for key in Assetinfo.keys():
                        dic.append(Assetinfo[key].decode('utf-8'))
                else:
                    dic.append(Assetinfo[v])
            return dic
    def remove(self,hostname):
        Assetinfo = dbm.open(self.SysPath+'/cmdb/utils/newhost','c')
        del Assetinfo[hostname]
