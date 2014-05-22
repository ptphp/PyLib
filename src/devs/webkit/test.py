import urllib2, urllib
import simplejson as json
import uuid
id = str(uuid.uuid1())
#{"jsonrpc": "1.0", "params": [{"clientid": 2}], "method": "check_valid", "id": "9a198780-6e57-11e1-8a1f-005056c00008"}
data = {}
params = []
param = {}
param['clientid'] = 1004
params.append(param)
data['jsonrpc'] = 1.0
data['method'] = "check_valid"
data['id'] = id
data['params'] = params

query = json.dumps(data)
print query
req = urllib2.urlopen("http://180.168.71.206:90/showcasecloud/index.php?r=site/test", query)
#req = urllib2.urlopen("http://127.0.0.1/showcasecloud/index.php?r=site/test", query)
print req.read()
