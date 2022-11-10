#from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('index/',views.index, name='index/'),
    path('', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('maintest/', views.maintest,name='maintest'),
    #path('search/<str:keyword>/<int:page>/', views.search),
    path('home/', views.home,name='home'),
    path('Empcreate/',views.Empcreate,name='Empcreate'),
    
    path('tool/show/', views.tool_show, name='tool_show'),
    path('Reprot', views.Reprot, name='Reprot'),
    path('tool/update/<int:id>/', views.tool_update, name='tool_update'),
    path('tool/delete/<int:id>/', views.tool_delete, name='tool_delete'),
    path('tool/att/<int:id>/', views.tool_att, name='tool_att'),
    path('addatt',views.addatt),
    path('tool/attdel/<int:id>/', views.tool_attdel, name='tool_attdel'),
    path('uptool',views.uptool),
    #re_path(r'^(?P<id>\d+)tool/delatt/$', views.tool_delatt, name='tool_delatt'),
    #path('<int:idw>/', views.tool_att, name='tool_att'),
    #path('tool/delatt/<int:id>/<int:iditem>', views.tool_delatt, name='tool_delatt'),
    #path('<int:id2>/', views.tool_delatt, name='tool_delatt'),
    
    #path('tool/showatt/<int:id>/', views.tool_showatt, name='tool_showatt'),
    #path('logout/',views.logout, name='logout'),
    #path('admin/', admin.site.urls),


    path('tool/create/', views.tool_create, name='tool_create'),
    path('addtool',views.addtool),

    path('item/CSV/', views.item_CSV, name='item_CSV'),
    path('item/Rpitem/', views.item_Rpitem, name='item_Rpitem'),
    #---------type---------#
    path('tool/type/<str:idtype>/', views.tool_type, name='tool_type'),
    path('typecreate',views.typecreate,name='typecreate'),
    path('typeshow',views.typeshow,name='typeshow'),
    path('typedel/<str:id>/',views.typedel,name='typedel'),
    path('addtype',views.addtype),
    #---------location---------#
    path('tool/loca/<str:loca>', views.tool_loca, name='tool_loca'),
    path('locacreate',views.locacreate,name='locacreate'),
    path('locashow',views.locashow,name='locashow'),
    path('locadel/<str:id>/',views.locadel,name='locadel'),
    path('addloca',views.addloca),
    #---------status---------#
    path('tool/status1/', views.tool_status1, name='tool_status1'),
    path('tool/status2/', views.tool_status2, name='tool_status2'),
    path('tool/status3/', views.tool_status3, name='tool_status3'),
    path('tool/status4/', views.tool_status4, name='tool_status4'),
    path('tool/status5/', views.tool_status5, name='tool_status5'),
    path('tool/status6/', views.tool_status6, name='tool_status6'),
]
