#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: key
# @Date:   2015-12-18 12:32:32
# @Last Modified by:   key
# @Last Modified time: 2015-12-26 23:54:19

"""keyqq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import (signup,login,add_friend,get_friends,delete_friend,
                    move_friend,find_friend,get_account_data,
                    set_account_data)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$',signup),
    url(r'^login/$',login),
    url(r'^addfriend/$',add_friend),
    url(r'^getfriends/$',get_friends),
    url(r'^deletefriend/$',delete_friend),
    url(r'^movefriend/$',move_friend),
    url(r'^findfriend/$',find_friend),
    url(r'^getaccountdata/$',get_account_data),
    url(r'^setaccountdata/$',set_account_data)
]
