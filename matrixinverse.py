"""
Direct matrix inversion implementation of Unfolding class
"""

import ROOT
from unfold_base import Unfolding, UnfoldResult
from utilities import cloneTNamedUUIDName
import numpy

class UnfoldingMatrixInverse(Unfolding):
    """
    Low-level unfolding class using matrix inverse
    """

    def __init__(self,reconstructedHist,migrationMatrix):
        """
        Unfolding Constructor
        Inputs:
            reconstructedHist: TH1 reconstructed histogram to unfold
            migrationMatrix: TH2 migration matrix to use for unfolding true v reconstructed
        """
        super(UnfoldingMatrixInverse, self).__init__(reconstructedHist,migrationMatrix)
        if migrationMatrix.GetNbinsX() != migrationMatrix.GetNbinsY():
            raise Exception("migrationMatrix must be square for matrix inverse unfolding")
        
    def unfold(self,parameter=None):
        """
        Method to unfold with regularization, n-iterations, etc. input parameter
        Inputs:
            parameter: the regularization, n-iterations, etc. input parameter
        Outputs:
            UnfoldResult
        """

        super(UnfoldingMatrixInverse,self).unfold(parameter)

        nBins = self.reconstructedHist.GetNbinsX()
        y = numpy.zeros(nBins)
        yCov = numpy.zeros((nBins,nBins))
        for iBin in range(1,nBins+1):
            y[iBin-1] = self.reconstructedHist.GetBinContent(iBin)
            yCov[iBin-1][iBin-1] = (self.reconstructedHist.GetBinContent(iBin))**0.5
        inverseMatrix = numpy.linalg.inv(yCov)
        x = inverseMatrix.dot(y)
        xCov = inverseMatrix.dot(yCov.dot(inverseMatrix.T))

        resultHist = cloneTNamedUUIDName(self.reconstructedHist)
        resultHist.Reset()
        covarianceMatrix = cloneTNamedUUIDName(self.migrationMatrix)
        covarianceMatrix.Reset()
        for iBin in range(1,nBins+1):
          resultHist.SetBinContent(iBin,x[iBin-1])
          resultHist.SetBinError(iBin,xCov[iBin-1][iBin-1])
          for jBin in range(1,nBins+1):
            covarianceMatrix.SetBinContent(iBin,jBin,xCov[iBin-1][jBin-1])

        result = UnfoldResult(self, resultHist, covarianceMatrix, parameter)
        return result

if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    from utilities import *

    trueDataHist, recoDataHist, trueMCHist, recoMCHist, migrationMatrix = CreateFakeData(2000,30000,10,10,0,0)

    u = UnfoldingMatrixInverse(recoDataHist,migrationMatrix)
    u.plotReconstructedHist("testMatInvReco.png")
    u.plotMigrationMatrix("testMatInvMigrate.png")
    r = u.unfold()
    r.plotResult("testMatInvFinal.png")
    r.plotCovarianceMatrix("testMatInvFinalCov.png")
