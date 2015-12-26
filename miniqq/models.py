#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: key
# @Date:   2015-12-18 12:35:48
# @Last Modified by:   key
# @Last Modified time: 2015-12-27 00:23:31
from django.db import models

# Create your models here.
class Friend(models.Model):
    person = models.ForeignKey('User',verbose_name="用户名",blank=True,null=True)
    groupname = models.CharField(default="默认的",max_length=30,verbose_name="组名")

    def __str__(self):
        return  "好友帐号:"+ str(self.person.account) + " 组名:" + self.groupname
        # return "组名:" + self.groupname

class User(models.Model):
    account = models.AutoField(unique=True,verbose_name="帐号",primary_key=True)
    password = models.CharField(max_length=30,verbose_name="密码")
    name = models.CharField(max_length=30,verbose_name="昵称")
    sex = models.CharField(max_length=6,default="男",verbose_name="性别")
    hometown = models.CharField(max_length=20,verbose_name="籍贯",blank=True)
    address = models.CharField(max_length=50,blank=True,verbose_name="地址")
    birth = models.CharField(max_length=10,verbose_name="出生年月")
    desc = models.TextField(verbose_name="个人描述",blank=True)
    imageid = models.CharField(max_length=50,verbose_name="头像ID",blank=True)
    email = models.EmailField(verbose_name="邮箱",blank=True)
    registered_date = models.DateTimeField(auto_now_add=True,verbose_name="注册日期")
    is_login = models.BooleanField(default=False,verbose_name="是否在线")
    ip = models.GenericIPAddressField(unpack_ipv4=True,verbose_name="IP地址",blank=True,null=True)
    ip_local = models.GenericIPAddressField(unpack_ipv4=True,verbose_name="内网IP地址",blank=True,null=True)
    local_port = models.CharField(max_length=8,blank=True,verbose_name="内网ip地址端口号")
    android_ip = models.GenericIPAddressField(unpack_ipv4=True,verbose_name="内网IP地址",blank=True,null=True)
    android_port = models.CharField(max_length=8,blank=True,)
    pcstate = models.CharField(max_length=4,blank=True)
    adstate = models.CharField(max_length=4,blank=True)
    friends = models.ManyToManyField('Friend',verbose_name="好友",blank=True,null=True)

    def __str__(self):
        return  '帐号:' + str(self.account)
