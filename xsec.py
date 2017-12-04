"""
Classes to handle unfolding a thick-target cross-section measurement
"""

import utilities
import unfold_base

class XsecUnfolder(object):
    """
    User-facing class for unfolding cross-sections
    """
    
    def __init__(self,dz,density,
                        numRecoHist,denomRecoHist,
                        numMigrationMatrix,denomMigrationMatrix,
                        numEfficiencyHist=None,denomEfficiencyHist=None,
                        numBackgroundHistList=[],denomBackgroundHistList=[],
                        numMigrationMatrixUncList=[],denomMigrationMatrixUncList=[]):
        """
        Inputs:
            dz: float thickness of thin slab (distance between 
                wires in average particle direction)
            density: float argon number density per volume
            numRecoHist: TH1 reconstructed numerator histogram to unfold
            denomRecoHist: TH1 reconstructed denominator histogram to unfold
            numMigrationMatrix: TH2 migration to use for unfolding denominator; true v reconstructed
            denomMigrationMatrix: TH2 migration to use for unfolding denominator; true v reconstructed
            numEfficiencyHist: optional TH1 efficiency of numerator in bins of true
            denomEfficiencyHist: optional TH1 efficiency of denominator in bins of true
            numBackgroundHistList: list of TH1 background count of numerator in bins of reco; 
                                    histo errors are taken as 1 sigma systematic uncertainties
            denomBackgroundHistList: list of TH1 background count of denominator in bins of reco;
                                    histo errors are taken as 1 sigma systematic uncertainties
            numMigrationMatrixUncList: list of TH2 migration matrix systematic uncertainties for numerator;
                                    each bin should be the relative 1 sigma systematic uncertainty
                                    e.g. 0.1 for 10% uncertainty
            denomMigrationMatrixUncList: list of TH2 migration matrix systematic uncertainties for denominator;
                                    each bin should be the relative 1 sigma systematic uncertainty
                                    e.g. 0.1 for 10% uncertainty
        """

        try:
            dz = float(dz)
        except ValueError:
            raise ValueError("Could not convert dz to float: ",dz)
        try:
            density = float(density)
        except ValueError:
            raise ValueError("Could not convert density to float: ",density)
        if not isinstance(numRecoHist,ROOT.TH1):
            raise TypeError("numRecoHist doesn't inherit from TH1",type(numRecoHist))
        if isinstance(numRecoHist,ROOT.TH2):
            raise NotImplementedError("numRecoHist inherits from TH2, 2D unfolding not yet implemented")
        if not isinstance(denomRecoHist,ROOT.TH1):
            raise TypeError("denomRecoHist doesn't inherit from TH1",type(denomRecoHist))
        if isinstance(denomRecoHist,ROOT.TH2):
            raise NotImplementedError("denomRecoHist inherits from TH2, 2D unfolding not yet implemented")
        if not isinstance(numMigrationMatrix,ROOT.TH2):
            raise TypeError("numMigrationMatrix doesn't inherit from TH2",type(numMigrationMatrix))
        if not isinstance(denomMigrationMatrix,ROOT.TH2):
            raise TypeError("denomMigrationMatrix doesn't inherit from TH2",type(denomMigrationMatrix))

        if not (numEfficiencyHist is None):
            if not isinstance(numEfficiencyHist,ROOT.TH1):
                raise TypeError("numEfficiencyHist doesn't inherit from TH1",type(numEfficiencyHist))
            if isinstance(numEfficiencyHist,ROOT.TH2):
                raise NotImplementedError("numEfficiencyHist inherits from TH2, 2D unfolding not yet implemented")
        if not (denomEfficiencyHist is None):
            if not isinstance(denomEfficiencyHist,ROOT.TH1):
                raise TypeError("denomEfficiencyHist doesn't inherit from TH1",type(denomEfficiencyHist))
            if isinstance(denomEfficiencyHist,ROOT.TH2):
                raise NotImplementedError("denomEfficiencyHist inherits from TH2, 2D unfolding not yet implemented")

        for numBackgroundHist in numBackgroundHistList:
            if not isinstance(numBackgroundHist,ROOT.TH1):
                raise TypeError("numBackgroundHist doesn't inherit from TH1",type(numBackgroundHist))
            if isinstance(numBackgroundHist,ROOT.TH2):
                raise NotImplementedError("numBackgroundHist inherits from TH2, 2D unfolding not yet implemented")
        for denomBackgroundHist in denomBackgroundHistList:
            if not isinstance(denomBackgroundHist,ROOT.TH1):
                raise TypeError("denomBackgroundHist doesn't inherit from TH1",type(denomBackgroundHist))
            if isinstance(denomBackgroundHist,ROOT.TH2):
                raise NotImplementedError("denomBackgroundHist inherits from TH2, 2D unfolding not yet implemented")

        for numMigrationMatrixUnc in numMigrationMatrixUncList:
            if not isinstance(numMigrationMatrixUnc,ROOT.TH2):
                raise TypeError("numMigrationMatrixUnc doesn't inherit from TH2",type(numMigrationMatrixUnc))
        for denomMigrationMatrixUnc in denomMigrationMatrixUncList:
            if not isinstance(denomMigrationMatrixUnc,ROOT.TH2):
                raise TypeError("denomMigrationMatrixUnc doesn't inherit from TH2",type(denomMigrationMatrixUnc))

        self.dz = dz
        self.density = density
        self.numRecoHist = numRecoHist
        self.denomRecoHist = denomRecoHist
        self.numMigrationMatrix = numMigrationMatrix
        self.denomMigrationMatrix = denomMigrationMatrix
        self.numEfficiencyHist = numEfficiencyHist
        self.denomEfficiencyHist = denomEfficiencyHist
        self.numBackgroundHistList = numBackgroundHistList
        self.denomBackgroundHistList = denomBackgroundHistList
        self.numMigrationMatrixUncList = numMigrationMatrixUncList
        self.denomMigrationMatrixUncList = denomMigrationMatrixUncList

    def unfold(self,unfoldingClass,numParameter,denomParameter):
        """
        Method to perform unfolding and produce a result
        Inputs:
            unfoldingClass: the unfolding technique class to use for unfolding
            numParameter: the regularization, n-iterations, etc. input parameter
                                    for unfolding the numerator histogram
            denomParameter: the regularization, n-iterations, etc. input parameter
                                    for unfolding the denominator histogram
        Outputs:
            XsecUnfoldResult
        """

        numUnfolding = unfoldingClass(self.numRecoHist,self.numMigrationMatrix)
        denomUnfolding = unfoldingClass(self.denomRecoHist,self.denomMigrationMatrix)
        
        numUnfoldResult = numUnfolding.unfold(numParameter)
        denomUnfoldResult = denomUnfolding.unfold(denomParameter)

        result = XsecUnfoldResult(self,numUnfoldResult,denomUnfoldResult)
        return result

class XsecUnfoldResult(object):
    """
    Holds result of XsecUnfolder class for a specific technique and set of parameters
    """

    def __init__(self,xsecUnfolder,numUnfoldResult,denomUnfoldResult):
        """
        Inputs:
            xsecUnfolder: the XsecUnfolder object used to unfold
            numUnfoldResult: the numerator UnfoldResult object
            denomUnfoldResult: the denominator UnfoldResult object
        """

        if not isinstance(xsecUnfolder,XsecUnfolder):
            raise TypeError("xsecUnfolder isn't a XsecUnfolder",type(xsecUnfolder))
        if not isinstance(numUnfoldResult,UnfoldResult):
            raise TypeError("numUnfoldResult isn't a UnfoldResult",type(numUnfoldResult))
        if not isinstance(denomUnfoldResult,UnfoldResult):
            raise TypeError("denomUnfoldResult isn't a UnfoldResult",type(denomUnfoldResult))

        self.xsecUnfolder = xsecUnfolder
        self.numUnfoldResult = numUnfoldResult
        self.denomUnfoldResult = denomUnfoldResult

    def getResult(self):
        result = self.numUnfoldResult.getResult()
        result.Divide(self.denomUnfoldResult.getResult())
        scaleFactor = 1./(self.xsecUnfolder.density*self.xsecUnfolder.dz)
        result.Scale(scaleFactor)
        return result
        
    def plotResult(self):
        pass
