# -*- coding: utf-8 -*-
from sqlModel import *

sqlObj = Db("fangtee.db")
sqlObj.query("select * from house limit 1")
r = sqlObj.showOne()
print r