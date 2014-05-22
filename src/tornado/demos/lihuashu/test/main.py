#!user/bin/env python
# -*- coding: utf8 -*- 
'''
Created on Jul 11, 2012

@author: joseph
'''
import riak


client = riak.RiakClient(port=8091)

bucket = client.bucket('test')
#p =bucket.new("test",data={
#                        'name':'joseph'
#                        })
#p.store()
p = bucket.get("test")
print p.get_data()