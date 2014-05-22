#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import MySQLdb #@UnresolvedImport

class MySQL(object):
    conn = ''
    cursor = ''
    def __init__(self, host='127.0.0.1', user='root', passwd='pb200898', db='jjr360'):
       
        """MySQL Database initialization """
        try:
            self.conn = MySQLdb.connect(host, user, passwd, db, charset='utf8')
        except MySQLdb.Error, e:
            errormsg = 'Cannot connect to server\nERROR (%s): %s' % (e.args[0], e.args[1])
            print errormsg
            sys.exit()           
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    def escape(self, str):
        return MySQLdb.escape_string(str)
    def query(self, sql):
        """  Execute SQL statement """
        try:
            self.cursor.execute(sql)
        except MySQLdb.Error, e:
            errormsg = 'Cannot connect to server\nERROR (%s): %s' % (e.args[0], e.args[1])
            print errormsg

   
    def show(self):
        """ Return the results after executing SQL statement """
        return self.cursor.fetchall()
    def close(self):
        """ Terminate the connection """
        self.conn.close()
    
    def __del__(self):
        """ Terminate the connection """
        self.conn.close()
        self.cursor.close()
        
