#coding=UTF-8
'''
Created on 2011-7-10

@author: Administrator
'''
import wx
from ui.window import create
class uiApp(wx.App):
    def OnInit(self):
        self.main = create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = uiApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()