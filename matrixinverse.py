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

        y = self.histToBinArray(self.reconstructedHist)
        yCov = numpy.diagflat(y**0.5)
        migrationMatrix = self.histToBinArray(self.migrationMatrix) 

        inverseMatrix = numpy.linalg.inv(migrationMatrix)
        x = inverseMatrix.dot(y)
        xCov = inverseMatrix.dot(yCov.dot(inverseMatrix.T))

        resultHist = self.binArrayToHist(x)
        covarianceMatrix = self.binArrayToHist(xCov,True)

        result = UnfoldResult(self, resultHist, covarianceMatrix, parameter)
        return result

    def histToBinArray(self,hist):
        if isinstance(hist,ROOT.TH2):
            nBins = hist.GetNbinsX()
            assert(hist.GetNbinsY() == nBins)
            result = numpy.zeros((nBins,nBins))
            for iBin in range(1,nBins+1):
                for jBin in range(1,nBins+1):
                    result[iBin-1][jBin-1] = hist.GetBinContent(iBin,jBin)
            return result
        else:
            nBins = hist.GetNbinsX()
            result = numpy.zeros(nBins)
            for iBin in range(1,nBins+1):
                result[iBin-1] = hist.GetBinContent(iBin)
            return result

    def binArrayToHist(self,a, th2=False):
        if th2:
            result = cloneTNamedUUIDName(self.migrationMatrix)
            result.Reset()
            nBins = result.GetNbinsX()
            assert(hist.GetNbinsY() == nBins)
            assert(a.shape == (nBins,nBins))
            for iBin in range(1,nBins+1):
                for jBin in range(1,nBins+1):
                    result.SetBinContent(iBin,jBin,a[iBin-1][jBin-1])
            return result
        else:
            result = cloneTNamedUUIDName(self.reconstructedHist)
            result.Reset()
            nBins = result.GetNbinsX()
            for iBin in range(1,nBins+1):
                result.SetBinContent(iBin,a[iBin-1])
            return result

if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    from utilities import *

    trueDataHist, recoDataHist, trueMCHist, recoMCHist, migrationMatrix = CreateFakeData(2000,300,10,10,0.1,0.1)

    u = UnfoldingMatrixInverse(recoDataHist,migrationMatrix)
    u.plotReconstructedHist("testMatInvReco.png")
    u.plotMigrationMatrix("testMatInvMigrate.png")

    true = u.histToBinArray(trueMCHist)
    reco = u.histToBinArray(recoMCHist)
    migrate = u.histToBinArray(migrationMatrix)
    for i in range(migrate.shape[0]):
        #for j in range(migrate.shape[0]):
        #    migrate[i,j] += i

        rowsum = migrate[i,:].sum()
        columnsum = migrate[:,i].sum()
        print "rowsum %.f" % rowsum
        print "colsum          %.f" % columnsum
        #migrate[i,:] = migrate[i,:]/rowsum

        #migrate[:,i] = migrate[:,i]/columnsum

    print "true"
    print true
    print "reco"
    print reco
    print "migrate dot true"
    print migrate.dot(true)
    print "migrate"
    print migrate

    r = u.unfold()
    r.plotResult("testMatInvFinal.png")
    r.plotCovarianceMatrix("testMatInvFinalCov.png")
