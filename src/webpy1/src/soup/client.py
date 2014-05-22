'''
Created on 2011-7-26

@author: dholer
'''
from suds.client import Client
hello_client = Client('http://localhost:7789/?wsdl')
result = hello_client.service.say_hello("Dave", 5)
print result