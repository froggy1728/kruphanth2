from asyncore import write
from contextlib import redirect_stderr
import re
from urllib import response
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse, reverse
from database.models import Item, Employee, EmpcreateForm, Location, ToolForm, attribute, attform, typeform, Type, locaform
from .forms import loginform, searchform, typeform2
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.contrib import messages
import csv

def index(request):
    return render(request, 'index.html')

def Reprot(request):
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    name = request.session['name']
    lastname = request.session['lastname']
    return render(request, 'Reprot.html', {'name': name, 'lastname': lastname, 'Qtype': Qtype, 'Qloca': Qloca})

@csrf_exempt
def login(request):
    # ถ้าในขณะนั้นได้เข้าสู่ระบบแล้ว
    # ก็ไปยังเพจหลักของสมาชิกได้ทันที
    if 'idcrad' in request.session:
        return redirect(reverse('home'))
    # ถ้าโพสต์ข้อมูลเข้ามา
    err_msg = None
    if request.method == 'POST':
        form = loginform(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        save = request.POST.get('save', False)
        # นำuserและรหัสผ่านไปตรวจสอบว่ามีในฐานข้อมูลหรือไม่
        # ถ้ามี ก็เก็บค่า id และชื่อไว้ในเซสชัน เพื่อบ่งชี้ว่า เข้าสู่ระบบแล้ว
        row = Employee.objects.filter(
            Q(username=username) & Q(password=password))
        if row.count() == 1:
            request.session['idcrad'] = row[0].idcrad
            request.session['name'] = row[0].name
            request.session['lastname'] = row[0].lastname
            request.session.set_expiry(0)
            # สร้างออบเจ็กต์ HttpResponse เพื่อส่งข้อมูลกลับไปและจัดการคุกกี้
            tmp = loader.get_template('home.html',)
            data = {
                'name': row[0].name, 'lastname': row[0].lastname, 'idcrad': row[0].idcrad}
            response = HttpResponse(tmp.render(data))

            # ถ้าเลือกบันทึกข้อมูลไว้ในเครื่อง ก็จัดเก็บในแบบคุกกี้ โดยกำหนดอายุ 1 วัน
            # แต่ถ้าไม่เลือก ก็ให้ลบออกจากคุกกี้ (เผื่อจะเก็บไว้ก่อนแล้ว)
            if save:
                # เวลา
                age = 60*60*24
                response.set_cookie('username', value=username, max_age=age)
                response.set_cookie('password', value=password, max_age=age)
                response.set_cookie('save', value=save, max_age=age)
            else:
                response.delete_cookie('username')
                response.delete_cookie('password')
                response.delete_cookie('save')
            return response
        else:
            err_msg = 'อีเมลหรือรหัสผ่านไม่ถูกต้อง'
    # ถ้าเปิดเพจ และมีข้อมูลจัดเก็บในแบบคุกกี้เอาไว้แล้ว
    # ให้อ่านค่า จากนั้นนำไปเติมเป็นค่าล่วงหน้าให้แก่ฟอร์ม
    elif 'username' in request.COOKIES:
        username = request.COOKIES.get('username', '')
        password = request.COOKIES.get('password', '')
        save = request.COOKIES.get('save', False)
        form = loginform(
            initial={'username': username, 'password': password, 'save': save}
        )
    else:
        form = loginform()
    return render(request, 'login.html', {'form': form, 'err_msg': err_msg})

def logout(request):
    if 'idcrad' in request.session:
        del request.session['idcrad']
        del request.session['name']
        del request.session['lastname']
    return redirect(reverse('login'))

def maintest(request):
    return render(request, 'maintest.html')

def home(request):
    if 'idcrad' not in request.session:
        return redirect(reverse('login'))
    idcrad = request.session['idcrad']
    name = request.session['name']
    lastname = request.session['lastname']
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    return render(request, 'home.html', {'idcrad': idcrad, 'name': name, 'lastname': lastname, 'Qtype': Qtype, 'Qloca': Qloca})

def tool_show(request):
    if 'idcrad' not in request.session:
        return redirect(reverse('login'))
    if request.method == 'POST':
        kw = request.POST.get('name', '')
        form = searchform(request.POST, initial={'name': kw})
    else:
        kw = request.GET.get('name', '')
        form = searchform(initial={'name': kw})
    data = Item.objects.filter(Q(idtype__contains=kw) | Q(name__contains=kw) | Q(
        status__contains=kw) | Q(serial__contains=kw) | Q(location__contains=kw))
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    name = request.session['name']
    lastname = request.session['lastname']
    return render(request, 'tool-show.html', {'name': name, 'lastname': lastname, 'form': form, 'data': data, 'Qtype': Qtype, 'Qloca': Qloca})

def tool_att(request, id):
    if request.method == 'POST':
        row = Item.objects.filter(id=id)
        SC = attribute.objects.filter(iditem=id)
    else:
        row = Item.objects.filter(id=id)
        SC = attribute.objects.filter(iditem=id)
    name = request.session['name']
    lastname = request.session['lastname']
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    iditem = id
    return render(request, 'tool-att.html', {'row': row, 'SC': SC, 'name': name, 'lastname': lastname, 'iditem': iditem, 'Qtype': Qtype, 'Qloca': Qloca})

def tool_delete(request, id):
    Item.objects.get(id=id).delete()
    return redirect('tool_show')
    #return render(request, 'tool-show.html', {'data': data, 'name': name, 'lastname': lastname, 'Qtype': Qtype, 'Qloca': Qloca})
def tool_attdel(request, id):
    SC = attribute.objects.get(idatt=id)
    SC.delete()
    return redirect('tool_att',id=SC.iditem)
    #return render(request, 'tool-attdel.html', {'SC': SC})
def addatt(request):
    iditem = request.POST['iditem']
    attname = request.POST['attname']
    value = request.POST['value']
    form = attribute.objects.create(
        iditem=iditem,
        attname=attname,
        value=value
    )
    form.save()
    return redirect('tool_att',id=iditem)
    #return render(request, 'tool-creatt.html', {'iditem': iditem})
def tool_create(request):
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    name = request.session['name']
    lastname = request.session['lastname']
    return render(request, 'tool-create.html', {'Qtype': Qtype, 'Qloca': Qloca, 'name': name, 'lastname': lastname})

def tool_update(request, id):
    # ถ้ามีข้อมูลจากฟอร์มถูกส่งเข้ามาด้วยเมธอด POST
    if request.method == 'POST':
        # อ่านข้อมูลเดิม
        row = Item.objects.get(id=id)   # get_object_or_404(Employee, id=id)

        # กำหนดข้อมูลเดิมให้กับโมเดลฟอร์ม เพื่อเปรียบเทียบกับข้อมูลใหม่ที่รับเข้ามา
        #ใช้form = ToolForm(instance=row, data=request.POST)
        # ถ้าข้อมูลทั้งหมดถูกต้อง
        # ใช้if form.is_valid():
        # บันทึกการเปลี่ยนแปลงลงในฟิลด์ต่างๆ
        # ใช้form.save()
    else:
        # ถ้าไม่มีข้อมูลส่งจากโมเดลฟอร์มเข้ามา
        # ให้อ่านข้อมูลเดิม เพื่อนำไปกำหนดเป็นค่าเริ่มแรกของอินพุทแต่ละอัน
        # วิธีที่ 1
        row = Item.objects.get(id=id)
        #ใช้form = ToolForm(initial=row.__dict__)
        # วิธีที่ 2
        #rows = Employee.objects.filter(id=id).values()
        #form = EmployeeForm(initial=rows[0])
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    name = request.session['name']
    lastname = request.session['lastname']
    return render(request, 'tool-update.html', {'row': row, 'Qtype': Qtype, 'Qloca': Qloca, 'name': name, 'lastname': lastname, })

def uptool(request):
    id = request.POST['id']
    Vserial = request.POST['serial']
    name = request.POST['name']
    idtype = request.POST['idtype']
    location = request.POST['location']
    status = request.POST['status']
    details = request.POST['details']
    price = request.POST['price']
    date = request.POST['date']
    pricetype = request.POST['pricetype']
    acquisition=request.POST['acquisition']


    if Item.objects.filter(serial=Vserial).exists() :
        if Vserial == "" :
            Item.objects.filter(id=id).update(serial=Vserial)
            Item.objects.filter(id=id).update(name=name)
            Item.objects.filter(id=id).update(idtype=idtype)
            Item.objects.filter(id=id).update(location=location)
            Item.objects.filter(id=id).update(status=status)
            Item.objects.filter(id=id).update(details=details)
            Item.objects.filter(id=id).update(price=price)
            Item.objects.filter(id=id).update(date=date)
            Item.objects.filter(id=id).update(pricetype=pricetype)
            Item.objects.filter(id=id).update(acquisition=acquisition)
        elif Vserial == request.POST['Vserial'] :
            Item.objects.filter(id=id).update(serial=Vserial)
            Item.objects.filter(id=id).update(name=name)
            Item.objects.filter(id=id).update(idtype=idtype)
            Item.objects.filter(id=id).update(location=location)
            Item.objects.filter(id=id).update(status=status)
            Item.objects.filter(id=id).update(details=details)
            Item.objects.filter(id=id).update(price=price)
            Item.objects.filter(id=id).update(date=date)
            Item.objects.filter(id=id).update(pricetype=pricetype)
            Item.objects.filter(id=id).update(acquisition=acquisition)
        else:
            print("เลขทะเบียน ซ้ำ !!!!")
            messages.info(request,"เลขทะเบียน ซ้ำ !!!!")
            return redirect('tool_update',id=id)
    else : 
        Item.objects.filter(id=id).update(serial=Vserial)
        Item.objects.filter(id=id).update(name=name)
        Item.objects.filter(id=id).update(idtype=idtype)
        Item.objects.filter(id=id).update(location=location)
        Item.objects.filter(id=id).update(status=status)
        Item.objects.filter(id=id).update(details=details)
        Item.objects.filter(id=id).update(price=price)
        Item.objects.filter(id=id).update(date=date)
        Item.objects.filter(id=id).update(pricetype=pricetype)
        Item.objects.filter(id=id).update(acquisition=acquisition)
   
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    name = request.session['name']
    lastname = request.session['lastname']
    return render(request, 'result.html', {'Qtype': Qtype, 'Qloca': Qloca, 'name': name, 'lastname': lastname})

def addtool(request):
    serial = request.POST['serial']
    name = request.POST['name']
    idtype = request.POST['idtype']
    location = request.POST['location']
    status = request.POST['status']
    details = request.POST['details']
    price = request.POST['price']
    date = request.POST['date']
    pricetype = request.POST['pricetype']
    acquisition=request.POST['acquisition']

    if Item.objects.filter(serial=serial).exists() :
        if serial=="" :
            tools = Item.objects.create(
                serial=serial,
                name=name,
                idtype=idtype,
                location=location,
                status=status,
                details=details,
                price=price,
                date=date,
                pricetype=pricetype,
                acquisition=acquisition
                )
            tools.save()
        else:
            print("เลขทะเบียน ซ้ำ !!!!")
            messages.info(request,"เลขทะเบียน ซ้ำ !!!!")
            return redirect('/tool/create')
    else :
        tools = Item.objects.create(
            serial=serial,
            name=name,
            idtype=idtype,
            location=location,
            status=status,
            details=details,
            price=price,
            date=date,
            pricetype=pricetype,
            acquisition=acquisition
            )
        tools.save()    
    return redirect('tool/show/')
    #return render(request, 'result.html', {'Qtype': Qtype, 'Qloca': Qloca, 'name': name, 'lastname': lastname})

#---------------------------------------type----------------------------------------------#
def tool_type(request, idtype):
    if request.method == 'POST':
        kw = request.POST.get('name', '')
        form = searchform(request.POST, initial={'name': kw})
    else:
        kw = request.GET.get('name', idtype)
        form = searchform(initial={'name': kw})
    data = Item.objects.filter(Q(idtype__contains=kw) | Q(name__contains=kw) | Q(
        status__contains=kw) | Q(serial__contains=kw) | Q(location__contains=kw))
    name = request.session['name']
    lastname = request.session['lastname']
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    return render(request, 'tool-show.html', {'name': name, 'lastname': lastname, 'form': form, 'data': data, 'Qtype': Qtype, 'Qloca': Qloca})

def typeshow(request):
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    name = request.session['name']
    lastname = request.session['lastname']
    return render(request, 'typeshow.html', {'name': name, 'lastname': lastname, 'Qtype': Qtype, 'Qloca': Qloca})

def typecreate(request):
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    name = request.session['name']
    lastname = request.session['lastname']
    return render(request, 'typecreate.html', {'Qtype': Qtype, 'Qloca': Qloca, 'name': name, 'lastname': lastname})

def typedel(request, id):
    Type.objects.get(idtype=id).delete()
    return redirect('typeshow')

def addtype(request):
    idtype = request.POST['idtype']
    typecode = request.POST['typecode']
    typedetails = request.POST['typedetails']
    if Type.objects.filter(idtype=idtype).exists() :
        print("เลขทะเบียน ซ้ำ !!!!")
        messages.info(request,"ชื่อประเภท ซ้ำ !!!!")
        return redirect('typecreate')
    elif Type.objects.filter(typecode=typecode).exists() :
        print("เลขทะเบียน ซ้ำ !!!!")
        messages.info(request,"รหัสประเภท ซ้ำ !!!!")
        return redirect('typecreate')    
    else :
        type = Type.objects.create(
            idtype=idtype,
            typecode=typecode,
            typedetails=typedetails
            )
        type.save()    
    return redirect('typeshow')
#---------------------------------------location----------------------------------------------#
def tool_loca(request, loca):
    if request.method == 'POST':
        kw = request.POST.get('name', '')
        form = searchform(request.POST, initial={'name': kw})
    else:
        kw = request.GET.get('name', loca)
        form = searchform(initial={'name': kw})
    data = Item.objects.filter(Q(idtype__contains=kw) | Q(name__contains=kw) | Q(
        status__contains=kw) | Q(serial__contains=kw) | Q(location__contains=kw))
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    name = request.session['name']
    lastname = request.session['lastname']
    return render(request, 'tool-show.html', {'name': name, 'lastname': lastname, 'form': form, 'data': data, 'Qtype': Qtype, 'Qloca': Qloca})

def locashow(request):
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    name = request.session['name']
    lastname = request.session['lastname']
    return render(request, 'locashow.html', {'name': name, 'lastname': lastname, 'Qtype': Qtype, 'Qloca': Qloca})

def locacreate(request):
    if request.method == 'POST':
        form = locaform(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = locaform()
    name = request.session['name']
    lastname = request.session['lastname']
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    return render(request, 'locacreate.html', {'form': form, 'name': name, 'lastname': lastname, 'Qtype': Qtype, 'Qloca': Qloca})

def locadel(request, id):
    Location.objects.get(location=id).delete()
    return redirect('locashow')

def addloca(request):
    location = request.POST['location']
    namelocation = request.POST['namelocation']
    if Location.objects.filter(location=location).exists() :
        print("ชื่อสถานที่ ซ้ำ !!!!")
        messages.info(request,"ชื่อสถานที่ ซ้ำ !!!!")
        return redirect('locacreate')
    else :
        loca = Location.objects.create(
            location=location,
            namelocation=namelocation,
            )
        loca.save()    
    return redirect('locashow')
#---------------------------------------status----------------------------------------------#
def tool_status1(request):
    if request.method == 'POST':
        kw = request.POST.get('name', '')
        form = searchform(request.POST, initial={'name': kw})
    else:
        kw = request.GET.get('name', 'ใช้งานปกติ')
        form = searchform(initial={'name': kw})
    data = Item.objects.filter(Q(name__contains=kw) | Q(status__contains=kw) | Q(
        serial__contains=kw) | Q(location__contains=kw))
    name = request.session['name']
    lastname = request.session['lastname']
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    return render(request, 'tool-show.html', {'name': name, 'lastname': lastname, 'form': form, 'data': data, 'Qtype': Qtype, 'Qloca': Qloca})

def tool_status2(request):
    if request.method == 'POST':
        kw = request.POST.get('name', '')
        form = searchform(request.POST, initial={'name': kw})
    else:
        kw = request.GET.get('name', 'ส่งคลัง ใช้งานได้')
        form = searchform(initial={'name': kw})
    data = Item.objects.filter(Q(name__contains=kw) | Q(status__contains=kw) | Q(
        serial__contains=kw) | Q(location__contains=kw))
    name = request.session['name']
    lastname = request.session['lastname']
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    return render(request, 'tool-show.html', {'name': name, 'lastname': lastname, 'form': form, 'data': data, 'Qtype': Qtype, 'Qloca': Qloca})

def tool_status3(request):
    if request.method == 'POST':
        kw = request.POST.get('name', '')
        form = searchform(request.POST, initial={'name': kw})
    else:
        kw = request.GET.get('name', 'ส่งคลัง ชำรุด')
        form = searchform(initial={'name': kw})
    data = Item.objects.filter(Q(name__contains=kw) | Q(status__contains=kw) | Q(
        serial__contains=kw) | Q(location__contains=kw))
    name = request.session['name']
    lastname = request.session['lastname']
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    return render(request, 'tool-show.html', {'name': name, 'lastname': lastname, 'form': form, 'data': data, 'Qtype': Qtype, 'Qloca': Qloca, })

def tool_status4(request):
    if request.method == 'POST':
        kw = request.POST.get('name', '')
        form = searchform(request.POST, initial={'name': kw})
    else:
        kw = request.GET.get('name', 'รอจำหน่าย')
        form = searchform(initial={'name': kw})
    data = Item.objects.filter(Q(name__contains=kw) | Q(status__contains=kw) | Q(
        serial__contains=kw) | Q(location__contains=kw))
    name = request.session['name']
    lastname = request.session['lastname']
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    return render(request, 'tool-show.html', {'name': name, 'lastname': lastname, 'form': form, 'data': data, 'Qtype': Qtype, 'Qloca': Qloca, })

def tool_status5(request):
    if request.method == 'POST':
        kw = request.POST.get('name', '')
        form = searchform(request.POST, initial={'name': kw})
    else:
        kw = request.GET.get('name', 'จำหน่ายแล้ว')
        form = searchform(initial={'name': kw})
    data = Item.objects.filter(Q(name__contains=kw) | Q(status__contains=kw) | Q(
        serial__contains=kw) | Q(location__contains=kw))
    name = request.session['name']
    lastname = request.session['lastname']
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    return render(request, 'tool-show.html', {'name': name, 'lastname': lastname, 'form': form, 'data': data, 'Qtype': Qtype, 'Qloca': Qloca, })

def tool_status6(request):
    if request.method == 'POST':
        kw = request.POST.get('name', '')
        form = searchform(request.POST, initial={'name': kw})
    else:
        kw = request.GET.get('name', 'อื่นๆ')
        form = searchform(initial={'name': kw})
    data = Item.objects.filter(Q(name__contains=kw) | Q(status__contains=kw) | Q(
        serial__contains=kw) | Q(location__contains=kw))
    name = request.session['name']
    lastname = request.session['lastname']
    Qtype = Type.objects.all()
    Qloca = Location.objects.all()
    return render(request, 'tool-show.html', {'name': name, 'lastname': lastname, 'form': form, 'data': data, 'Qtype': Qtype, 'Qloca': Qloca, })
#---------------------------------------Empcreate----------------------------------------------#
def Empcreate(request):
    if request.method == 'POST':
        form = EmpcreateForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EmpcreateForm()
    return render(request, 'Empcreate.html', {'form': form})
#---------------------------------------Reprot----------------------------------------------#
def item_CSV(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=itemattall.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    item= Item.objects.all()
    num =0
    writer.writerow(['ลำดับที่','serial','name', 'location', 'status', 'idtype' , 'details','id'])
    for item in item:
        num += 1
        writer.writerow([num,item.serial,item.name,item.location,item.status,item.idtype,item.details,item.id])
        att=attribute.objects.filter(iditem=item.id)
        for att in att:
            writer.writerow(['',att.attname,att.value])
        writer.writerow('')
    return response

def item_Rpitem(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=itemall.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    item= Item.objects.all()
    num =0
    writer.writerow(['ลำดับที่','serial','name', 'location', 'status', 'idtype' , 'details','id'])
    for item in item:
        num += 1
        writer.writerow([num,item.serial,item.name,item.location,item.status,item.idtype,item.details,item.id])
    return response