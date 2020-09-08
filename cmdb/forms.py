from django import forms
from cmdb import models
from django.forms import widgets
class AssetSearchField(forms.ModelForm):#搜索框点击加号新增的下拉框用
    class Meta:
        model = models.Asset
        exclude = ()
        widgets = {
            'TypeId':forms.Select(attrs={'disabled':'disabled','id':'AssetType','class':'form-control','style':'width:110px;display:none',}),
            'device_status':forms.Select(attrs={'disabled':'disabled','id':'AssetStatus','class':'form-control','style':'width:110px;display:none',})
        }
class Login(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"请输入用户名","autocomplete":"new-password","size":"10"}))
    password = forms.CharField(widget=widgets.PasswordInput(attrs={"placeholder": "请输入密码","autocomplete":"new-password","size":"10"}))