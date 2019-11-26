from django.db import models

# Create your models here.

class Manager(models.Model):
    Mana_ID = models.CharField(max_length=15,primary_key=True)
    username=models.CharField(max_length=24)
    password=models.CharField(max_length=60)
    name=models.CharField(max_length=45)
    gender = models.CharField(max_length=10)
    age=models.IntegerField()
    supera=models.IntegerField()
    
#books in stocks   
class Book(models.Model):
    ISBN=models.CharField(max_length=30,primary_key=True)
    Book_ID=models.CharField(max_length=20)
    title=models.CharField(max_length=60)
    writer=models.CharField(max_length=20)
    press=models.CharField(max_length=60)
    price=models.FloatField(max_length=8)
    num=models.IntegerField()
    discount=models.FloatField(max_length=4)
    image=models.CharField(max_length=20)

class Customer(models.Model):
    Cus_ID = models.CharField(max_length=45,primary_key=True)
    password=models.CharField(max_length=60)

class PurchaseList(models.Model):
    Book_ID=models.CharField(max_length=20)
    purchase=models.IntegerField()
    number=models.IntegerField()
    state=models.IntegerField()
#state=0:not paid state=1:have paid state=2:have refunded

class Account(models.Model):
    ISBN=models.CharField(max_length=30)
    price=models.FloatField()
    state=models.IntegerField()
    number=models.IntegerField()
    dt=models.DateTimeField(auto_now=True)
#state=0:payment state=1:proceed

class Comment(models.Model):
    ISBN=models.ForeignKey(Book,on_delete=models.CASCADE,)
    customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE,)
    grade=models.FloatField(max_length=2)
    description=models.CharField(max_length=400)



class tempbook(models.Model):
    ISBN=models.CharField(max_length=30,primary_key=True)
    Book_ID=models.CharField(max_length=20)
    title=models.CharField(max_length=60)
    writer=models.CharField(max_length=20)
    press=models.CharField(max_length=60)
   


