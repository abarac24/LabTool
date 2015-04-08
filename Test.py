

# http://groups.google.com/group/wxpython-users/browse_thread/thread/f36a4527bee4a82?hl=en

import wx

def InitOnPanelTest( controller, enable, disable):
    # allows for some decoupling
    # if toggle state is all you want
    # but stores another "reference" to object thus harder to Destroy()
    OnPanelTest.chboxController = controller
    OnPanelTest.toggleWithItems = enable
    OnPanelTest.toggleNotWithItems = disable

def OnPanelTest(evt):
    print evt.GetEventObject().GetLabel(),
    print 'EVT_CHECBOX is bound to a Panel object'

    if hasattr(OnPanelTest,"chboxController"):
        on = OnPanelTest.chboxController.IsChecked()
        for item in OnPanelTest.toggleWithItems:
            item.Enable(on)
        for item in OnPanelTest.toggleNotWithItems:
            item.Enable(not on)

    # --------
    evt.Skip()

def OnTextCtrlTest(evt):
    print evt.GetEventObject().GetLabel(),
    print 'EVT_CHECBOX is bound to a TextCtrl object'
    evt.Skip()

app = wx.PySimpleApp()
frm = wx.Frame(None,-1,"Test")
panel = wx.Panel(frm)
panelsizer = wx.BoxSizer(wx.HORIZONTAL)

chbox = wx.CheckBox(panel, -1, 'CheckBox')
panelsizer.Add(chbox, 0, wx.ALL, 10)

tcsizer = wx.BoxSizer(wx.VERTICAL)


ctrl1 = wx.TextCtrl(panel, -1, 'TextCtrl')
tcsizer.Add(ctrl1, 0, wx.ALL, 10)
ctrl2 = wx.TextCtrl(panel, -1, 'TextCtrl')
tcsizer.Add(ctrl2, 0, wx.ALL, 10)
ctrl3 = wx.TextCtrl(panel, -1, 'TextCtrl')
tcsizer.Add(ctrl3, 0, wx.ALL, 10)
ctrl4 = wx.TextCtrl(panel, -1, 'TextCtrl')
tcsizer.Add(ctrl4, 0, wx.ALL, 10)

panelsizer.Add(tcsizer, 0, wx.ALL, 10)

panel.Bind(wx.EVT_CHECKBOX, OnPanelTest, chbox) # working
ctrl1.Bind(wx.EVT_CHECKBOX, OnTextCtrlTest, chbox) # not working

InitOnPanelTest( chbox, [ctrl1,ctrl2], [ctrl3, ctrl4])

panel.SetAutoLayout(True)
panel.SetSizer(panelsizer)
panelsizer.Fit(panel)
panelsizer.SetSizeHints(panel)
panel.Layout()
app.SetTopWindow(frm)
frm.Show()
app.MainLoop()