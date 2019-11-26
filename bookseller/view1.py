# Create your views here.

# -*- coding: utf-8 -*-
 
from django.shortcuts import render,redirect
from django.views.decorators import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from TestModel.models import *
from django.urls import reverse
from datetime import date
import time
import datetime 
from django.db.models import Q
import hashlib

UserType='none'
UserID='000'
Manager_ID='000'
isbn='000'
bookid=0
p=0
n=0
pur=0

# 接收POST请求数据

#登陆界面
def log_in(request):
    global UserType,UserID
    ctx ={}
    ans ={}
    if request.POST:
        ctx['type'] = request.POST['usertype']
        ctx['name'] = request.POST['username']
        ctx['pass'] = request.POST['password']
        if ctx['type']=='customer':
            temp=Customer.objects.filter(Cus_ID=ctx['name'])
            leng=len(temp)
            if leng>0: 
                ans['status']=1#用户名存在
            else:
                ans['status']=0
            if ans['status']==1:
                passw=Customer.objects.filter(Cus_ID=ctx['name']).values("password")
                for passwo in passw:
                    hash = hashlib.md5()  #创建md5()加密实例
                    hash.update(bytes(ctx["pass"], encoding='utf-8'))  #对admin字符进行加密
                    key=hash.hexdigest() #返回产生的十六进制的bytes
                    print(key)
                    if key==passwo["password"]:
                           ans['ispass']=1 #密码核实正确，是顾客
                           UserType='customer'
                           UserID=ctx['name'] #传回顾客ID
                           return HttpResponseRedirect(reverse('showall'))
                    else:
                           ans['ispass']=0
        elif ctx['type']=='manager':
            temp=Manager.objects.filter(Mana_ID=ctx['name'])
            leng=len(temp)
            if leng>0: 
                ans['status']=1#用户名存在
            else:
                ans['status']=0
            if ans['status']==1:
                passw=Manager.objects.filter(Mana_ID=ctx['name']).values("password")
                for passwo in passw:
                    hash = hashlib.md5()  #创建md5()加密实例
                    hash.update(bytes(ctx["pass"], encoding='utf-8'))  #对admin字符进行加密
                    key=hash.hexdigest() #返回产生的十六进制的bytes
                    if key==passwo["password"]:
                         ans['ispass']=1 #密码正确，是管理员
                    else:
                         ans['ispass']=0
                    if ans['ispass']==1:
                        issuper=Manager.objects.filter(Mana_ID=ctx['name']).values("supera")
                        for s in issuper:
                            if s["supera"]==1:
                                UserType='supermanager'
                                UserID=ctx['name']
                                ans['super']=1 #是超级管理员
                            else:
                                UserType='manager'
                                UserID=ctx['name']
                                ans['super']=0
                        return HttpResponseRedirect(reverse('entermanager'))
    return render(request,"home.html",ans)

#顾客注册界面
def sign_up(request):
    ctx={}
    ans={}
    if request.POST:
        ctx['name'] = request.POST['username']
        temp=Customer.objects.filter(Cus_ID=ctx['name'])
        leng=len(temp)
        if leng>0: 
            ans['ex']=1      #用户名已存在
            ans['create']=0  #创建失败
        else:
            ans['ex']=0
        if ans['ex']==0:
            ctx['pass'] = request.POST['password']
            ctx['pass2'] = request.POST['password2']
            if ctx['pass']!=ctx['pass2']:
                ans['pass']=0  #两次密码不相等
                ans['create']=0 
            else:
                ans['pass']=1
                hash = hashlib.md5()  #创建md5()加密实例
                hash.update(bytes(ctx['pass'], encoding='utf-8'))  #对admin字符进行加密
                key=hash.hexdigest() #返回产生的十六进制的bytes
                cus_dict={"Cus_ID":ctx['name'],"password":key}
                Customer.objects.create(**cus_dict)
                ans['create']=1
    return render(request,"home.html",ans)

##显示所有书籍信息
def showall(request):
    global UserType,UserID
    ctx={}
    bookinfo=Book.objects.values("title","writer","press","price","discount","ISBN","image","num")
    for boo in bookinfo:
        boo["discount_price"]=round(boo["price"]*boo["discount"],2)
        boo["discount"]=boo["discount"]*10
        temp=Comment.objects.filter(ISBN=boo["ISBN"]).values("grade","description","customer_id_id") #查询每本书是否有评论
        #算出平均评分
        sum=0
        i=0
        for t in temp:
            sum=sum+t["grade"]
            i=i+1
        if i!=0:
            boo["grade"]=round(sum/i,2)
        else:
            boo["grade"]=0
        boo["star"]=boo["grade"]*20
        for t in temp:
            boo["comment"]=temp
    ctx["book_list"]=bookinfo
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    return render(request,"customer.html",ctx)

##查询书籍信息
def search(request):
    global UserType,UserID
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    if request.POST:
        t=request.POST['search_type']
        q=request.POST['question']
        if t=='ID':
            bookinfo=Book.objects.filter(Book_ID=q).values("title","writer","press","num","price","discount","ISBN","Book_ID","image")
        if t=='ISBN':
            bookinfo=Book.objects.filter(ISBN=q).values("title","writer","press","num","price","discount","ISBN","Book_ID","image")
        if t=='title':
            bookinfo=Book.objects.filter(title=q).values("title","writer","press","num","price","discount","ISBN","Book_ID","image")
        if t=='writer':
            bookinfo=Book.objects.filter(writer=q).values("title","writer","press","num","price","discount","ISBN","Book_ID","image")
        if t=='press':
            bookinfo=Book.objects.filter(press=q).values("title","writer","press","num","price","discount","ISBN","Book_ID","image")
        if not bookinfo:
            ctx["exist"]=0;
        else:
            for boo in bookinfo:
                boo["discount_price"]=round(boo["price"]*boo["discount"],2)
                boo["discount"]=boo["discount"]*10
                temp=Comment.objects.filter(ISBN_id=boo["ISBN"]).values("grade","description","customer_id_id")
                sum=0
                i=0
                for t in temp:
                    sum=sum+t["grade"]
                    i=i+1
                if i!=0:
                    boo["grade"]=round(sum/i,2)
                else:
                    boo["grade"]=0
                boo["star"]=boo["grade"]*20
                for t in temp:
                    boo["comment"]=temp
            ctx["book_list"]=bookinfo
    return render(request,"search.html",ctx)

##输入评论
def comment(request):
    global UserType,UserID
    ctx={}
    if UserType!='customer':
        return HttpResponse("<p>您无权访问此网页</p>")
    if 'ISBN' in request.GET and 'description' in request.POST:
        g=request.POST['grade']
        d=request.POST['description']
        isbn=request.GET["ISBN"]
        #添加一条评论
        comm_dict={"grade":g,"description":d,"ISBN_id":isbn,"customer_id_id":UserID}
        Comment.objects.create(**comm_dict)
        bookinfo=Book.objects.filter(ISBN=isbn).values("title","writer","press","price","discount","ISBN","image")
        for boo in bookinfo:
            boo["discount_price"]=round(boo["price"]*boo["discount"],2)
            boo["discount"]=boo["discount"]*10
            temp=Comment.objects.filter(ISBN_id=boo["ISBN"]).values("grade","description","customer_id_id")
            sum=0
            i=0
            for t in temp:
                sum=sum+t["grade"]
                i=i+1
            if i!=0:
                boo["grade"]=round(sum/i,2)
            else:
                boo["grade"]=0
            boo["star"]=boo["grade"]*20
            for t in temp:
                boo["comment"]=temp
        ctx["book_list"]=bookinfo
        ctx['UserType']=UserType
        ctx['UserID']=UserID
        return render(request,"comment.html",ctx)
    if 'ISBN' in request.GET:
     #通过点击图片进入界面
        isbn=request.GET['ISBN']
        #显示要评论的书的信息
        bookinfo=Book.objects.filter(ISBN=isbn).values("title","writer","press","price","discount","ISBN","image")
        for boo in bookinfo:
            boo["discount_price"]=round(boo["price"]*boo["discount"],2)
            boo["discount"]=boo["discount"]*10
            temp=Comment.objects.filter(ISBN_id=boo["ISBN"]).values("grade","description","customer_id_id")
            sum=0
            i=0
            for t in temp:
                sum=sum+t["grade"]
                i=i+1
            if i!=0:
                boo["grade"]=round(sum/i,2)
            else:
                boo["grade"]=0
            boo["star"]=boo["grade"]*20
            for t in temp:
                boo["comment"]=temp
        ctx["book_list"]=bookinfo
        ctx['UserType']=UserType
        ctx['UserID']=UserID
        return render(request,"comment.html",ctx)
    elif 'title' in request.POST:
        tit=request.POST['title']
        #通过点击评论来进入界面
        bookinfo=Book.objects.filter(title=tit).values("title","writer","press","price","discount","ISBN","image")
        for boo in bookinfo:
            boo["discount_price"]=round(boo["price"]*boo["discount"],2)
            boo["discount"]=boo["discount"]*10
            temp=Comment.objects.filter(ISBN_id=boo["ISBN"]).values("grade","description","customer_id_id")
            sum=0
            i=0
            for t in temp:
                sum=sum+t["grade"]
                i=i+1
            if i!=0:
                boo["grade"]=round(sum/i,2)
            else:
                boo["grade"]=0
            boo["star"]=boo["grade"]*20
            for t in temp:
                boo["comment"]=temp
        ctx["book_list"]=bookinfo
        ctx['UserType']=UserType
        ctx['UserID']=UserID
        return render(request,"comment.html",ctx)
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    return render(request,"comment.html",ctx)

#雇佣普通管理员
def manager_register(request):
    global UserType,UserID
    if UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    if request.POST:
        hash = hashlib.md5()  #创建md5()加密实例
        hash.update(bytes(request.POST["password"], encoding='utf-8'))  #对admin字符进行加密
        key=hash.hexdigest() #返回产生的十六进制的bytes
        manainfo=Manager.objects.values("Mana_ID","username","name","gender","age","password")
        for m in manainfo:
            if m["Mana_ID"]==request.POST["Mana_ID"]:
                ctx["exist"]=1
                return render(request,"manager_signup.html",ctx)
        mana_dict={"Mana_ID":request.POST["Mana_ID"],"username":request.POST["username"],"password":key,"name":request.POST["name"],"gender":request.POST["gender"],"age":request.POST["age"],"supera":0}
        Manager.objects.create(**mana_dict)
    return render(request,"manager_signup.html",ctx)

#解雇普通管理员
def manager_delete(request):
    global UserType,UserID
    if UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    if UserType=="supermanager":
        if "Mana_ID" in request.POST:
            manainfo=Manager.object.filter(Mana_ID=request.POST["Mana_ID"]).values("Mana_ID","username","password","name","gender","age","supera","password")
            ctx["manainfo"]=manainfo
            return render(request,"fire.html",ctx)
        elif "Mana_ID" in request.GET:
            Manager.objects.filter(Mana_ID=request.GET["Mana_ID"]).delete()
        else:
            manainfo=Manager.objects.filter(supera=0).values("Mana_ID","username","password","name","gender","age","supera","password")
            ctx["manainfo"]=manainfo
    return render(request,"fire.html",ctx)

##进入管理员界面
def entermanager(request):
    global UserType,UserID
    if UserType!='supermanager'and UserType!='manager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    #库存小于10的做低库存提示
    bookinfo=Book.objects.filter(num__lte=10).values("Book_ID","num","title")
    ctx["bookinfo"]=bookinfo
    return render(request,"manager.html",ctx)

#超级管理员查看所有用户资料
def superview_info(request):
    global UserType,UserID
    if UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    #判断是不是超级管理员
    if UserType=='supermanager':
        #超级管理员信息
        superinfo=Manager.objects.filter(supera=1).values("Mana_ID","username","password","name","gender","age","supera","password")
        ctx["super1"]=superinfo[0]
        ctx["super2"]=superinfo[1]
        ctx["super3"]=superinfo[2]
        #普通管理员
        ctx["manainfo"]=Manager.objects.filter(supera=0).values("Mana_ID","username","password","name","gender","age","supera","password")
    return render(request,"view_info.html",ctx)

#超级管理员修改用户资料
def superchange_info(request):
    global UserType,UserID
    if UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    #判断是不是超级管理员
    if UserType=="supermanager":
        if "Mana_ID" in request.POST:
            i=request.POST["Mana_ID"]
            manainfo=Manager.objects.filter(Mana_ID=i).values("Mana_ID","username","password","name","gender","age","supera","password")
            ctx["manainfo"]=manainfo
            return render(request,"superchange_info.html",ctx)
        else:
             manainfo=Manager.objects.filter(supera=0).values("Mana_ID","username","password","name","gender","age","supera","password")
             ctx["manainfo"]=manainfo
             return render(request,"superchange_info.html",ctx)

def change_info(request):
    global UserType,UserID,Manager_ID
    if UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    if "Mana_ID" in request.GET:
        Manager_ID=request.GET["Mana_ID"]
        manainfo=Manager.objects.filter(Mana_ID=Manager_ID).values("Mana_ID","username","password","name","gender","age","supera")
        ctx["manainfo"]=manainfo
    if "Mana_ID" in request.POST:
            if request.POST["Mana_ID"]!='':
                Manager.objects.filter(Mana_ID=Manager_ID).update(Mana_ID=request.POST["Mana_ID"])
            if request.POST["username"]!='':
                Manager.objects.filter(Mana_ID=Manager_ID).update(username=request.POST["username"])
            if request.POST["password"]!='':
                hash = hashlib.md5()  #创建md5()加密实例
                hash.update(bytes(request.POST["password"],encoding='utf-8'))  #对admin字符进行加密
                key=hash.hexdigest() #返回产生的十六进制的bytes
                Manager.objects.filter(Mana_ID=Manager_ID).update(password=key)
            if request.POST["name"]!='':
                Manager.objects.filter(Mana_ID=Manager_ID).update(name=request.POST["name"])
            if request.POST["gender"]!='':
                Manager.objects.filter(Mana_ID=Manager_ID).update(gender=request.POST["gender"])
            if request.POST["age"]!='':
                Manager.objects.filter(Mana_ID=Manager_ID).update(age=request.POST["age"])
            manainfo=Manager.objects.filter(Mana_ID=Manager_ID).values("Mana_ID","username","password","name","gender","age","supera")
            ctx["manainfo"]=manainfo
            return render(request,"change_info.html",ctx)
    return render(request,"change_info.html",ctx)



##管理员查询修改自己的信息
def commonchange_info(request):
    global UserType,UserID
    if UserType!='supermanager'and UserType!='manager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    if request.POST:
        if request.POST["Mana_ID"]!='':
            Manager.objects.filter(Mana_ID=UserID).update(Mana_ID=request.POST["Mana_ID"])
        if request.POST["username"]!='':
            Manager.objects.filter(Mana_ID=UserID).update(username=request.POST["username"])
        if request.POST["password"]!='':
                hash = hashlib.md5()  #创建md5()加密实例
                hash.update(bytes(request.POST["password"],encoding='utf-8'))  #对admin字符进行加密
                key=hash.hexdigest() #返回产生的十六进制的bytes
                Manager.objects.filter(Mana_ID=Manager_ID).update(password=key)
        if request.POST["name"]!='':
            Manager.objects.filter(Mana_ID=UserID).update(name=request.POST["name"])
        if request.POST["gender"]!='':
            Manager.objects.filter(Mana_ID=UserID).update(gender=request.POST["gender"])
        if request.POST["age"]!='':
            Manager.objects.filter(Mana_ID=UserID).update(age=request.POST["age"])
    manainfo=Manager.objects.filter(Mana_ID=UserID).values("Mana_ID","username","password","name","gender","age","supera")
    ctx["manainfo"]=manainfo
    return render(request,"commonchange_info.html",ctx)

#图书信息修改
def changebook_info(request):
    global UserType,UserID
    if UserType!='supermanager'and UserType!='manager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    if request.POST:
        t=request.POST['search_type']
        q=request.POST['question']
        if t=='ISBN':
            bookinfo=Book.objects.filter(ISBN=q).values("ISBN","Book_ID","title","writer","press","price","num","discount","image")
            for boo in bookinfo:
                boo["discount"]=boo["discount"]*10
            ctx["book_list"]=bookinfo
            return render(request,"bookchange1.html",ctx)
        if t=='Book_ID':
            bookinfo=Book.objects.filter(Book_ID=q).values("ISBN","Book_ID","title","writer","press","price","num","discount","image")
            for boo in bookinfo:
                boo["discount"]=boo["discount"]*10
            ctx["book_list"]=bookinfo
            return render(request,"bookchange1.html",ctx)
        if t=='title':
            bookinfo=Book.objects.filter(title=q).values("ISBN","Book_ID","title","writer","press","price","num","discount","image")
            for boo in bookinfo:
                boo["discount"]=boo["discount"]*10
            ctx["book_list"]=bookinfo
            return render(request,"bookchange1.html",ctx)
    else:
            bookinfo=Book.objects.values("ISBN","Book_ID","title","writer","press","price","num","discount","image")
            for boo in bookinfo:
                boo["discount"]=boo["discount"]*10
            ctx["book_list"]=bookinfo
            return render(request,"bookchange1.html",ctx)

def bookchange_info(request):
    global UserType,UserID,isbn
    if UserType!='supermanager'and UserType!='manager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    if "ISBN" in request.GET:
        isbn=request.GET["ISBN"]
        bookinfo=Book.objects.filter(ISBN=isbn).values("title","writer","press","price","discount","image")
        for boo in bookinfo:
            boo["discount"]=boo["discount"]*10
        ctx["book_list"]=bookinfo
    if "title" in request.POST:
            if request.POST["title"]!='':
                Book.objects.filter(ISBN=isbn).update(title=request.POST["title"])
            if request.POST["writer"]!='':
                Book.objects.filter(ISBN=isbn).update(writer=request.POST["writer"])
            if request.POST["press"]!='':
                Book.objects.filter(ISBN=isbn).update(press=request.POST["press"])
            if request.POST["price"]!='':
                Book.objects.filter(ISBN=isbn).update(price=request.POST["price"])
            if request.POST["discount"]!='':
                Book.objects.filter(ISBN=isbn).update(discount=request.POST["discount"])
            if request.POST["image"]!='':
                Book.objects.filter(ISBN=isbn).update(image=request.POST["image"])
            bookinfo=Book.objects.filter(ISBN=isbn).values("ISBN","Book_ID","title","writer","press","price","num","discount","image")
            for boo in bookinfo:
                boo["discount"]=boo["discount"]*10
            ctx["book_list"]=bookinfo
    return render(request,"bookchange2.html",ctx)

    

#若库存为0,则删除该书
def book_delete(request):
    global UserType,UserID,isbn
    if UserType!='supermanager'and UserType!='manager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    if "ISBN" in request.GET:
        isbn=request.GET["ISBN"]
        Book.objects.filter(ISBN=isbn).delete()
        bookinfo=Book.objects.values("ISBN","Book_ID","title","writer","press","price","num","purchase","discount","image")
        for boo in bookinfo:
                boo["discount"]=boo["discount"]*10
        ctx["book_list"]=bookinfo
    return render(request,"bookchange1.html",ctx)   

#顾客购买函数
def buy(request):
    global UserType,UserID,isbn
    if UserType!='customer':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID  
    if request.POST:
        t=request.POST['search_type']
        q=request.POST['question']
        if t=='ID':
            bookinfo=Book.objects.filter(Book_ID=q).values("title","writer","press","price","discount","ISBN","image","num")
        if t=='ISBN':
            bookinfo=Book.objects.filter(ISBN=q).values("title","writer","press","price","discount","ISBN","image","num")
        if t=='title':
            bookinfo=Book.objects.filter(title=q).values("title","writer","press","price","discount","ISBN","image","num")
        if t=='writer':
            bookinfo=Book.objects.filter(writer=q).values("title","writer","press","price","discount","ISBN","image","num")
        if t=='press':
            bookinfo=Book.objects.filter(press=q).values("title","writer","press","price","discount","ISBN","image","num")
        for boo in bookinfo:
            boo["discount_price"]=round(boo["price"]*boo["discount"],2)
            boo["discount"]=boo["discount"]*10
            temp=Comment.objects.filter(ISBN_id=boo["ISBN"]).values("grade","description","customer_id_id") #查询每本书是否有评论
            #算出平均评分
            sum=0
            i=0
            for t in temp:
                sum=sum+t["grade"]
                i=i+1
            if i!=0:
                boo["grade"]=round(sum/i,2)
            else:
                boo["grade"]=0
            boo["star"]=boo["grade"]*20
            for t in temp:
                boo["comment"]=temp
        ctx["book_list"]=bookinfo
        return render(request,"buy.html",ctx)
    else:
        bookinfo=Book.objects.values("title","writer","press","price","discount","ISBN","image","num")
        for boo in bookinfo:
            boo["discount_price"]=round(boo["price"]*boo["discount"],2)
            boo["discount"]=boo["discount"]*10
            temp=Comment.objects.filter(ISBN_id=boo["ISBN"]).values("grade","description","customer_id_id") #查询每本书是否有评论
            #算出平均评分
            sum=0
            i=0
            for t in temp:
                sum=sum+t["grade"]
                i=i+1
            if i!=0:
                boo["grade"]=round(sum/i,2)
            else:
                boo["grade"]=0
            boo["star"]=boo["grade"]*20
            for t in temp:
                boo["comment"]=temp
        ctx["book_list"]=bookinfo
        return render(request,"buy.html",ctx)

def payment (request):
    global UserType,UserID,isbn
    if UserType!='customer':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID  
    if "ISBN" in request.GET:
        isbn=request.GET["ISBN"]
        bookinfo=Book.objects.filter(ISBN=isbn).values("title","writer","press","price","discount","ISBN","image","num")
        for boo in bookinfo:
            boo["discount_price"]=round(boo["price"]*boo["discount"],2)
            boo["discount"]=boo["discount"]*10
            temp=Comment.objects.filter(ISBN=boo["ISBN"]).values("grade","description","customer_id_id") #查询每本书是否有评论
                #算出平均评分
            sum=0
            i=0
            for t in temp:
                sum=sum+t["grade"]
                i=i+1
            if i!=0:
                boo["grade"]=round(sum/i,2)
            else:
                boo["grade"]=0
            boo["star"]=boo["grade"]*20
            for t in temp:
                boo["comment"]=temp
        ctx["book_list"]=bookinfo 
        return render(request,"payment.html",ctx)
    if "num" in request.GET:
        n1= int(request.GET["num"])
        bookinfo=Book.objects.filter(ISBN=isbn).values("num","price")
        for boo in bookinfo:
            n2=boo["num"]
            p=boo["price"]
        if n1>n2:
            bookinfo=Book.objects.filter(ISBN=isbn).values("title","writer","press","price","discount","ISBN","image","num")
            for boo in bookinfo:
                boo["discount_price"]=round(boo["price"]*boo["discount"],2)
                boo["discount"]=boo["discount"]*10
                temp=Comment.objects.filter(ISBN=boo["ISBN"]).values("grade","description","customer_id_id") #查询每本书是否有评论
                    #算出平均评分
                sum=0
                i=0
                for t in temp:
                    sum=sum+t["grade"]
                    i=i+1
                if i!=0:
                    boo["grade"]=round(sum/i,2)
                else:
                    boo["grade"]=0
                boo["star"]=boo["grade"]*20
                for t in temp:
                    boo["comment"]=temp
            ctx["book_list"]=bookinfo 
            ctx["warning"]=1
            return render(request,"payment.html",ctx)
        elif n1<=0:
            bookinfo=Book.objects.filter(ISBN=isbn).values("title","writer","press","price","discount","ISBN","image","num")
            for boo in bookinfo:
                boo["discount_price"]=round(boo["price"]*boo["discount"],2)
                boo["discount"]=boo["discount"]*10
                temp=Comment.objects.filter(ISBN=boo["ISBN"]).values("grade","description","customer_id_id") #查询每本书是否有评论
                    #算出平均评分
                sum=0
                i=0
                for t in temp:
                    sum=sum+t["grade"]
                    i=i+1
                if i!=0:
                    boo["grade"]=round(sum/i,2)
                else:
                    boo["grade"]=0
                boo["star"]=boo["grade"]*20
                for t in temp:
                    boo["comment"]=temp
            ctx["book_list"]=bookinfo 
            ctx["warning"]=2
            return render(request,"payment.html",ctx)
        else:
            ctx["warning"]=0
            if "sure" in request.GET:
                 if request.GET["sure"]=='1':
                       ctx["success"]=1
                       Book.objects.filter(ISBN=isbn).update(num=n2-n1)
                       bookinfo=Book.objects.filter(ISBN=isbn).values("title","writer","press","price","discount","ISBN","image","num")
                       for boo in bookinfo:
                            boo["discount_price"]=round(boo["price"]*boo["discount"],2)
                            ctx["total_price"]=round(boo["discount_price"]*n1,2)  
                            test1 = Account(price=boo["discount_price"],state=1,number=n1,ISBN=isbn)
                            test1.save()
                       return render(request,"payment.html",ctx)
                 if request.GET["sure"]=='0':
                       ctx["warning"]=3
                       bookinfo=Book.objects.filter(ISBN=isbn).values("title","writer","press","price","discount","ISBN","image","num")
                       for boo in bookinfo:
                            boo["discount_price"]=round(boo["price"]*boo["discount"],2)
                            boo["discount"]=boo["discount"]*10
                            temp=Comment.objects.filter(ISBN=boo["ISBN"]).values("grade","description","customer_id_id") #查询每本书是否有评论
                            sum=0
                            i=0
                            for t in temp:
                                sum=sum+t["grade"]
                                i=i+1
                            if i!=0:
                                boo["grade"]=round(sum/i,2)
                            else:
                                boo["grade"]=0
                            boo["star"]=boo["grade"]*20
                            for t in temp:
                                boo["comment"]=temp
                       ctx["book_list"]=bookinfo 
                       return render(request,"payment.html",ctx)
            else:
                bookinfo=Book.objects.filter(ISBN=isbn).values("title","writer","press","price","discount","ISBN","image","num")
                for boo in bookinfo:
                         boo["discount_price"]=round(boo["price"]*boo["discount"],2)
                ctx["total_price"]=round(boo["discount_price"]*n1,2)  
                ctx["num"]=n1
                return render(request,"payment.html",ctx)

#看账单
def viewaccount3(request):
    global UserType,UserID
    if UserType!='manager'and UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID 
    ctx["choice"]=3
        #显示总账单
    if request.POST:
                d1=request.POST["date1"]
                date1 = datetime.datetime.strptime(d1,'%Y-%m-%d')
                d2=request.POST["date2"]
                date2 = datetime.datetime.strptime(d2,'%Y-%m-%d')
                accountinfo=Account.objects.filter(dt__gte=date1).filter(dt__lte=date2).values("id","price","state","number","ISBN","dt")
                for a in accountinfo:
                    a["total"]=round(a["price"]*a["number"],2)
                accountinfo0=Account.objects.filter(state=0).filter(dt__gte=date1).filter(dt__lte=date2).values("price","number")
                sum0=0
                sum1=0
                for a in accountinfo0:
                    sum0=sum0+a["price"]*a["number"]
                ctx["total_expenditure"]=round(sum0,2)
                accountinfo1=Account.objects.filter(state=1).filter(dt__gte=date1).filter(dt__lte=date2).values("price","number")
                for a in accountinfo1:
                    sum1=sum1+a["price"]*a["number"]
                ctx["account"]=accountinfo
                ctx["total_income"]=round(sum1,2)
                ctx["total_profit"]=round(sum1-sum0,2)
                return render(request,"account.html",ctx)
    else:
                accountinfo=Account.objects.values("id","price","state","number","ISBN","dt")
                accountinfo0=Account.objects.filter(state=0).values("price","number")
                accountinfo1=Account.objects.filter(state=1).values("price","number")
                for a in accountinfo:
                    a["total"]=round(a["price"]*a["number"],2)
                sum0=0
                sum1=0
                for a in accountinfo0:
                    sum0=sum0+a["price"]*a["number"]
                ctx["total_expenditure"]=sum0
                for a in accountinfo1:
                    sum1=sum1+a["price"]*a["number"]
                ctx["account"]=accountinfo
                ctx["total_income"]=round(sum1,2)
                ctx["total_profit"]=round(sum1-sum0,2)
                return render(request,"account.html",ctx)

def viewaccount2(request):
    global UserType,UserID
    if UserType!='manager'and UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID 
    ctx["choice"]=2
    #显示进货账单
    if request.POST:
                d1=request.POST["date1"]
                date1 = datetime.datetime.strptime(d1,'%Y-%m-%d')
                d2=request.POST["date2"]
                date2 = datetime.datetime.strptime(d2,'%Y-%m-%d')
                accountinfo0=Account.objects.filter(state=0).filter(dt__gte=date1).filter(dt__lte=date2).values("id","price","state","number","ISBN","dt")
                for a in accountinfo0:
                    a["total"]=round(a["price"]*a["number"],2)
                sum0=0
                for a in accountinfo0:
                    sum0=sum0+a["price"]*a["number"]
                ctx["total_expenditure"]=round(sum0,2)
                ctx["account"]=accountinfo0
                return render(request,"account.html",ctx)
    else:
                accountinfo0=Account.objects.filter(state=0).values("id","price","state","number","ISBN","dt")
                for a in accountinfo0:
                    a["total"]=round(a["price"]*a["number"],2)
                sum0=0
                for a in accountinfo0:
                    sum0=sum0+a["price"]*a["number"]
                ctx["total_expenditure"]=round(sum0,2)
                ctx["account"]=accountinfo0
                return render(request,"account.html",ctx)

def viewaccount1(request):
    global UserType,UserID
    if UserType!='manager'and UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID 
    ctx["choice"]=1
    #显示售书账单
    if request.POST:
                d1=request.POST["date1"]
                date1 = datetime.datetime.strptime(d1,'%Y-%m-%d')
                d2=request.POST["date2"]
                date2 = datetime.datetime.strptime(d2,'%Y-%m-%d')
                accountinfo1=Account.objects.filter(state=1).filter(dt__gte=date1).filter(dt__lte=date2).values("id","price","state","number","ISBN","dt")
                for a in accountinfo1:
                    a["total"]=round(a["price"]*a["number"],2)
                sum1=0
                for a in accountinfo1:
                    sum1=sum1+a["price"]*a["number"]
                ctx["total_income"]=round(sum1,2)
                ctx["account"]=accountinfo1
                return render(request,"account.html",ctx)
    else:
                accountinfo1=Account.objects.filter(state=1).values("id","price","state","number","ISBN","dt")
                for a in accountinfo1:
                    a["total"]=round(a["price"]*a["number"],2)
                sum1=0
                for a in accountinfo1:
                    sum1=sum1+a["price"]*a["number"]
                ctx["total_income"]=round(sum1,2)
                ctx["account"]=accountinfo1
                return render(request,"account.html",ctx)

#进货
def purchase(request):
    global UserType,UserID,bookid,p,n
    if UserType!='manager'and UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID 
    if "Book_ID"in request.POST:
        id=request.POST["Book_ID"]
        p=request.POST["purchase"]
        n=request.POST["number"]
        book_list=Book.objects.values("Book_ID")
        old=0
        for boo in book_list:
            if boo["Book_ID"]==id:
               old=1
        bookid=id
        if old==0:#告知是新书
           ctx["new"]=1
           list=PurchaseList.objects.values("id","purchase","number","state","Book_ID")
           for l in list:
                l["total"]=l["number"]*l["purchase"]
           ctx["list"]=list
           return render(request,"purchase.html",ctx)
        if old==1:#旧书
            pp=PurchaseList(Book_ID=id,purchase=p,number=n,state=0)
            pp.save()
            list=PurchaseList.objects.values("id","purchase","number","state","Book_ID")
            for l in list:
                l["total"]=l["number"]*l["purchase"]
            ctx["list"]=list
            ctx["add_success"]=1
            return render(request,"purchase.html",ctx)
    if "title" in request.GET:#添加新书
            pp=PurchaseList(Book_ID=bookid,purchase=p,number=n,state=0)
            pp.save()
            temp=tempbook.objects.filter(Book_ID=bookid).values("Book_ID")
            if len(temp)==0:
                tb=tempbook(ISBN=request.GET["ISBN"],Book_ID=bookid,title=request.GET["title"],writer=request.GET["writer"],press=request.GET["press"])
                tb.save()
            list=PurchaseList.objects.values("id","purchase","number","state","Book_ID")
            for l in list:
                l["total"]=l["number"]*l["purchase"]
            ctx["list"]=list
            ctx["add_success"]=1
            return render(request,"purchase.html",ctx)
    else:
        list=PurchaseList.objects.values("id","purchase","number","state","Book_ID")
        for l in list:
            l["total"]=l["number"]*l["purchase"]
        ctx["list"]=list
        return render(request,"purchase.html",ctx)

#付款
def pur_pay(request):
     global UserType,UserID
     if UserType!='manager'and UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
     ctx={}
     ctx['UserType']=UserType
     ctx['UserID']=UserID 
     if request.GET:
         PurchaseList.objects.filter(id=request.GET["id"]).update(state=1)
         list=PurchaseList.objects.values("id","purchase","number","state","Book_ID")
         for l in list:
             l["total"]=l["number"]*l["purchase"]
         ctx["list"]=list
         ctx["success"]=1
         purf=PurchaseList.objects.filter(id=request.GET["id"]).values("purchase","number","Book_ID")
         for x in purf:
             temp1=x["purchase"]
             temp2=x["number"]
             temp3=x["Book_ID"]
         book_list=Book.objects.values("Book_ID")
         old=0
         for boo in book_list:
            if boo["Book_ID"]==temp3:
               old=1
         if old==1:
             oldbook=Book.objects.filter(Book_ID=temp3).values("ISBN")
             for o in oldbook:
                 isbn=o["ISBN"]
         if old==0:
             newbook=tempbook.objects.filter(Book_ID=temp3).values("ISBN")
             for n in newbook:
                 isbn=n["ISBN"]
         a=Account(price=temp1,state=0,number=temp2,ISBN=isbn)
         a.save()
     return render(request,"purchase.html",ctx)

 #退货
def cancel(request):
     global UserType,UserID
     if UserType!='manager'and UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
     ctx={}
     ctx['UserType']=UserType
     ctx['UserID']=UserID 
     if request.GET:
         PurchaseList.objects.filter(id=request.GET["id"]).update(state=2)
         p=PurchaseList.objects.filter(id=request.GET["id"]).values("Book_ID")
         for pp in p:
            temp=PurchaseList.objects.filter(Book_ID=pp["Book_ID"]).filter(~Q(state=2)).values("Book_ID")
            if len(temp)==0:
                tempbook.objects.filter(Book_ID=pp["Book_ID"]).delete() #只有当purchaselist中每一条记录都不需要该信息时，才能删除
         list=PurchaseList.objects.values("id","purchase","number","state","Book_ID")
         for l in list:
             l["total"]=l["number"]*l["purchase"]
         ctx["list"]=list
     return render(request,"purchase.html",ctx)

 #入库
def load(request):
    global UserType,UserID,bookid,pur,n,isbn,tit
    if UserType!='manager'and UserType!='supermanager':
        return HttpResponse("<p>您无权访问此网页</p>")
    ctx={}
    ctx['UserType']=UserType
    ctx['UserID']=UserID
    if request.GET:
        i=request.GET["id"]
        pinfo=PurchaseList.objects.filter(id=i).values("Book_ID")
        for p in pinfo:
            bookid=p["Book_ID"]
        bookinfo=Book.objects.values("Book_ID")
        flag=0
        for boo in bookinfo:
            if boo["Book_ID"]==bookid:
                flag=1
        if flag==1:#旧书
            PurchaseList.objects.filter(Book_ID=bookid).update(state=3)
            purinfo= PurchaseList.objects.filter(Book_ID=bookid).values("purchase","number")
            for p in purinfo:
                pur=p["purchase"]
                n=p["number"]
            bookinfo=Book.objects.filter(Book_ID=bookid).values("num")
            for boo in bookinfo:
                x=boo["num"]
            Book.objects.filter(Book_ID=bookid).update(num=x+n)
            ctx["success"]=1
        return render(request,"insure.html",ctx)
    if request.POST:
        discoun=request.POST["discount"]
        pric=request.POST["price"]
        PurchaseList.objects.filter(Book_ID=bookid).update(state=3)
        purinfo= PurchaseList.objects.filter(Book_ID=bookid).values("purchase","number")
        for p in purinfo:
            pur=p["purchase"]
            n=p["number"]
        tempinfo=tempbook.objects.filter(Book_ID=bookid).values("ISBN","title","writer","press")
        for t in tempinfo:
                isbn=t["ISBN"]
                tit=t["title"]
                w=t["writer"]
                pr=t["press"]
        b=Book(ISBN=isbn,Book_ID=bookid,title=tit,writer=w,press=pr,price=pric,num=n,discount=discoun,image=request.POST["image"])
        b.save()
        temp=PurchaseList.objects.filter(Book_ID=bookid).filter(~Q(state=2)).filter(~Q(state=3)).values("Book_ID")
        if len(temp)==0:
            tempbook.objects.filter(Book_ID=bookid).delete()
        ctx["success"]=1
        return render(request,"insure.html",ctx)









        
