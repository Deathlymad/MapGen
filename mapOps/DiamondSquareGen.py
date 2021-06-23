import numpy as np
from .AbstractSidebar import AbstractSidebar
from ui import SliderPanel
from noiseGen import NoiseGen
import functools
import math

def _square_displace(m, i, j, half_step, computePoint):
    """
    Defines the midpoint displacement for the square step
    :param DS_array:
    :param i:
    :param j:
    :param half_step:
    :param roughness:
    :return:
    """
    _sum = 0.0
    divide_by = 4

    # check cell "above"
    if i - half_step >= 0:
        _sum += m[i-half_step, j]
    else:
        divide_by -= 1

    # check cell "below"
    if i + half_step < m.shape[0]:
        _sum += m[i+half_step, j]
    else:
        divide_by -= 1

    # check cell "left"
    if j - half_step >= 0:
        _sum += m[i, j-half_step]
    else:
        divide_by -= 1

    # check cell "right"
    if j + half_step < m.shape[0]:
        _sum += m[i, j+half_step]
    else:
        divide_by -= 1

    ave = _sum / divide_by
    
    return computePoint(ave, i, j)

def diamond_square(m, resolution, computePoint):
    
    m[0][0] = computePoint(0,0,0)
    m[0][-1] = computePoint(0,0,1)
    m[-1][0] = computePoint(0,1,0)
    m[-1][-1] = computePoint(0,1,1)
    
    for i in reversed(range(resolution)):
        step_size = int(math.pow(2, i))
        
        half_step = int(math.floor(step_size/2))
        x_steps = range(half_step, m.shape[0], step_size)
        y_steps = x_steps[:]
        
        for i in x_steps:
            for j in y_steps:
                if m[i,j] == -1.0:
                    ul = m[i-half_step, j-half_step]
                    ur = m[i-half_step, j+half_step]
                    ll = m[i+half_step, j-half_step]
                    lr = m[i+half_step, j+half_step]

                    ave = (ul + ur + ll + lr)/4.0
                    
                    m[i,j] = computePoint(ave, i, j)
        # vertical step
        steps_x_vert = range(half_step, m.shape[0], step_size)
        steps_y_vert = range(0, m.shape[1], step_size)

        # horizontal step
        steps_x_horiz = range(0, m.shape[0],   int(step_size))
        steps_y_horiz = range(half_step, m.shape[1],   int(step_size))
        
        for i in steps_x_horiz:
            for j in steps_y_horiz:
                m[i,j] = _square_displace(m, i, j, half_step, computePoint)

        for i in steps_x_vert:
            for j in steps_y_vert:
                m[i,j] = _square_displace(m, i, j, half_step, computePoint)


class DiamondSquareGen(AbstractSidebar):
    
    def __init__(self):
        AbstractSidebar.__init__(self)
        
        self.AverageWeight = 1
        self.RandomWeight = 1
        self.Noise = 1

    def addSidebarProperties(self, panel):
        smSlider = SliderPanel(panel, "SmoothSlider", 0, 100, self.updateAvg)
        enSlider = SliderPanel(panel, "EntropySlider", 0, 100, self.updateRand)
        slSlider = SliderPanel(panel, "SlopeSlider", 0, 100, self.updateNoise)
        
        return [smSlider, enSlider, slSlider]
    
    def updateAvg(self, evt):
        self.AverageWeight = evt.EventObject.GetValue() / 100
    def updateRand(self, evt):
        self.RandomWeight = evt.EventObject.GetValue() / 100
    def updateNoise(self, evt):
        self.Noise = evt.EventObject.GetValue() / 100
    
    def getChange(self, progressCtx, resolution, avg, i, j):
        progressCtx.SetValue(progressCtx.GetValue() + 1)
        r = 0.1#random_func(i, j)
        n = self.generator.NoiseAtPos2(i / ((2 ** resolution) - resolution), j / ((2 ** resolution) - resolution)) ** 2
        
        return avg * self.AverageWeight + self.RandomWeight * r + self.Noise * n
    
    def init(self, context, progressCtx):
        self.generator = NoiseGen(context.seed)
    
    def apply(self, context, progressCtx):
        
        progressCtx.SetValue(0)
        progressCtx.SetRange(3 * (context.data["sideLen"] ** 2))
        
        diamond_square(context.map, context.data["resolution"], functools.partial(self.getChange, progressCtx, context.data["resolution"]))
        
        
        
    