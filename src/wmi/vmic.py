'''
Created on Jan 24, 2013

@author: joseph
'''
import os
def getOsEnvVar(name):  
    cmd ='wmic ENVIRONMENT where "name=\'%s\' and username=\'<system>\'" get VariableValue /value' % name
    path = os.popen(cmd)
    res =  path.read().strip().replace("VariableValue=","")
    if res == '':
        print "this is no {%s} for name var " % name
        return None
    return res

print getOsEnvVar("PATH") 
path = os.popen("wmic")
print path.read()