import wx

class SliderPanel(wx.Panel):
    
    def __init__(self, parent, title, min, max, onSlide):
        wx.Panel.__init__(self, parent)
        
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title = wx.StaticText(self, label = title)
        self.slider = wx.Slider(self, minValue=min, maxValue=max, value=min)
        
        self.slider.Bind(wx.EVT_SCROLL, onSlide)
        
        self.MainSizer.AddStretchSpacer(1)
        self.MainSizer.Add(self.title, 3, wx.EXPAND)
        self.MainSizer.AddStretchSpacer(1)
        self.MainSizer.Add(self.slider, 3, wx.EXPAND)
        self.MainSizer.AddStretchSpacer(1)
        
        self.SetSizer(self.MainSizer)
    
    