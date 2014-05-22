#!user/bin/env python
# -*- coding: utf8 -*- 
from riakkit import Document,StringProperty #@UnresolvedImport
import riak
some_client = riak.RiakClient(port=8091) #@UndefinedVariable

class User(Document):
    bucket_name = "doctest_users"
    client = some_client
    name = StringProperty(required=True)
    def __str__(self):
        return self.name

user = User(name="joseph")
user.save()
user_query = User.search("name:'joseph'")
print user_query.length()