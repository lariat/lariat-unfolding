"""
Utility Functions
"""

import ROOT
import uuid
import numbers

def cloneTNamedUUIDName(hist):
    return hist.Clone(uuid.uuid1().hex)

def CanvasUUID():
   return ROOT.TCanvas(uuid.uuid1().hex)

def HistUUID(*args,**kargs):
  """
  Returns TH1F/TH1D/TEfficiency with UUID for name and "" for title.
  Positional arguments:
    either:
        nBins: number of histogram bins
        xLow: lowest histogram bin low edge
        xHigh: highest histogram bin high edge
    or:
        xBinEdges: A list of bin edges
  Keyword arguments:
    TH1D: if TH1D=True, hist will be TH1D
    TEfficiency: if TEfficiency=True, will be TEfficiency instead of TH1F
  Outputs:
    ROOT 1D histogram or TEfficiency
  """
  func = ROOT.TH1F
  if "TH1D" in kargs and kargs["TH1D"]:
    func = ROOT.TH1D
  if "TEfficiency" in kargs and kargs["TEfficiency"]:
    func = ROOT.TEfficiency
  name = uuid.uuid1().hex
  hist = None
  if len(args) == 1 and type(args[0]) == list:
    hist = func(name,"",len(args[0])-1,array.array('f',args[0]))
  elif len(args) == 3:
    for i in range(3):
      if not isinstance(args[i],numbers.Number):
        raise Exception(i,"th argument is not a number")
    hist = func(name,"",args[0],args[1],args[2])
  else:
    raise Exception("Hist: Innapropriate arguments, requires either nBins, low, high or a list of bin edges:",args)
  return hist

def Hist2DUUID(*args,**kargs):
  """
  Returns TH2F/TH2D/2D-TEfficiency with UUID for name and "" for title.
  Positional arguments:
    either:
        nBinsX: number of histogram bins
        xLow: lowest histogram bin low edge
        xHigh: highest histogram bin high edge
        nBinsY: number of histogram bins
        yLow: lowest histogram bin low edge
        yHigh: highest histogram bin high edge
    or:
        xBinEdges: a list of bin edges
        yBinEdges: a list of bin edges
  Keyword arguments:
    TH2D: if TH2D=True, hist will be TH2D
    TEfficiency: if TEfficiency=True, will be TEfficiency instead of TH2F
  Outputs:
    ROOT 2D histogram or 2D TEfficiency
  """
  func = ROOT.TH2F
  if "TH2D" in kargs and kargs["TH2D"]:
    func = ROOT.TH2D
  if "TEfficiency" in kargs and kargs["TEfficiency"]:
    func = ROOT.TEfficiency
  name = uuid.uuid1().hex
  hist = None
  if len(args) == 2 and type(args[0]) == list and type(args[1]) == list:
    hist = func(name,"",len(args[0])-1,array.array('f',args[0]),len(args[1])-1,array.array('f',args[1]))
  elif len(args) == 6:
    for i in range(6):
      if not isinstance(args[i],numbers.Number):
        raise Exception(i,"th argument is not a number")
    hist = func(name,"",args[0],args[1],args[2],args[3],args[4],args[5])
  elif len(args) == 4:
    if type(args[0]) == list:
      for i in range(1,4):
        if not isinstance(args[i],numbers.Number):
          raise Exception(i,"th argument is not a number")
      hist = func(name,"",len(args[0])-1,array.array('d',args[0]),args[1],args[2],args[3])
    elif type(args[3]) == list:
      for i in range(3):
        if not isinstance(args[i],numbers.Number):
          raise Exception(i,"th argument is not a number")
      hist = func(name,"",args[0],args[1],args[2],len(args[3])-1,array.array('d',args[3]))
  else:
    raise Exception("Hist: Innapropriate arguments, requires either nBins, low, high or a list of bin edges:",args)
  return hist
