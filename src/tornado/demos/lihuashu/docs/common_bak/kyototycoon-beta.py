import time,urllib

#python-requests.org
import requests

class KyotoTycoon:
    # connect to the server
    def open(self, host = "127.0.0.1", port = 1978, timeout = 30):
        #self.ua = http.client.HTTPConnection(host, port, False, timeout)
        self.host=host
        self.port=str(port)
        self.timeout=timeout

    # store a record
    def set(self, key, value, xt = None):
        #requests.put("http://httpbin.org/put")
        if isinstance(key, str): key = key.encode("UTF-8")
        if isinstance(value, str): value = value.encode("UTF-8")
        #urllib.quote("http://neeao.com/index.php?id=1",":?=/") 
        key = "/" + urllib.quote(key,safe=':;')
        '''
        v={}
        if xt != None:
            try:
                xt=str(int(xt))
                v= {'key':key,'value':value,'xt':xt}
            except:
                xt=None
                v= {'key':key,'value':value}
        else:
            xt=None
            v= {'key':key,'value':value}
                
        print(v)
        '''
        v= {'key':key,'value':value}
        headers = {}
        if xt != None:
            xt = int(time.time()) + xt
            headers["X-Kt-Xt"] = str(xt)
        r=requests.put('http://'+self.host+':'+self.port+"/", params=v,headers=headers)
        #r = requests.get('http://'+self.host+':'+self.port+"/rpc/set", params=v)
        return r.status_code == requests.codes.ok
    
    def set_int(self, key, value, xt = None):
        self.set(key,str(value), xt)
        
    # remove a record
    def remove(self, key):
        if isinstance(key, str): key = key.encode("UTF-8")
        key = "/" + urllib.quote(key)
        v= {'key':key}
        r = requests.get('http://'+self.host+':'+self.port+"/rpc/remove", params=v)
        return r.status_code == requests.codes.ok
    
    # retrieve the value of a record
    def get(self, key):
        if isinstance(key, str): key = key.encode("UTF-8")
        key = "/" + urllib.quote(key,safe=':;')
        v= {'key':key}
        r = requests.get('http://'+self.host+':'+self.port+"/rpc/get", params=v)
        if r.status_code == 200:
            return r.text
        elif r.status_code == 450:
            return None
        else:
            return False
    
    def get_int(self, key):
        if self.get(key) ==None:
            return None
        else:
            return int(str(self.get(key),'UTF-8'))

    def get_str(self, key):
        if self.get(key) ==None:
            return None
        else:
            return str(self.get(key),'UTF-8')
        
    def match_prefix(self,prefix):
        if isinstance(prefix, str): prefix =prefix.encode("UTF-8")
        prefix = "/" + urllib.quote(prefix)
        v= {'prefix':prefix}
        r = requests.get('http://'+self.host+':'+self.port+"/rpc/match_prefix", params=v)
        return r.text
    
    def match_regex(self,regex):
        if isinstance(regex, str):regex =regex.encode("UTF-8")
        prefix = "/" + urllib.quote(regex)
        v= {'regex':regex}
        r = requests.get('http://'+self.host+':'+self.port+"/rpc/match_regex", params=v)
        return r.text
    
'''
# sample usage
kt = KyotoTycoon()
kt.open("localhost", 1978)
kt.set("japan", "tokyo", 60)
print(kt.get("japan"))
kt.remove("japan")
kt.close()
'''