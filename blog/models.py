from django.db import models

# Create your models here.
#!/usr/bin/python
#coding:utf-8
 
from django.db import models
 
class Blog(models.Model):
    
    def __unicode__(self):
        return self.title
