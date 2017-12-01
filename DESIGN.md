LArIAT Unfolding Package Design
===============================

Requirements
------------

- Unfold distributions
- Implement modularity in the unfolding technique to compare different techniques
- Provide diagnostic plots that show unfolding is working
- Provide standardized pretty final plots
- User-friendly interface/API

General Design
--------------

- Use PyROOT
- Inputs/outputs are ROOT histograms
- Base classes:
  - Unfolding: low-level unfolding technique base class for a single distribution (incident or interacting, completely general)
  - UnfoldResult: holds unfolding result and produces plots based on the result for a single distribution (incident or interacting, completely general)
  - XsecUnfolder: user friendly class that manages input histos, calling of Unfolding class, and returns XsecUnfoldResult to user
  - XsecUnfoldResult: holds UnfoldResult for both numerator and denominator and produces final plot
- What to do about systematics e.g. on efficiency and background?

User Inputs
-----------

- float density: argon number density
- float dz: thickness of thin slab (distance between wires in the average particle direction)
- One each for incident and interacting (all reco binning must be the same and all true binning must be the same):
  - TH1 histogram N events reconstructed as a function of reconstructed KE
  - TH1 histogram estimate of N background events reconstructed as a function of reconstructed KE (histogram errors are 1 sigma systematic uncertainties on background, can be 0)
  - TH1 histogram estimate of the signal efficiency as a function of true KE (histogram errors are 1 sigma systematic uncertainties on efficiency, can be 0)
  - TH2 2D histogram migration matrix of only signal events. Y-binning should be reco, X-binning should be true. This is only for events that are reconstructed
  - optional list of TH2 2D histogram migration matrix systematic uncertainties. Each bin should be the relative 1 sigma systematic uncertainty e.g. 0.1 for 10% uncertainty.
- Unfolding technique specific regularization parameters

Output Histograms
-----------------

- One each for incident and interacting:
  - Background subtracted histogram in terms of reco KE
  - Unfolding matrix
  - Background subtracted histogram in terms of true KE
  - Background subtracted, efficiency corrected histogram in terms of true KE
  - Relative systematic uncertainty on background, efficiency, migration matrix, unfolding matrix, and unfolded histogram (by source as a reach goal)
- Final unfolded result histogram with uncertainty
