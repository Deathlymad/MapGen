import wx
import numpy as np

class HostWindow(wx.Frame):
    def __init__(self, pipeline):
        wx.Frame.__init__(self, None, pos=(200,100), size=(800,600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        
        
        self.display = wx.Panel(self)
        self.display.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.progressGauge = wx.Gauge(self)
        
        self.ProgressSizeWrapper = wx.BoxSizer(wx.VERTICAL)
        self.HeadSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SidebarSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.placeholderSidebar = wx.StaticText(self, label="PLACEHOLDER")
        self.finishedSidebar = wx.StaticText(self, label="FINISHED")
        self.finishedSidebar.Hide()
        
        self.SidebarSizer.Add(self.placeholderSidebar, 15, wx.EXPAND)
        
        #Store pipeline data and init the state
        self.pipelineContext = pipeline
        self.currentSidebar = self.placeholderSidebar
        for sidebar in self.pipelineContext.getSidebars(self):
            self.SidebarSizer.AddStretchSpacer(1)
            self.SidebarSizer.Add(sidebar, 15, wx.EXPAND)
            sidebar.Hide()
        
        self.SidebarSizer.Layout()
        
        self.StepPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        #create the forward/backward buttons and bind their data
        self.backBtn = wx.Button(self, label="<< Back")
        self.backBtn.Bind(wx.EVT_BUTTON, self.onStepBackward)
        self.backBtn.Disable()
        self.nextBtn = wx.Button(self, label="Next >>")
        self.nextBtn.Bind(wx.EVT_BUTTON, self.onStepForward)
        
        #Structure the Bottom back and next buttons
        self.StepPanelSizer.AddStretchSpacer(1)
        self.StepPanelSizer.Add(self.backBtn, 3, wx.EXPAND)
        self.StepPanelSizer.AddStretchSpacer(1)
        self.StepPanelSizer.Add(self.nextBtn, 3, wx.EXPAND)
        self.StepPanelSizer.AddStretchSpacer(1)
        
        #Add the Button Panel to the Sidebar
        self.SidebarSizer.AddStretchSpacer(1)
        self.SidebarSizer.Add(self.StepPanelSizer, 2, wx.EXPAND)
        self.SidebarSizer.AddStretchSpacer(1)
        
        #Create the Sidebar and the Image
        self.HeadSizer.Add(self.SidebarSizer, 5, wx.EXPAND)
        self.HeadSizer.Add(self.display, 8, wx.EXPAND)
        self.ProgressSizeWrapper.Add(self.HeadSizer, 20, wx.EXPAND)
        self.ProgressSizeWrapper.Add(self.progressGauge, 1, wx.EXPAND)
        self.SetSizer(self.ProgressSizeWrapper)
        
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.pipelineContext.init(self.progressGauge)
    
    def onStepForward(self, evt):
        #backup data to reload it
        if (self.placeholderSidebar.IsShown()):
            self.placeholderSidebar.Hide()
        else:
            self.currentSidebar.Hide()
        self.currentSidebar = self.pipelineContext.Next(self.progressGauge)
        if (self.currentSidebar is None):
            self.finishedSidebar.Show()
            self.nextBtn.Disable()
        else:
            self.backBtn.Enable()
            
        self.SidebarSizer.Layout()
        
        map = self.pipelineContext.getCurrentImage()
        
        if map is not None:
            oldDisplay = self.display.GetSizer().Clear() #not sure this will destroy
            if oldDisplay is not None:
                oldDisplay.FindWindowByName("Map").Destroy()
            mapSize = map.shape[0]
            if (len(map.shape) < 3):
                map = map - np.min(map)
                if (np.ptp(map) != 0):
                    map = 255 * map / np.ptp(map)
                map = map.astype(np.uint8)
                m = np.stack([map, map, map], axis = -1)
            
            newMap = wx.StaticBitmap(self.display, bitmap = wx.Bitmap.FromBuffer(mapSize, mapSize, m.flatten()), name = "Map")
            self.display.GetSizer().Add(newMap)
    
    def onStepBackward(self, evt):
        #reset to last stage move backwards in Pipeline
        self.backBtn.Disable()
        
    
    def onClose(self, evt):
        
        evt.Skip()
