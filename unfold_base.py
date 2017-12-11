"""
Base classes for low-level unfolding
"""

import ROOT
import copy
from utilities import cloneTNamedUUIDName, CanvasUUID

class Unfolding(object):
    """
    Low-level unfolding technique base class for a single distribution

    Subclass this for each unfolding technique
    """

    def __init__(self,reconstructedHist,migrationMatrix):
        """
        Unfolding Constructor
        Inputs:
            reconstructedHist: TH1 reconstructed histogram to unfold
            migrationMatrix: TH2 migration matrix to use for unfolding true v reconstructed
        """
        if not isinstance(reconstructedHist,ROOT.TH1):
            raise TypeError("reconstructedHist doesn't inherit from TH1",type(reconstructedHist))
        if isinstance(reconstructedHist,ROOT.TH2):
            raise NotImplementedError("reconstructedHist inherits from TH2, 2D unfolding not yet implemented")
        if not isinstance(migrationMatrix,ROOT.TH2):
            raise TypeError("migrationMatrix doesn't inherit from TH2",type(migrationMatrix))

        self.reconstructedHist = reconstructedHist
        self.migrationMatrix = migrationMatrix
        
    def unfold(self,parameter=None):
        """
        Method to unfold with regularization, n-iterations, etc. input parameter
        Inputs:
            parameter: the regularization, n-iterations, etc. input parameter
        Outputs:
            UnfoldResult
        """
        pass

    def getReconstructedHist(self):
        return cloneTNamedUUIDName(self.reconstructedHist)
    def getMigrationMatrix(self):
        return cloneTNamedUUIDName(self.migrationMatrix)

class UnfoldResult(object):
    """
    Holds result of Unfolding class

    """

    def __init__(self,unfolding, resultHist, covarianceMatrix, parameter):
        """
        Inputs:
            unfolding: Unfolding class object used to create this result
            resultHist: TH1 result histogram
            covarianceMatrix: TH2 showing convariance of result
            parameter: the regularization, n-iterations, etc. input parameter
        """

        if not isinstance(unfolding,Unfolding):
            raise TypeError("unfolding doesn't inherit from Unfolding",type(unfolding))
        if not isinstance(covarianceMatrix,ROOT.TH2):
            raise TypeError("covarianceMatrix doesn't inherit from TH2",type(covarianceMatrix))

        if not isinstance(resultHist,ROOT.TH1):
            raise TypeError("resultHist doesn't inherit from TH1",type(resultHist))
        if isinstance(resultHist,ROOT.TH2):
            raise NotImplementedError("resultHist inherits from TH2, 2D unfolding not yet implemented")

        if not isinstance(covarianceMatrix,ROOT.TH2):
            raise TypeError("covarianceMatrix doesn't inherit from TH2",type(covarianceMatrix))

        self.unfolding = unfolding
        self.resultHist = resultHist
        self.covarianceMatrix = covarianceMatrix
        self.parameter = parameter

    def getReconstructedHist(self):
        return self.unfolding.getReconstructedHist()
    def getMigrationMatrix(self):
        return self.unfolding.getMigrationMatrix()
    def getResult(self):
        return cloneTNamedUUIDName(self.resultHist)
    def getCovarianceMatrix(self):
        return cloneTNamedUUIDName(self.covarianceMatrix)
    def getParameter(self):
        return copy.deepcopy(parameter)

    def plotResult(self,outfilename):
        c = CanvasUUID()
        resultHist = self.getResult()
        resultHist.Draw("E")
        c.SaveAs(outfilename)
        
    def plotCovarianceMatrix(self,outfilename):
        c = CanvasUUID()
        matrix = self.getCovarianceMatrix()
        matrix.Draw("colz")
        c.SaveAs(outfilename)
