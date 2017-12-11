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
        super().__init__(reconstructedHist,migrationMatrix)
        ### Be careful of underflow/overflow bins, may want to set to zero for all?
        self.tunfold = ROOT.TUnfoldDensity(cloneTNamedUUIDName(migrationMatrix))
        self.tunfold.SetInput(cloneTNamedUUIDName(reconstructedHist))

    def unfold(self,parameter):
        super().unfold(parameter)
        self.tunfold.DoUnfold(parameter)
        resultHist = self.tunfold.GetOutput(uuid.uuid1().hex)
        covarianceMatrix = self.tunfold.GetEmatrixTotal(uuid.uuid1().hex)
        result = UnfoldResult(self,resultHist,covarianceMatrix,parameter)
        return result
