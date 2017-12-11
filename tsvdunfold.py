"""
TSVDUnfold implementation of the Unfolding class
"""

import ROOT
from unfold_base import Unfolding, UnfoldResult
import utilities

class UnfoldingTSVDUnfold(Unfolding):
    """
    Low-level unfolding class using ROOTi TSVDUnfold 
    """

    def __init__(self,reconstructedHist,migrationMatrix,simRecoHist,simTrueHist):
        """
        Unfolding Constructor
        Inputs:
            reconstructedHist: TH1 reconstructed histogram to unfold
            migrationMatrix: TH2 migration matrix to use for unfolding true v reconstructed
            simRecoHist: TH1 reconstructed simulation histogram corrosponding to simTrueHist and migrationMatrix
            simTrueHist: TH1 true simulation histogram corresponding to simTrueHist and migrationMatrix
        """
        super(UnfoldingTSVDUnfold, self).__init__(reconstructedHist,migrationMatrix)

        if not isinstance(simRecoHist,ROOT.TH1):
            raise TypeError("simRecoHist doesn't inherit from TH1",type(simRecoHist))
        if isinstance(simRecoHist,ROOT.TH2):
            raise NotImplementedError("simRecoHist inherits from TH2, 2D unfolding not yet implemented")
        if not isinstance(simTrueHist,ROOT.TH1):
            raise TypeError("simTrueHist doesn't inherit from TH1",type(simTrueHist))
        if isinstance(simTrueHist,ROOT.TH2):
            raise NotImplementedError("simTrueHist inherits from TH2, 2D unfolding not yet implemented")


        if not isinstance(reconstructedHist,ROOT.TH1D):
            raise TypeError("reconstructedHist must be TH1D not",type(reconstructedHist))
        if not isinstance(migrationMatrix,ROOT.TH2D):
            raise TypeError("migrationMatrix must be TH2D not",type(migrationMatrix))
        if not isinstance(simRecoHist,ROOT.TH1D):
            raise TypeError("simRecoHist must be TH1D not",type(simRecoHist))
        if not isinstance(simTrueHist,ROOT.TH1D):
            raise TypeError("simTrueHist must be TH1D not",type(simTrueHist))

        self.simRecoHist = simRecoHist
        self.simTrueHist = simTrueHist

        self.tsvdunfold = ROOT.TSVDUnfold(reconstructedHist,simRecoHist,simTrueHist,migrationMatrix)
        
    def unfold(self,parameter=None):
        """
        Method to unfold with regularization, n-iterations, etc. input parameter
        Inputs:
            parameter: the regularization, n-iterations, etc. input parameter
        Outputs:
            UnfoldResult
        """

        resultHist = self.tsvdunfold.Unfold(parameter)
        covarianceMatrix = self.tsvdunfold.GetXtau()
        result = UnfoldResult(self, resultHist, covarianceMatrix, parameter)
        return result

if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    from utilities import *
    import numpy

    c = ROOT.TCanvas("c")
    
    N = 100
    trueData = numpy.random.rand(N) # N samples uniform [0,1)
    recoData = trueData+numpy.random.rand(N)*0.1 # random normal dist

    trueMC = numpy.random.rand(N) # N samples uniform [0,1)
    recoMC = trueData+numpy.random.rand(N)*0.1 # random normal dist

    trueDataHist = HistUUID(10,0,1,TH1D=True)
    recoDataHist = HistUUID(10,0,1,TH1D=True)
    for t, r in zip(trueData,recoData):
        trueDataHist.Fill(t)
        recoDataHist.Fill(r)

    trueMCHist = HistUUID(10,0,1,TH1D=True)
    recoMCHist = HistUUID(10,0,1,TH1D=True)
    migrationMatrix = Hist2DUUID(10,0,1,10,0,1,TH2D=True)
    for t, r in zip(trueMC,recoMC):
        trueMCHist.Fill(t)
        recoMCHist.Fill(r)
        migrationMatrix.Fill(t,r)
    
    u = UnfoldingTSVDUnfold(recoDataHist,migrationMatrix,recoMCHist,trueMCHist)
    r = u.unfold(5)
    r.plotResult("testSVD.png")
    r.plotCovarianceMatrix("testSVDCov.png")
