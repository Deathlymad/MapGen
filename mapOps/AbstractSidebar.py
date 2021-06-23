import wx

class AbstractSidebar():
    
    def __init__(self):
        self.sidebarPanel = None
        self.sidebarPanelState = True
    
    def addSidebarProperties(self, panel):
        #add the different objects.
        raise NotImplementedError()
    
    def init(self, context, progressCtx):
        #execute step on context
        raise NotImplementedError()
    
    def apply(self, context, progressCtx):
        #execute step on context
        raise NotImplementedError()
    
    def generateSidebar(self, parent):
        if self.sidebarPanel is not None:
            return self.sidebarPanel
        else:
            panel = wx.Panel(parent)
            
            sizer = wx.BoxSizer(wx.VERTICAL)
            
            objects = self.addSidebarProperties(panel)
            
            for o in objects:
                sizer.Add(o, 1, wx.EXPAND)
            
            panel.SetSizer(sizer)
            
            panel.Layout()
            
            if (self.sidebarPanelState):
                panel.Show()
            else:
                panel.Hide()
            
            self.sidebarPanel = panel
            return panel
    
    def Show(self):
        if self.sidebarPanel is not None:
            self.sidebarPanel.Show()
        else:
            self.sidebarPanelState = True
            
    def Hide(self):
        if self.sidebarPanel is not None:
            self.sidebarPanel.Hide()
        else:
            self.sidebarPanelState = False