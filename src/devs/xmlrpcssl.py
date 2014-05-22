import xmlrpclib

class SafeTransportWithCert(xmlrpclib.SafeTransport):
	__cert_file = 'D:\\Dholer\\Data\\sslcert\\server.pem'
	__key_file = 'D:\\Dholer\\Data\\sslcert\\server.pem'

	def make_connection(self, host):
		host_with_cert = (host, {'key_file' : self.__key_file, 'cert_file' : self.__cert_file})

		return xmlrpclib.SafeTransport.make_connection(self, host_with_cert)


transport = SafeTransportWithCert()
server_url = 'https://localhost:8069/xmlrpc/object'
server = xmlrpclib.ServerProxy(server_url, transport=transport)

#print server.execute('test', 1, 'admin', 'res.users', 'search', [])
