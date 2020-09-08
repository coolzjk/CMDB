import pydblite
import json
class pydb:
    def __init__(self,Asset):
        self.Asset = Asset
    def IsNew(self,hostname):
        bb = self.Asset
        results = pydb(My_test1=bb)
        for i in results:
            print(i[hostname])
    def NewAsset(self):
        bb = self.Asset
        bb=json.loads(bb)
        hostname = json.loads(self.Asset)['data']['hostname']
        pydb = pydblite.Base(':memory:')
        pydb.create('%s'%hostname)
        pydb.insert('%s=%s'%(hostname,bb))
        pydb.insert('%s=111'%hostname)
        results = pydb('%s'%hostname)