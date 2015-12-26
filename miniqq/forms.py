#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: key
# @Date:   2015-12-18 12:35:48
# @Last Modified by:   key
# @Last Modified time: 2015-12-26 20:50:04
from django.forms import ModelForm
from .models import User

class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['password','name','sex','birth','hometown','address','desc','imageid','email']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['account','password']
