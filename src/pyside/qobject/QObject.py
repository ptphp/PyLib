from PySide.QtCore import *
from PySide.QtGui import *
import sys


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    win = QWidget()
    win.setWindowTitle("test")
    print win.acceptDrops()
    win.show()
    sys.exit(app.exec_())
  
