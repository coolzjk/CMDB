from django.db import models

class Per(models.Model):
    name = models.CharField("权限名称", max_length=64)
    url = models.CharField('URL名称', max_length=255)
    chioces = ((1, 'GET'), (2, 'POST'))
    PerMethod = models.SmallIntegerField('请求方法', choices=chioces, default=1)
    argument_list = models.CharField('参数列表', max_length=255, help_text='多个参数之间用英文半角逗号隔开', blank=True, null=True)
    describe = models.CharField('描述', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
        # 权限信息，这里定义的权限的名字，后面是描述信息，描述信息是在django admin中显示权限用的
        permissions = (
            ('add_location', '添加数据中心'),
            ('edit_location', '编辑数据中心'),
            ('audit_assets', '资产审核权限'),
            ('add_assets', '添加资产信息'),
            ('edit_assets', '已录资产编辑'),
            ('del_assets', '已录资产删除'),
        )
class UserGroup(models.Model):
    """
    用户组
    """
    name = models.CharField(max_length=32, unique=True)
    users = models.ManyToManyField('UserProfile')
    class Meta:
        verbose_name_plural = "用户组表"
    def __str__(self):
        return self.name
class UserProfile(models.Model):
    """
    用户信息
    """
    name = models.CharField(u'姓名', max_length=32)
    email = models.EmailField(u'邮箱')
    phone = models.CharField(u'座机', max_length=32)
    mobile = models.CharField(u'手机', max_length=32)
    class Meta:
        verbose_name_plural = "用户表"
    def __str__(self):
        return self.name
class BusinessUnit(models.Model):
    """
    业务线
    """
    name = models.CharField('业务线', max_length=64, unique=True)
    contact = models.ForeignKey('UserGroup', verbose_name='业务联系人', related_name='c',on_delete=models.CASCADE) # 多个人
    manager = models.ForeignKey('UserGroup', verbose_name='系统管理员', related_name='m',on_delete=models.CASCADE) # 多个人
    class Meta:
        verbose_name_plural = "业务线表"
    def __str__(self):
        return self.name
class IDC(models.Model):
    """
    机房信息
    """
    name = models.CharField(max_length=64)
    floor = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=128,null=True,blank=True)
    RackNum = models.CharField(max_length=32)
    class Meta:
        verbose_name_plural = "IDC机房表"
    def __str__(self):
        return self.name
class Rack(models.Model):
    """
    机柜信息
    """
    IDC = models.ForeignKey('IDC',verbose_name='IDC机房',related_name='r_i',on_delete=models.CASCADE)
    cabinet_order = models.CharField('机柜内位置',max_length=24,null=True,blank=True)
    cabinet_num = models.CharField('机柜号',max_length=32,null=True,blank=True)
    class Meta:
        verbose_name_plural = "机房表"
    def __str__(self):
        return self.cabinet_num
class Asset(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
    """
    device_type_choices = (
        (1, '服务器'),
        (2, '网络设备'),
        (3, '存储设备'),
        (4, '虚拟机'),
        (5, '云主机'),
    )
    device_status_choices = (
        (1, '待投产'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架'),
    )
    TypeId = models.IntegerField(choices=device_type_choices, default=1)
    # AssetNum = models.CharField('资产编号', max_length=48, default=1)
    device_status = models.IntegerField(choices=device_status_choices, default=1)
    cabinet_num = models.ForeignKey('Rack', verbose_name='所属机柜编号',related_name='R_A',on_delete=models.CASCADE)
    position = models.CharField('机柜中位置', max_length=6, null=True, blank=True)
    form = models.CharField('设备高度', max_length=2, null=True, blank=True)
    AssetNumber = models.CharField('资产编号', max_length=48)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='属于的业务线', null=True, blank=True,on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', null=True, blank=True)
    latest_date = models.DateField(auto_now=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    administrator = models.CharField('管理员',max_length=8, null=True, blank=True)
    comment = models.CharField('设备描述',max_length=24,null=True, blank=True)
    class Meta:
        verbose_name_plural = "资产表"
    def __str__(self):
        return self.get_TypeId_display()
        # return "%s-%s-%s" % (self.idc.name, self.cabinet_num, self.cabinet_order)
class Server(models.Model):
    """
    服务器信息
    """
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)
    hostname = models.CharField(max_length=128, unique=True)
    sn = models.CharField('SN号', max_length=64, db_index=True)
    manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    model = models.CharField('型号', max_length=64, null=True, blank=True)
    manage_ip = models.GenericIPAddressField('管理IP', null=True, blank=True)
    IpAdress = models.CharField('IP地址', max_length=128, null=True, blank=True)
    DiskInfo = models.CharField('磁盘信息',max_length=512, null=True, blank=True)
    os_platform = models.CharField('系统', max_length=16, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=16, null=True, blank=True)
    cpu_count = models.IntegerField('CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField('CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)
    MemSize = models.IntegerField('内存大小', null=True, blank=True)
    MemNumber = models.IntegerField('物理内存个数', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    purchasing_time = models.DateField(null=True,blank=True,verbose_name='采购时间')
    # uptime = models.CharField('运行时长', max_length=32, null=True, blank=True)
    class Meta:
        verbose_name_plural = "服务器表"
    def __str__(self):
        return self.hostname
class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)
    management_ip = models.CharField('管理IP', max_length=64, blank=True, null=True)
    vlan_ip = models.CharField('VlanIP', max_length=64, blank=True, null=True)
    intranet_ip = models.CharField('内网IP', max_length=128, blank=True, null=True)
    sn = models.CharField('SN号', max_length=64, blank=True, null=True, unique=True)
    manufacture = models.CharField(verbose_name=u'制造商', max_length=128, null=True, blank=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField('端口个数', null=True, blank=True)
    device_detail = models.CharField('设置详细配置', max_length=255, null=True, blank=True)
    class Meta:
        verbose_name_plural = "网络设备"
class TAG(models.Model):
    """
     资产标签
     """
    name = models.CharField('标签', max_length=32, unique=True)
    class Meta:
        verbose_name_plural = "标签表"
    def __str__(self):
        return self.name
class ErrorLog(models.Model):
    """
    错误日志,如：agent采集数据错误 或 运行错误
    """
    asset_obj = models.ForeignKey('Asset', null=True, blank=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=16)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "错误日志表"
    def __str__(self):
        return self.title