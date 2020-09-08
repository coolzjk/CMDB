#/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *
# urlparterns = [
urlpatterns = [
    url(r'^post_asset/', post_asset.as_view()),
]