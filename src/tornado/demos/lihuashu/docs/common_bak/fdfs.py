#coding:utf8
# Python bind  fastDFS/fastDHT by Insion
# Email:insion@garning.com
import os
import subprocess
#import hashlib
#from kyototycoon import KyotoTycoon


class Fdfs:
	def open(self,client_conf = "/etc/fdfs/client.conf",fdfs_path="/usr/local/bin",tracker_host = "192.168.106.78", tracker_http_port ="8080"):
		#self.kt = KyotoTycoon()
		#self.kt.open("localhost", 1978)
		self.tracker_url='http://'+tracker_host+':'+tracker_http_port+'/'
		self.fdfs_path=fdfs_path
		self.client_conf=client_conf

	def upload(self,upload_file =None):
		if os.path.isfile(self.client_conf):
			if os.path.isfile(upload_file):
				try:
					#from function import GetFileCRC32
					#icrc32=GetFileCRC32(upload_file)
					'''
					if not self.kt.get("file;"+str(icrc32)):
					    fdfs_bin=os.path.join(self.fdfs_path,'fdfs_upload_file')
					    s=subprocess.Popen([fdfs_bin,self.client_conf,upload_file], stdout=subprocess.PIPE)
		    
					    self.kt.set("file;"+str(icrc32),s.stdout.read())
					    return self.tracker_url+str(s.stdout.read())
					else:
					    return self.tracker_url+self.kt.get_str("file;"+str(icrc32))
					'''
					fdfs_bin=os.path.join(self.fdfs_path,'fdfs_upload_file')
					s=subprocess.Popen([fdfs_bin,self.client_conf,upload_file], stdout=subprocess.PIPE)
					sr=s.stdout.read()
					import re
					p = re.compile(r".*/.*/.*/.*/.*_.*")
					m=p.match(str(sr,'utf8'))
					if m:
						#return self.tracker_url+str(sr)
						return str(sr,'utf8')
					else:
						return False
					
				except:
					return False


			else:
				print('Please set the upload file path!')
				return False
		else:
			print('Please set the FDFS client configuration file:/etc/client.conf!')
			return False

	#fdfs_delete_file /etc/fdfs/client.conf groupserver1/M00/00/00/wKhqTk_DNfOKkA66AARGyzjIiao904.jpg
	def delete(self,delete_file =None):
		if os.path.isfile(self.client_conf):
			try:
				#fdfs_file_info /etc/fdfs/client.conf groupserver1/M00/00/00/wKhqTk_DNfOKkA66AARGyzjIiao904.jpg
				'''
				fdfs_bin_info=os.path.join(self.fdfs_path,'fdfs_file_info')
				s_info=subprocess.Popen([fdfs_bin_info,self.client_conf,delete_file], stdout=subprocess.PIPE)
				import re
				p = re.compile(r"\(([^\)]+)\)")
				icrc32=p.search(str(s_info.stdout.read())).group(1)
				'''
				fdfs_bin=os.path.join(self.fdfs_path,'fdfs_delete_file')
				s = subprocess.Popen([fdfs_bin,self.client_conf,delete_file], stdout=subprocess.PIPE)

				#self.kt.remove("file;"+icrc32)
				return True

			except:
				pass

		else:
			print('Please set the FDFS client configuration file:/etc/client.conf!')



'''
from fdfs import Fdfs
fs=Fdfs()
fs.open()

k=fs.upload("/home/insion/Pictures/m.jpg")
print(k)
fs.delete("groupserver1/M00/00/00/wKhqTk_EsI7bH178AAX1V26GPDY840.jpg")
'''