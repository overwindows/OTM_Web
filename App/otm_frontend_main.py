#coding:utf-8

import os
import web
import model
import time
import datetime
import json
import sign
import urllib
import memcache

from webchat import *
from index import *
from sites import *
from menus import *
from member import *
from qulification import *
from bill import *
from login import *
from orders import *
from receipt import *
from register import *
from reset import *
from defray import *
from webchatpay import *
from delivery import *
from sign import Sign
from pay import *
from orderinfo import *
from orderfail import *
from cancelorder import *
from logout import *
from terms import *

'''
from succeed import *
from paylunch import *
from sms import *
from register import *
'''

from env import render

class MemCacheStore(web.session.Store):
    mc = None
    def __init__(self):
        self.mc = memcache.Client(['127.0.0.1:37194'], debug=0)
    def __contains__(self, key):
        return self.mc.get(key) != None
    def __getitem__(self, key):
        return self.mc.get(key)
    def __setitem__(self, key, value):
        self.mc.set(key, value, time = web.config.session_parameters["timeout"])
    def __delitem__(self, key):
        self.mc.delete(key)
    def cleanup(self, timeout):
        pass # Not needed as we assigned the timeout to memcache

urls = (
        '/favicon.ico','icon',
        '/', 'index',
        '/index', 'index ',
        '/sites', 'sites',
        '/menus', 'menus',
        '/defray', 'defray',
        '/member', 'member',
        '/qulification', 'qulification',
        '/bill', 'bill',
        '/login', 'login',
        '/orders', 'orders',
        '/receipt', 'receipt',
        '/register', 'register',
        '/reset', 'reset',
        '/webchatpay', 'webchatpay',
        '/member', 'member',
        '/delivery','delivery',
        '/orderfail', 'orderfail',
        '/orderinfo', 'orderinfo',
        '/cancelorder', 'cancelorder',
        '/logout', 'logout',
        '/terms', 'terms',
	'''
        '/carte_detail', 'carte_detail',
        '/carte_succeed', 'carte_succeed',
        '/order_cancel', 'order_cancel',
        '/order_over', 'order_over',
        '/order_index', 'order_index',
        '/order_list', 'order_list',
        '/success', 'success',
        '/carte_pay', 'carte_pay',
        '/sms_valid', 'sms_valid',
	'''
        )

app = web.application(urls, globals())
#sessions_store = web.session.DBStore(model.db, 'sessions')
sessions_store = MemCacheStore() 
#session = web.session.Session(app,sessions_store)
session = web.session.Session(app,sessions_store)

# http://webpy.org/cookbook/sessions_with_subapp
def session_hook():
    web.ctx.session = session
    web.template.Template.globals['session'] = session
app.add_processor(web.loadhook(session_hook))

class icon:
    def GET(self): 
        raise web.seeother("/static/images/favicon.ico")

#已完成订单
class order_over:
    def GET(self):
        #username = session.username
        userid = session.userid 
        #userid = web.cookies().get('uid')
        #print userid
        msgs = []
        msgs_it = model.ongoing_orders_cnt(userid)
        msgs = list(msgs_it)
        orders_1 = model.get_orders(int(userid),1)
        return render.order_over(userid,orders_1, session.headimgurl, session.nickname, msgs)
    
class order_cancel:
    def GET(self):
        #username = session.username
        userid = session.userid 
        #userid = web.cookies().get('uid')
        #print userid
        msgs = []
        msgs_it = model.ongoing_orders_cnt(userid)
        msgs = list(msgs_it)
        orders_2 = model.get_orders(int(userid),2)
        return render.order_cancel(userid,orders_2, session.headimgurl, session.nickname, msgs)   

if __name__ == '__main__':
    app.run()
