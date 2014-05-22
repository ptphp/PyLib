#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
from PyQt4.QtGui      import *
from PyQt4.QtCore     import *
from PyQt4.QtNetwork  import *


class SslClient(QObject):
    """ This is used to connect to server"""
    def __init__(self, parent=None):
        super(QObject, self).__init__(parent)
        self.m_sslSocket = None

    def connectToHostEncrypted(self, addr, port=443):
        self.m_sslSocket = QSslSocket(self)
        ##self.m_sslSocket.setSocketOption(QAbstractSocket.KeepAliveOption)
        ##sslConfig = QSslConfiguration()
        ##sslConfig.setPeerVerifyMode(QSslSocket.VerifyPeer)
        
        ##此处nginx.crt是服务器的证书�?—即Bob的证书CAb.
        bl = self.m_sslSocket.addCaCertificates('ca.crt')
        if(bl):
            qDebug('server.crt loaded!')
        else:
            qDebug('Can not add the CA ca.crt')
            QApplication.exit()

        self.connect(self.m_sslSocket,
                     SIGNAL("stateChanged(QAbstractSocket::SocketState)"),
                     self.stateChanged)

        self.connect(self.m_sslSocket, SIGNAL("sslErrors(QList<QSslError>)"),
                     self.sslErrors)

        self.connect(self.m_sslSocket, SIGNAL("encrypted()"),
                     self.socketEncrypted)

        self.connect(self.m_sslSocket, SIGNAL("readyRead()"),
                     self.socketReadyRead)

        self.m_sslSocket.connectToHostEncrypted(addr, port)
        qDebug("Connectting ...")
        

    def sslErrors(self, errorList):
        for error in errorList:
            qDebug(str(int(error.SslError())) + ": " + error.errorString())
        #显示完错误就�?��，避免继续在exec_()循环中运�?
        QApplication.exit()

    def stateChanged(self, state):
        if state == 0:
            qDebug(" @@@ " + "The socket is not connected.")
        elif state == 1:
            qDebug(" @@@ " + "The socket is performing a host name lookup.")
        elif state == 2:
            qDebug(" @@@ " + "The socket has started establishing a connection.")
        elif state == 3:
            qDebug(" @@@ " + "A connection is established.")
        elif state == 4:
            qDebug(" @@@ " + "The socket is bound to an address and port(servers).")
        elif state == 5:
            qDebug(" @@@ " + "For internal use only.")
        elif state == 6:
            qDebug(" @@@ " + "The socket is about to close (data may still be waiting to be written).")
        else:
            qDebug(" @@@ " + "UNKNOW CASE")
        
    def socketReadyRead(self):
        qDebug("socketReadyRead(self):")

    def socketEncrypted(self):
        qDebug("socketEncrypted(self)")


def main():
    app = QApplication(sys.argv)
    sslClient = SslClient()
    sslClient.connectToHostEncrypted('192.168.1.109', 443)

    return app.exec_()

if __name__ == '__main__':
    main()



###程序的执行结果为�?
# /etc/ssl/nginx/nginx.crt loaded!
# @@@ The socket is performing a host name lookup.
# @@@ The socket has started establishing a connection.
# Connectting ...
#  @@@ A connection is established.
# 0: The host name did not match any of the valid hosts for this certificate
# 0: The issuer certificate of a locally looked up certificate could not be foun# d
# 0: The root CA certificate is not trusted for this purpose
# 0: No certificates could be verified
#  @@@ The socket is about to close (data may still be waiting to be written).
#  @@@ The socket is not connected.
