"""
Utility Functions
"""

import ROOT
from ROOT import gStyle as gStyle
import uuid
import numbers
import numpy

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

def CreateFakeData(nData,nMC,nBinsReco,nBinsTrue,smearingData=0.1,smearingMC=0.1):
    """
    Creates a fake dataset for testing, histogram goes from 0 to 1.
    Data and MC are generated identically.

    Inputs:
      N: number of events
      nBins: number of bins
      smearing: relative smearing factor on reco

    Outputs:
        trueDataHist: true distribution of data
        recoDataHist: smeared distribution of data
        trueMCHist: true distribution of MC
        recoMCHist: true distribution of MC
        migrationMatrix: migration matrix of MC, reco v true
    """
    trueData = numpy.random.rand(nData) # N samples uniform [0,1)
    recoData = trueData+numpy.random.randn(nData)*smearingData # random normal dist

    trueMC = numpy.random.rand(nMC) # N samples uniform [0,1)
    recoMC = trueMC+numpy.random.randn(nMC)*smearingMC # random normal dist

    trueDataHist = HistUUID(nBinsTrue,0,1,TH1D=True)
    recoDataHist = HistUUID(nBinsReco,0,1,TH1D=True)
    for t, r in zip(trueData,recoData):
        trueDataHist.Fill(t)
        recoDataHist.Fill(r)

    trueMCHist = HistUUID(nBinsTrue,0,1,TH1D=True)
    recoMCHist = HistUUID(nBinsReco,0,1,TH1D=True)
    migrationMatrix = Hist2DUUID(nBinsTrue,0,1,nBinsReco,0,1,TH2D=True)
    for t, r in zip(trueMC,recoMC):
        trueMCHist.Fill(t)
        recoMCHist.Fill(r)
        migrationMatrix.Fill(t,r)
    return trueDataHist, recoDataHist, trueMCHist, recoMCHist, migrationMatrix

def setStyle():
  gStyle.SetCanvasColor(0)
  gStyle.SetCanvasBorderSize(10)
  gStyle.SetCanvasBorderMode(0)
  gStyle.SetCanvasDefH(700)
  gStyle.SetCanvasDefW(700)

  gStyle.SetPadColor       (0)
  gStyle.SetPadBorderSize  (10)
  gStyle.SetPadBorderMode  (0)
  gStyle.SetPadBottomMargin(0.13)
  gStyle.SetPadTopMargin   (0.08)
  gStyle.SetPadLeftMargin  (0.15)
  gStyle.SetPadRightMargin (0.05)
  gStyle.SetPadGridX       (0)
  gStyle.SetPadGridY       (0)
  gStyle.SetPadTickX       (1)
  gStyle.SetPadTickY       (1)

  gStyle.SetFrameFillStyle ( 0)
  gStyle.SetFrameFillColor ( 0)
  gStyle.SetFrameLineColor ( 1)
  gStyle.SetFrameLineStyle ( 0)
  gStyle.SetFrameLineWidth ( 1)
  gStyle.SetFrameBorderSize(10)
  gStyle.SetFrameBorderMode( 0)

  gStyle.SetNdivisions(505)

  gStyle.SetLineWidth(2)
  gStyle.SetHistLineWidth(2)
  gStyle.SetFrameLineWidth(2)
  gStyle.SetLegendFillColor(ROOT.kWhite)
  gStyle.SetLegendFont(42)
  gStyle.SetMarkerSize(1.2)
  gStyle.SetMarkerStyle(20)
  gStyle.SetHistLineColor(1)
 
  gStyle.SetLabelSize(0.040,"X")
  gStyle.SetLabelSize(0.040,"Y")

  gStyle.SetLabelOffset(0.010,"X")
  gStyle.SetLabelOffset(0.010,"Y")
 
  gStyle.SetLabelFont(42,"X")
  gStyle.SetLabelFont(42,"Y")
 
  gStyle.SetTitleBorderSize(0)
  gStyle.SetTitleFont(42)
  gStyle.SetTitleFont(42,"X")
  gStyle.SetTitleFont(42,"Y")

  gStyle.SetTitleSize(0.045,"X")
  gStyle.SetTitleSize(0.045,"Y")
 
  gStyle.SetTitleOffset(1.4,"X")
  gStyle.SetTitleOffset(1.6,"Y")
 
  gStyle.SetTextSize(0.055)
  gStyle.SetTextFont(42)
 
  gStyle.SetOptStat(0)
  gStyle.SetOptStat("nemr")
  
setStyle()

def setupCOLZFrame(pad,reset=False):
   if reset:
     pad.SetRightMargin(gStyle.GetPadRightMargin())
   else:
     pad.SetRightMargin(0.15)
     gStyle.SetOptStat(0)
