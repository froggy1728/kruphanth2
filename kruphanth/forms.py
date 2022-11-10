from cProfile import label
from multiprocessing.sharedctypes import Value
from django import forms
from database.models import Item 

class loginform(forms.Form):
    username=forms.CharField(label='username')
    password=forms.CharField(label='password',widget=forms.PasswordInput(render_value=True))
    save = forms.BooleanField(label='บันทึกไว้ในเครื่องนี้',required=False)

class searchform(forms.Form):
    name = forms.CharField(label='',required=False)
    #id = forms.CharField(required=False)

class typeform2(forms.Form):
    idtype = forms.CharField(label='idtype',required=False,widget=forms.TextInput)
    typename = forms.CharField(label='typename',required=False,widget=forms.TextInput)
    typedetails = forms.CharField(label='typedetails',required=False,widget=forms.TextInput)






