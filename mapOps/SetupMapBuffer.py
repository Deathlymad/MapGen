import numpy as np
from .AbstractSidebar import AbstractSidebar
from ui import SliderPanel

class SetupMapBuffer(AbstractSidebar):
    
    def __init__(self):
        AbstractSidebar.__init__(self)
        
        self.sizeExponent = 1

    def addSidebarProperties(self, panel):
        expSlider = SliderPanel(panel, "sizeExponent", 0, 10, self.updateExponent)
        
        return [expSlider]
    
    def updateExponent(self, evt):
        self.sizeExponent = evt.EventObject.GetValue()
    
    def init(self, context, progressCtx):
        pass
        
    def apply(self, context, progressCtx):
        progressCtx.SetValue(0)
        progressCtx.SetRange(1)
        
        size = ((2 ** self.sizeExponent) + 1)
        context.data["sideLen"] = size
        context.data["resolution"] = self.sizeExponent
        context.map = np.full((size, size), -1, dtype='float')
        
        progressCtx.Update()
    