#coding=UTF-8
from suds.client import Client
hello_client = Client('http://localhost:8888/hello.wsdl')
result = hello_client.service.hello("Dave")
print result