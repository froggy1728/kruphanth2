from cProfile import label
from dataclasses import field
from enum import auto
from django.db import models
from django import forms
from django import views

import datetime
import os

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

class Item(models.Model):
    name = models.CharField(max_length=100,default="")
    location = models.CharField(max_length=20,)
    #location = models.ForeignKey('location', on_delete=models.CASCADE)
    status = models.CharField(max_length=20,default="")
    details = models.TextField(max_length=100,null=True,default="-")
    idtype = models.CharField(max_length=99,null=False,default="")
    #idtype = models.ForeignKey('Type', on_delete=models.DO_NOTHING, verbose_name="Type", null=True, default=get_idtype)
    serial = models.CharField(max_length=11,default="")
    price = models.CharField(max_length=10,default="",null=True)
    pricetype = models.CharField(max_length=100,default="",null=True)
    date = models.CharField(max_length=11,default="",null=True)
    acquisition = models.CharField(max_length=50,default="",null=True)

class Type(models.Model):
    idtype = models.CharField(primary_key=True,max_length=99, null=False,default="")
    typecode = models.CharField(max_length=99,default="", null=True)
    typedetails = models.CharField(max_length=190, null=True,default="")

class Location(models.Model):
    location = models.CharField(primary_key=True,null=False,max_length=20,default="")
    namelocation = models.TextField(max_length=50, null=False, default="")
    

class attribute(models.Model):
    idatt = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='IDATT')
    iditem = models.CharField(max_length=10, null=False, default="")
    attname = models.CharField(max_length=100,null=False,default="")
    value = models.CharField(max_length=150,null=True,default="")

class locaform(forms.ModelForm):
		class Meta:
			model = Location
			fields = '__all__'
			labels = {
				'location': 'ชื่อสถานที่',
                'namelocation': 'ตำแหน่งสถานที',
			}
			

class attform(forms.ModelForm):
		class Meta:
			model = attribute
			fields = '__all__'
			labels = {
				'iditem': 'iditem',
                'attname': 'attname',
                'value': 'value',
			}
			widgets = {
                'iditem': forms.HiddenInput
			}

class ToolForm(forms.ModelForm):
		class Meta:
			model = Item
			fields = '__all__'
			labels = {
				'name': 'ชื่อเครื่องมือ',
				'location': 'สถานที่ใช้งาน',
				'status': 'สถานะเครื่องมือ',
                'idtype': 'ประเภทเครื่องมือ',
				'details': 'รายละเอียด',
			}
			
class typeform(forms.ModelForm):
		class Meta:
			model = Type
			fields = '__all__'
			labels = {
				'idtype': 'รหัสประเภท',
                'typename': 'ชื่อประเภท',
                'typedetails': 'รายละเอียดประเภท',
			}
            
class Employee(models.Model):
    idcrad = models.CharField(max_length=14,primary_key=True,null=False,default="")
    name = models.CharField(max_length=30,default="")
    lastname = models.CharField(max_length=30,default="")
    gender = models.CharField(
			max_length=6,
			choices=[('ชาย', 'ชาย'), ('หญิง', 'หญิง')],
			default='ชาย'
		)
    username = models.CharField(max_length=20, unique=True,default="")
    password = models.CharField(max_length=20,default="")
    position = models.CharField(max_length=20,default="")

class session(models.Model):
    name = models.TextField(max_length=100,default="")

class EmployeeForm(forms.ModelForm):
        class Meta:
            model = Employee
            fields = '__all__'
            labels = {
                'username': 'ชื่อผู้ใช้',
                'password': 'รหัสผ่าน'
            }
            widgets = {
                'password': forms.PasswordInput(render_value=True)
            }

class EmpcreateForm(forms.ModelForm):
		class Meta:
			model = Employee
			fields = '__all__'
			labels = {
                'idcrad': 'ID',
				'name': 'ชื่อ',
				'lastname': 'นามสกุล',
				'gender': 'เพศ',
                'username': 'ชื่อผู้ใช้',
                'password': 'รหัสผ่าน',
				'position': 'ตำแหน่งงาน',
			}
			widgets = {
				'gender': forms.RadioSelect(),
                'password': forms.PasswordInput(render_value=True)
			}

