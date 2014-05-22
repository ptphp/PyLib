from ptmysql import PtMysql
from ptsqlite import PtSqlite
config = {
          'default':{
                     'type':'mysql',
                     'host':'localhost',
                     'port':3306,
                     'dbname':'game110_dev',
                     'dbuser':'root',
                     'dbpass':'',
                     'charset':'utf8',
                     },
          'sqlite':{
                    'type':'sqlite',                    
                    }
          }
instance = {}
def init(k='default'):
    if config[k]['type'] == 'sqlite':
        db = PtSqlite()
    else:
        print instance
        if k in instance:
            db = instance[k]
        else:            
            db = PtMysql(config[k]['host'], config[k]['dbname'], config[k]['dbuser'], config[k]['dbpass'])
            instance[k] = db        
    return db
    


