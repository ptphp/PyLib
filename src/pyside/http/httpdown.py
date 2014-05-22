#coding:utf-8
'''
Created on Sep 25, 2012

@author: joseph
'''
import sys

import io
import urllib2

from PySide import QtCore, QtGui, QtNetwork
import time

class QDownloadBuffer(QtCore.QBuffer):
    downloadFinished = QtCore.Signal()
    def __init__(self):
        super(QDownloadBuffer, self).__init__()
        self.open(QtCore.QBuffer.ReadWrite)
        self.url = QtCore.QUrl("http://www.google.com.au/images/srpr/logo3w.png")
        self.manager = QtNetwork.QNetworkAccessManager()
        self.request = QtNetwork.QNetworkRequest(self.url)
        self.manager.finished.connect(self.onFinished)

    def startDownload(self):
        print("Starting Download --")
        self.reply = self.manager.get(self.request)

        self.reply.error[QtNetwork.QNetworkReply.NetworkError].connect(self.onError)

    def onFinished(self):
        print("Download Finished -- ")
        print(self.write(self.reply.readAll()))
        self.reply.close()
        self.downloadFinished.emit()

    def onError(self):
        print("oh no there is an error -- ")
        print(self.reply.error())

class ImagePreview(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ImagePreview, self).__init__(parent)
        self.setMinimumSize(50, 50)
        self.text = None
        self.pixmap = None
        self.dl_n = 0


    def paintEvent(self, paintEvent):
        painter = QtGui.QPainter(self)

        if(self.pixmap):
            painter.drawPixmap(0, 0, self.pixmap)

        if(self.text):
            painter.setPen(QtCore.Qt.blue)
            painter.setFont(QtGui.QFont("Arial", 30))
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, self.text)

    def startDownload(self):
        self.setText(str(self.dl_n))
        self.dl_n += 1
        print("Starting Download {0}".format(self.dl_n))

        self.db = QDownloadBuffer()
        self.connect(self.db, QtCore.SIGNAL("downloadFinished()"), self, QtCore.SLOT("ondownloadFinished()"))
        self.db.startDownload()

    def ondownloadFinished(self):
        self.paintImage()
        print("download finished?")
        self.db.close()
        #self.startDownload()
        QtCore.QTimer.singleShot(0, self.startDownload)
        #or
        #QtCore.QMetaObject.invokeMethod(self, 'startDownload',  QtCore.Qt.QueuedConnection)


    def paintImage(self):
        print("Painting")
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self.db.data())
        self.setPixmap(pixmap)

    def setPixmap(self, pixmap):
        self.pixmap = pixmap
        self.setMinimumSize(pixmap.width(), pixmap.height())
        self.update()

    def setText(self, text):
        self.text = text
        self.update()


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.imagepreview = ImagePreview()
        self.button = QtGui.QPushButton("Start")
        self.button.clicked.connect(self.imagepreview.startDownload)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.imagepreview)
        self.setLayout(layout)



if __name__ == "__main__":
    import sys

    try:
        app = QtGui.QApplication(sys.argv)
    except RuntimeError:
        pass

    mainwindow = MainWindow()
    mainwindow.show()

    sys.exit(app.exec_())