LArIAT Unfolding Package Design
===============================

Requirements
------------

- Unfold distributions
- Implement modularity in unfolding technique to compare different techniques
- Provide diagnostic plots that unfolding is working
- Provide standardized pretty final plots
- User-friendly interface/API

General Design
--------------

- Use PyROOT
- Inputs/outputs are ROOT histograms
- Base classes:
  - Unfolding: low-level unfolding technique base class
  - UnfoldResult: holds unfolding result and produces plots based on the result (diagnostic and pretty final plots)
  - Unfolder: user friendly class that manages input histos, calling of Unfolding class, and returns UnfoldResult to user
- What to do about systematics e.g. on efficiency and background?

User Inputs
-----------

- float density: argon number density
- float dz: distance between measurements (distance between wire planes in the average particle direction)
- One each for incident and interacting (all reco binning must be the same and all true binning must be the same):
  - TH1 histogram N events reconstructed as a function of reconstructed KE
  - TH1 histogram estimate of N background events reconstructed as a function of reconstructed KE
  - TH1 histogram estimate of the signal efficiency as a function of true KE
  - TH2 2D histogram migration matrix of only signal events. Y-binning should be reco, X-binning should be true. This is only for events that are reconstructed (don't apply efficiency corrections)
- Unfolding technique specific regularization parameters

Output Histograms
-----------------

- One each for incident and interacting:
  - Background subtracted histogram in terms of reco KE
  - Unfolding matrix
  - Background subtracted histogram in terms of true KE
  - Background subtracted, efficiency corrected histogram in terms of true KE
