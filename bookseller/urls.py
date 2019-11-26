"""bookseller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import *
from . import testdb
from . import view1
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


def prod_static_url():
    '''
    prod 模式下的 url 适配
    '''
    from django.views import static
    urlpattern = url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static')
    return urlpattern


urlpatterns = [
    url(r'^testdb$', testdb.Insertsuper),
    url(r'^sign_up', view1.sign_up),
    url(r'^log_in', view1.log_in),
    url(r'^showall', view1.showall, name='showall'),
    url(r'^search', view1.search),
    url(r'^comment', view1.comment),
    url(r'^manager_register', view1.manager_register),
    url(r'^entermanager', view1.entermanager, name='entermanager'),
    url(r'^commonchange_info', view1.commonchange_info, name='commonchange_info'),
    url(r'^superview_info', view1.superview_info, name='superview_info'),
    url(r'^superchange_info', view1.superchange_info, name='superchange_info'),
    url(r'^change_info', view1.change_info, name='change_info'),
    url(r'^manager_delete', view1.manager_delete, name='manager_delete'),
    url(r'^changebook_info', view1.changebook_info, name='changebook_info'),
    url(r'^bookchange_info', view1.bookchange_info, name='bookchange_info'),
    url(r'^book_delete', view1.book_delete, name='book_delete'),
    url(r'^buy', view1.buy, name='buy'),
    url(r'^payment', view1.payment, name='payment'),
    url(r'^viewaccount3', view1.viewaccount3, name='viewaccount3'),
    url(r'^viewaccount2', view1.viewaccount2, name='viewaccount2'),
    url(r'^viewaccount1', view1.viewaccount1, name='viewaccount1'),
    url(r'^purchase', view1.purchase, name='purchase'),
    url(r'^pur_pay', view1.pur_pay, name='pur_pay'),
    url(r'^cancel', view1.cancel, name='cancel'),
    url(r'^load', view1.load, name='load'),
    prod_static_url()

]
urlpatterns += staticfiles_urlpatterns()
