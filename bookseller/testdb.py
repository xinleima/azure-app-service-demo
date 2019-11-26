# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
 
from TestModel.models import Manager
 
# 添加超级管理员
def Insertsuper(request):
    test1 = Manager(Mana_ID='17307130357',username='Oba',password='123456',name='tang',gender='Female',age=20,supera=1)
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")
