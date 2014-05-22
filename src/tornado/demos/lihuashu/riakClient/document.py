#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-20
'''
import urllib2
import urllib
from hashlib import md5
import cookielib
from config.settings import globalSetting
import simplejson as json

class Document():    
    bucket_name = None
       
    obj         = None
    bucket      = None
    key         = None
    query       = None
    data        = {}
    
    port=globalSetting['riakPort']
    host=globalSetting['riakHost']
    url = None
        
    def __init__(self):
        #self.bucket = self.bucket(self.bucket_name)
        self.url = "http://%s:%s" % (self.host,self.port)
        httpHandler = urllib2.HTTPHandler(debuglevel = 0)
        opener = urllib2.build_opener(httpHandler)
        
        urllib2.install_opener(opener)
        
        
    def get(self,key):
        url = "%s/riak/%s/%s" % (self.url,self.bucket_name,key)    
        #print url
        try:    
            res = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            #print e.code
            return None
        else:
            #data = json.loads(res)
            return  json.loads(res.read())

        
    def post(self):        
        url = "%s/riak/%s/%s" % (self.url,self.bucket_name,self.key)    
        self.data['key'] = self.key
        data = json.dumps(self.data)
        #print data
        
        req = urllib2.Request(url,data.encode("utf-8"))
        req.add_header("Accept", "application/json")
        req.add_header("content-type", "application/json;charset=utf-8")        
        req.add_header("X-Riak-Vclock", "a85hYGBgzGDKBVIszMk55zKYEhnzWBlKIniO8mUBAA==")
        
        req.get_method = lambda:"POST"                
        try:            
            res = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            return e.code
        else:                          
            return res.code
        
    def put(self):
        url = "%s/riak/%s/%s" % (self.url,self.bucket_name,self.key)    
        self.data['key'] = self.key
        req = urllib2.Request(url,json.dumps(self.data))
        
        req.add_header("Content-Type", "application/json")        
        req.add_header("X-Riak-Vclock", "a85hYGBgzGDKBVIszMk55zKYEhnzWBlKIniO8mUBAA==")      
          
        req.get_method = lambda:"PUT"        
        
        try:            
            res = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            return e.code
        else:                          
            return res.code
    
    def delete(self,key):        
        url = "%s/riak/%s/%s" % (self.url,self.bucket_name,key)    
        #print url
        req = urllib2.Request(url)
        req.get_method = lambda:"DELETE"
        
        #204 No Content and 404 Not Found        
        try:            
            res = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            return e.code
        else:                          
            return res.code
    
    def all(self,keys):        
        data = []
        for key in keys:
            data.append(self.get(key))
        return data
    
    def solr(self,query):
        query['wt'] = "json"
        querystr = urllib.urlencode(query)
        url = "%s/solr/%s/select?%s" % (self.url,self.bucket_name,querystr)
        #print url
        req = urllib2.Request(url)
        #req.add_header("Content-Type", "application/json")
           
        try:            
            res = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            #print e.code
            return []
        else:                          
            #print res.code
            response = json.loads(res.read())
            docs = response['response']['docs']
            if docs:
                result = []
                for doc in docs:                
                    result.append(doc['fields'])
                return  result
            else:
                return []
    
    def allKey(self):
        url = "%s/buckets/%s/keys?keys=true" % (self.url,self.bucket_name)
        #print url
        req = urllib2.Request(url)
        req.add_header("Content-Type", "application/json")
           
        try:            
            res = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            #print e.code
            return []
        else:                          
            #print res.code
            return  json.loads(res.read())['keys']
    def getByKeyValues(self,key,value):
        #print key,value
        source = """        
        function(v) { 
                var data = JSON.parse(v.values[0].data); 
                if(data.%s == '%s') 
                { 
                    return [v.key]; 
                } 
                return []; 
            }
        """ % (key,value)
        query ={
                "inputs":self.bucket_name,
                "query":[
                         {"map":{
                                 "language":"javascript",
                                 "source":source,
                                 "keep":True
                                 }
                          }
                         ]}
        
        
        url = "%s/mapred " % self.url
               
        data = json.dumps(query)
        #print data
        req = urllib2.Request(url,data)
        req.add_header("Accept", "application/json")
        req.add_header("content-type", "application/json;charset=utf-8")      
        
        req.get_method = lambda:"POST"        
        
        try:            
            res = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            #print "e.code"
            #print e.code
            return []
        else:   
            #print res.code
            return json.loads(res.read())
        
    def allData(self):
        source1 = """        
        "function(value) {    
            var data = Riak.mapValuesJson(value)[0];
            return [value]; 
        }"
        """
        source = """        
        function(riakObject) {   
                            return  [riakObject.values[0].data];     
                            }
        """
       # source = "function(v) {return [[v.key, data]]; }"

        query ={
                "inputs":self.bucket_name,
                "query":[
                         {"map":{
                                 "language":"javascript",
                                 "source":source,
                                 "keep":True
                                 }
                          }
                         ]}
        
        
        url = "%s/mapred " % self.url
               
        data = json.dumps(query)
        
        req = urllib2.Request(url,data)
        req.add_header("Accept", "application/json")
        req.add_header("content-type", "application/json;charset=utf-8")      
        
        req.get_method = lambda:"POST"        
        
        try:            
            res = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            pass
            #print e.code
        else:                          
            #print res.code
            return res.read()
    def genKey(self,str):
        return md5(str.encode('utf-8')).hexdigest()
    def __str__(self):
        return self.data
    
class Test(Document):
    bucket_name = "test"
    
    data = {
             'name':None,
             'sex':None,
             }
    
    def __init__(self):
        Document.__init__(self)        
    
def runme():
    #client = RiakClient(port=globalSetting['riakPort'],host=globalSetting['riakHost'])
    #client = RiakClient(port=8091,host="127.0.0.1")    
    client = ""
    d = Test(client)
    d.key = "joseph"
    d.data['name'] = "ww"
    d.data['sex'] = "male"
    d.post()
    
    putData = d.get(d.key)
    #d.delete()
    putData['name'] = "john2"
    d.put(putData)
    
    print d.all()
    print d.allKey()
    print d.allData()
    
def gorunme():    
    t = Test()
    t.key = "fangtee"
    
    t.data['name'] = "fangtee"
    t.data['sex'] = "中"
    
    t.post()
    
    print t.get("fangtee")['sex']
    #print t.all()
    allData = t.allData()
    print json.loads(allData)
    #print t.allKey()
    #t.delete("testqq")
    #d.all("testqq")
    #d.put("testqq")
  
if __name__ == '__main__':
    gorunme()
    
    