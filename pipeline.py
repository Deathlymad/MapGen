from context import Context
import time

class Pipeline():
    
    def __init__(self, data):
        #should accept Object Array
        self.data = data
        self.pos = -1
        self.state = Context(round(time.time()))
    
    def init(self, progCtx):
        for e in self.data:
            e.init(self.state, progCtx)
    
    def Next(self, progCtx):
        if (self.pos >= 0):
            self.data[self.pos].apply(self.state, progCtx)
        self.pos += 1
        if (self.pos < len(self.data)):
            self.data[self.pos].Show()
            return self.data[self.pos]
        else:
            return None
    
    def getSidebars(self, parent):
        return [step.generateSidebar(parent) for step in self.data]
    
    def getCurrentImage(self):
        return self.state.map