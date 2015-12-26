#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: key
# @Date:   2015-12-18 12:35:48
# @Last Modified by:   key
# @Last Modified time: 2015-12-27 00:23:47
from django.contrib import admin
from .models import User,Friend

# Register your models here.
admin.site.register(User)
admin.site.register(Friend)
