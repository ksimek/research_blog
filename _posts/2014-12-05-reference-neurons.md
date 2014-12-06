---
layout: post
title: "Neuron work planning"
description: ""
category: 'reference'
tags: []
---
{% include JB/setup %}

Input data: Skeleton graph
* nodes: junctions (data: none)
* edges: curves (data: curve points + indices)

Ouptut data: curve graph
* nodes: curves (data: curve points + indices)
* edges: branches (data: branch point and index offset)

Converting from skeleton graph to curve graph requires a "resolution" for each junction
  4 possible resolutions for three-way graph { (ab,c) (a,bc) (ac,b) (a,b,c) }
  6 possible resolutions for 4-way graph

Special case: loops
        
  a <-> b <-> c <-> d <-> a
        ^     ^     ^     
        |     |     |
        V     v     v
        e     f     g

  above, subgraph {a,b,c,d} constitutes a loop.
  requires "loop resolution": pick two endpoints and interpolate (estimating the index changebetween them). the remaining junction nodes become lateral branches (which require their offsets).

    struct loop_resolution
    {
      int endpoint_1;
      int endpoint_2;
      double index_delta;
      double lateral_branch_index[n];
      double lateral_index_deltas[n];
    }

Inference
------------
preprocess: compute putative junction resolution branch poionts
preprocess: compute putative loop resolution branch points and index offsets

* Ideal method: Gibbs sample over junction/loop resolutions.  Metropolis sample model parameters.
* Metropolis method 1: To avoid computing full BGP marginal likelihood at each sample, compute local improvement at each junction/loop. Occasionally evaluate full BGP and accept/reject based on difference between local improvement and global improvement.
* Metropolis method 2: After each global improvement, extend local curves using junction resolutions.  New junction resolutions can use this information to improve local estimates.
      
dependency flow:
-----------------
skeleton_graph plus junction resolutions implies curve graph
Curve graph plus BGP parameters implies BGP matrix
BGP matrix plus BGP mean implies marginal likelihood

Model:
---------
    Curve covariance: smooth central curve plus mean-reverting random-walk plus small iid noise (for quantization error)
        smooth central curve: either cubic spline GP or squared-exponential GP w/ initial constraints
        random walk curve: Ornstein-Uhlenbeck GP
    
  
Training:
----------
manually specify all junction and loop resolutions
per image:
    argmax smoothness covariance , random walk covariance, 
        compute BGP covariance matrix
fix a distribution over smoothness covariance and random walk covariance

Straw man:
------------
A. Resolve using best linear fit and threshold
B. resolve using trained SVM
C. resolve using sampling with manually-set parameters (aka "first pass" below)


First pass: no training
--------
    don't train.  set covariances somewhat randomly (overestimate; use matlab generate samples and eyeball )
    use full gibbs sampling and run for several days.

Second pass: training, don't sample model parameters.
---------------
    gather ground truth on all 8 datasets (imagej? c++?)
    train parameters for all 8 datasets
    fit parameter model to 7 datasets; inference on 8th.
    For each parameter covariance, use largest over all training 7 datasets (no gibbs sampling)

Third pass: full model (training and sampling model parameters
-----------------------
    self explanatory

Fourth pass: full model  w/ metropolis method 1
-----------------------
    (see "metropolis method 1" above, under "inference")
    Use local marginal likelihood during Gibbs sampling; periodically accept/reject new model using metropolis method on full marginal likelihood.
    don't update local curves after accepting 

Fifth pass: full model  w/ metropolis method 2
-----------------------
    (see "metropolis method 2" above, under "inference")
    same as previous, but update local curves after accepting.
    Should result in better acceptance, faster convergence.

Evaluation:
-----------
    Percent of correctly classified junction resolutions
        (Ignore "don't know" junction resolutions in ground truth annotation)
    compare straw man, various "Nth pass" method above.
    Compare energy vs. time on various "Nth pass" method above
    Visual: show smoothed skeleton

Extensions
-------------
* allow junction breaking.
* allow creating of junctions by filling gaps.
    - (requires additional annotation code)
* imageJ plugin for ground-truthing


Miscellanous observations
---------------------------
Loop collapsing shouldn't occur if interpolated curve or lateral curves pass through block region (non-neuron).  Prefer breaking loop in this case.

When breaking loops, prefer curves that grow narrower that farther then get from the tree.  Each edge can be assigned a "direction" posterior probability based on its tendancy to grow thinner.  Could use an OU process; given initial point, compute probability of remaining.  Since OU prefers reverting to the mean (zero in this case), the forward direction should be preferred.

When breaking, prefer keeping thick branch points, rather than thin ones.

When resolving junctions, make sure "parent" curve doesn't wind up in a child configuration.  In other words, in a y junction, one curve will be closer to the tree root than the other two.  The other two cannot end up being connected, because that would imply the parent curve is a lateral branch of the child.

