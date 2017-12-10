"""
Implemenation of low-level unfolding classes
"""

import uuid
import ROOT
from unfold_base import Unfold, UnfoldResult
from utilities import cloneTNamedUUIDName

class UnfoldTUnfold(Unfold):
    """
    Unfold using ROOT TUnfold class
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
        unfoldingMatrix = self.tunfold.GetEmatrixTotal(uuid.uuid1().hex)
        result = UnfoldResult(self,resultHist,unfoldingMatrix,parameter)
        return result
