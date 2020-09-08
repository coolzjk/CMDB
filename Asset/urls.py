"""Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.schemas import get_schema_view
from cmdb.views import account, home
from cmdb.views import asset
from cmdb.views import user
from cmdb.views import api
from cmdb.views.api import ReturnJson
from cmdb import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',views.index),
    url(r'^^$',views.homepage),
    url(r'^api_post/',api.post_asset.as_view()),
    url(r'^account/', account.LoginView.as_view()),
    url(r'^asset/', asset.AssetInfo.as_view(),name="asset"),
    url(r'^location/', asset.Location.as_view(),name="location"),
    url(r'^dcroom/', asset.Location.as_view(),name="location"),
    url(r'^home/', home.Index.as_view()),
    url(r'^user/', user.Userinfo.as_view()),
    url(r'^detail/',asset.AssetDetail.as_view()),
    url(r'^audit_asset/', api.AuditAsset.as_view(),name="add_assets"),
    url(r'^docs/', get_schema_view()),
    url(r'^api/get_idc', ReturnJson.as_view()),
    url(r'^api/get_asset', ReturnJson.as_view()),
    # url(r'^layout.html', api.layoutview.as_view()),
    url(r'^header_menu.html', api.header.as_view()),
    url(r'^search/', views.search.as_view()),
    url(r'^popover/', views.popover),

]
