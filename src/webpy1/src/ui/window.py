#coding=UTF-8
'''
Created on 2011-7-10

@author: Administrator
'''
import wx
from core import tongcheng58, ganji, soufang
from fetch.fetch_links_ctrl import gogogo
gsites={
        u"58同城":{tongcheng58:["su","gz","bj","ks",]},
        u"赶集":{ganji:["su","gz","bj","ks",]},
        u"搜房":{soufang:["su","gz","bj","ks",]},
        }
def create(parent):
    return mainFrame(parent)
class mainFrame(wx.Frame):
    def __init__(self, parent):
        self.__init_ctrls(parent)
    def __init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=-1, name='mainFrame',
              parent=prnt, pos=wx.Point(372, 72), size=wx.Size(500, 500),
              style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX),
              title=u'采集助手')
        self.allParams=[]
        
        
        
        self.myMenuBar = wx.MenuBar()
        self.myMenuBar.SetWindowStyleFlag(1)
        self.SetMenuBar(self.myMenuBar)
        self.SetThemeEnabled(True)
        self.File = wx.Menu(title=u'')
        self.File.SetEvtHandlerEnabled(True)
        self.Help = wx.Menu(title=u'')
        self.myMenuBar.Append(menu=self.File, title=u'文件')
        self.myMenuBar.Append(menu=self.Help, title=u'帮助')
        exit=self.File.Append(help=u'退出程序', id=-1,
              kind=wx.ITEM_NORMAL, text=u'退出')
        self.Bind(wx.EVT_MENU, self.OnSelectExitMenu,exit)
        
        
        self.panel = wx.Panel(id=-1, name='panel',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(531, 571),
              style=wx.MAXIMIZE_BOX | wx.TAB_TRAVERSAL)
        wx.StaticText(parent=self.panel, id=-1,pos=wx.Point(8,11),label=u'网站:')
        sites = self.getCategory()
        self.site=wx.ComboBox(self.panel, -1, pos=(50, 8), size=(80, -1), choices=sites, style=wx.CB_READONLY)
        self.site.SetToolTip(wx.ToolTip(u"选择网站"))
        self.site.Bind(wx.EVT_COMBOBOX, self.changeSite)
        
        wx.StaticText(parent=self.panel, id=-1,pos=wx.Point(135,11),label=u'城市:')
        self.city=wx.ComboBox(self.panel, -1, pos=(165, 8), size=(80, -1), choices=[], style=wx.CB_READONLY)
        self.city.SetToolTip(wx.ToolTip(u"选择城市"))
        
        wx.StaticText(parent=self.panel, id=-1,pos=wx.Point(250,11),label=u'操作:')
        self.opt=wx.ComboBox(self.panel, -1, pos=(280, 8), size=(53, -1), choices=[u"出售",u"出租",u"求购",u"求租"], style=wx.CB_READONLY)
        self.opt.SetToolTip(wx.ToolTip(u"选择操作"))
        
        self.delitems=wx.Button(self.panel, id=-1,pos=wx.Point(420,8),size=wx.Size(60, -1),label=u'删除')
        self.delitems.Bind(wx.EVT_BUTTON, self.delgriditems)
        
        wx.StaticText(parent=self.panel, id=-1,pos=wx.Point(8,45),label=u'线程数:')
        self.tn=wx.SpinCtrl(parent=self.panel,id= -1, pos=wx.Point(50, 40), initial=20,size=wx.Size(50, -1), min=1, max=999)
        
        wx.StaticText(parent=self.panel, id=-1,pos=wx.Point(110,45),label=u'时间 1:')
        self.tst=wx.SpinCtrl(parent=self.panel,id= -1, pos=wx.Point(150, 40), initial=3000,size=wx.Size(60, -1), min=1, max=86400)
        self.tst.SetToolTip(wx.ToolTip(u"整体循环休眠时间"))
        
        wx.StaticText(parent=self.panel, id=-1,pos=wx.Point(215,45),label=u'时间 2:')
        self.lst=wx.SpinCtrl(parent=self.panel,id= -1, pos=wx.Point(260, 40), initial=3,size=wx.Size(50, -1), min=1, max=999)
        self.lst.SetToolTip(wx.ToolTip(u"链接抓取间隔时间"))
        
        
        self.addThreadSet=wx.Button(self.panel, id=-1,pos=wx.Point(345,8),size=wx.Size(60, -1),label=u'添加')
        self.addThreadSet.Bind(wx.EVT_BUTTON, self.addThreadOption)
        
        self.goImport=wx.Button(self.panel, id=-1,pos=wx.Point(345,40),size=wx.Size(60, -1),label=u'导入')
        self.goImport.Bind(wx.EVT_BUTTON, self.addThreadOption)
    
        self.goRun=wx.Button(self.panel, id=-1,pos=wx.Point(420,40),size=wx.Size(60, -1),label=u'运行')
        self.goRun.Bind(wx.EVT_BUTTON, self.startFetch)
    
    
    
#        self.lc =CheckList(self, columns=[
#                (u'网站', 150, 'left'),
#                (u'城市', 150, 'left'),
#                (u'操作', 174, 'left'),
#            ])
#        self.lc.load(self.getdata)    
        self.lc = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT,pos=wx.Point(8,80),size=(478, 350))
        self.lc.InsertColumn(0, u'网站')
        self.lc.InsertColumn(1, u'城市')
        self.lc.InsertColumn(2, u'操作')
        self.lc.SetColumnWidth(0, 150)
        self.lc.SetColumnWidth(1, 150)
        self.lc.SetColumnWidth(2, 174)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def delgriditems(self,evt):
        site= self.site.GetStringSelection()
        city=self.city.GetStringSelection()
        opt=self.opt.GetSelection()
        data=[gsites.get(site).keys()[0],city,str(opt+1)]
        self.allParams.remove(data)
        index = self.lc.GetFocusedItem()
        self.lc.DeleteItem(index)
    def startFetch(self,evt):
        print self.tn.GetValue()
        print self.tst.GetValue()
        print self.lst.GetValue()
#        data=[
#              [tongcheng58,"su","1","3"]
#              ]
        if self.allParams==[]:
            self.ShowMessage(u"请输入数据")
            return
        data=[]
        for p in self.allParams:
            data.append([p[0],p[1],p[2],self.lst.GetValue()])
        tnum=self.tn.GetValue()
        if tnum>len(data):
            tnum=len(data)
        go=gogogo(data,self.tst.GetValue(),tnum)
        go.start()
        
        
    
    def ShowMessage(self,msg):
        wx.MessageBox(msg, 'Error')
        return
    def addThreadOption(self,evt):
        site= self.site.GetStringSelection()
        city=self.city.GetStringSelection()
        opt=self.opt.GetSelection()
        if site=="" or city =="" or opt==-1:
            self.ShowMessage(u"请输入完整")
            return
        
        param=[gsites.get(site).keys()[0],city,str(opt+1)]
        if param not in self.allParams: 
            self.allParams.append(param)
            num_items = self.lc.GetItemCount()
            self.lc.InsertStringItem(num_items, site)
            self.lc.SetStringItem(num_items, 1, city)
            self.lc.SetStringItem(num_items, 2, str(opt+1))
#        print site,city,opt
    def changeSite(self,evt):
        site= self.site.GetStringSelection()
        self.city.Clear()
        self.city.AppendItems(gsites.get(site).values()[0])
    def OnSelectExitMenu(self, event):
        self.Close(True)
    def getCategory(self):
        return [u"58同城",u"赶集",u"搜房"]