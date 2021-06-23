import wx
from ui import HostWindow
from pipeline import Pipeline
from mapOps import SetupMapBuffer
from mapOps import DiamondSquareGen

#return 

dataPipeline = Pipeline([SetupMapBuffer(), DiamondSquareGen()])

app = wx.App()
window = HostWindow(dataPipeline)
window.Show()
app.MainLoop()
