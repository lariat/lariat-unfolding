"""
Implemenation of low-level unfolding class using ROOT TUnfold
"""

import uuid
import ROOT
from unfold_base import Unfolding, UnfoldResult
from utilities import cloneTNamedUUIDName

class UnfoldingTUnfold(Unfolding):
    """
    Unfolding using ROOT TUnfold class
    """

    def __init__(self,reconstructedHist,migrationMatrix):
        super(UnfoldingTUnfold, self).__init__(reconstructedHist,migrationMatrix)
        ### Be careful of underflow/overflow bins, may want to set to zero for all?
        self.tunfold = ROOT.TUnfoldDensity(cloneTNamedUUIDName(migrationMatrix),ROOT.TUnfold.kHistMapOutputVert)
        errCode = self.tunfold.SetInput(cloneTNamedUUIDName(reconstructedHist))
        if errCode >= 10000:
            print("Warning: TUnfold doesn't think input data can make unfolding work")

    def unfold(self,parameter):
        super(UnfoldingTUnfold,self).unfold(parameter)
        self.tunfold.DoUnfold(parameter)
        resultHist = self.tunfold.GetOutput(uuid.uuid1().hex)
        covarianceMatrix = self.tunfold.GetEmatrixTotal(uuid.uuid1().hex)
        result = UnfoldResult(self,resultHist,covarianceMatrix,parameter)
        return result

if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    from utilities import *

    trueDataHist, recoDataHist, trueMCHist, recoMCHist, migrationMatrix = CreateFakeData(2000,30000,10,10,0,0)

    u = UnfoldingTUnfold(recoDataHist,migrationMatrix)
    u.plotReconstructedHist("testTUnfoldReco.png")
    u.plotMigrationMatrix("testTUnfoldMigrate.png")
    r = u.unfold(5)
    r.plotResult("testTUnfoldFinal.png")
    r.plotCovarianceMatrix("testTUnfoldFinalCov.png")
