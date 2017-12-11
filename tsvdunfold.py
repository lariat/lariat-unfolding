"""
TSVDUnfold implementation of the Unfolding class
"""

import ROOT
from unfold_base import Unfolding, UnfoldResult
from utilities import cloneTNamedUUIDName

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

        self.tsvdunfold = ROOT.TSVDUnfold(reconstructedHist,
                                            simRecoHist,
                                            simTrueHist,
                                            migrationMatrix
                                        )
        
    def unfold(self,parameter=None):
        """
        Method to unfold with regularization, n-iterations, etc. input parameter
        Inputs:
            parameter: the regularization, n-iterations, etc. input parameter
        Outputs:
            UnfoldResult
        """

        super(UnfoldingTSVDUnfold,self).unfold(parameter)
        resultHist = self.tsvdunfold.Unfold(parameter)
        covarianceMatrix = self.tsvdunfold.GetXtau()
        result = UnfoldResult(self, resultHist, covarianceMatrix, parameter)
        return result

if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    from utilities import *

    trueDataHist, recoDataHist, trueMCHist, recoMCHist, migrationMatrix = CreateFakeData(2000,30000,10,10,0,0)

    u = UnfoldingTSVDUnfold(recoDataHist,migrationMatrix,recoMCHist,trueMCHist)
    u.plotReconstructedHist("testSVDReco.png")
    u.plotMigrationMatrix("testSVDMigrate.png")
    r = u.unfold(5)
    r.plotResult("testSVDFinal.png")
    r.plotCovarianceMatrix("testSVDFinalCov.png")
