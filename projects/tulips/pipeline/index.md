---
layout: page
title: "TULIPS data pipeline"
description: ""
---
{% include JB/setup %}

The Track processing pipeline is split into 7 stages.  This allows us to avoid recomputing everything when a single field changes; if a "stage 3 field" changes, only stages 4 through 7 need to be re-run.  

This information was originally discussed [in this blog post]({{site.baseurl}}/2013/09/26/reference).


Stage 0
----------

Track is ready to be processed.   At this stage, the only valid fields are those set by the user, namely:
    
    Track.assoc
    Track.reversed

To construct a stage-zero track:
    
    init_track

Stage 1
-------------

A stage 1 track has passed the correspondence stage.  

Three functions can prepare a track for stage 1:
    
    init_trivial_track
    merge_correspondence
    build_full_correspondence

Associated fields are:
    
    corr
    means
    precisions
    cov_error

Stage 2:
-----------

In stage 2, raw curve likelihood fields have been constructed, and are ready for post-processing.

The transition from stage 1 to stage 2 is relatively expensive, as every point requires backprojection, a pass of dynamic time warping, and a few iterations newton's method to find the index set.  

Associated fields
    
    ll_means
    ll_precisions
    ll_distances
    sm_lambda
    curve_sm
    curve_sm_t

Associated functions

    corr_to_likelihood

Stage 3
----------

Stage three consists of inexpensive post-processing of the likelihood fields.  Curve reversal is handled here; flattening and sorting is lumped into this stage too.  Reversing and re-evaluating curves is a common use-case, and this can be done efficiently by keeping stage 3 separate from stage 2.

This is also where the likelihood covariance blocks are computed; since this is somewhat time-costly, it may be moved into stage 2 in the future.


Associated fields

    ll_views_flat
    ll_means_flat
    ll_precisions_flat
    ll_distances_flat
    ll_S

Associated functions
    
    flatten_sort_and_reverse

Stage 4: Attachment
----------------------

Stage 4 is where topology is handled.  The predictive distribution of the branch point is computed and stored for efficient computation of the marginal likelihood later.  

Stage 4 needs to be applied recursively to all children.  

Associated fields

    parent_ci
    start_index
    prior_K
    branch_distance
    mu_b
    Sigma_b
    branch_mu
    branch_K

Associated functions

    attach
    detach
    att_set_branch_distance (called from attach)
    att_set_start_index (called from attach/detach)

Stage 5: Index refinement
---------

In stage 5, the Tracks are ready for index refinement, in which Tracks.ll_distances_flat is optimized wrt the marginal likelihood.  This allows us to recover from mis-matching at stage 2, and most notably, mitigates the "stretching and twisting" phenomenon, discussed briefly [here](http://vision.sista.arizona.edu/ksimek/research/2013/11/11/work-log/).

This is an expensive iterative minimization operation, requiring O(n^3) each iteration. 


Associated_fields 
    
    ll_distances_flat

Associated functions 

    optimize_ml_wrt_indices


Stage 6: Marginal likelihood
---------

Marginal likelihood is ready to be computed for this track, conditioned on its parent.

This stage is still in flux; it is unclear which likelihood terms will be included in the final project.  In the current implementation, ml field is not set, and curve_ml simply returns the ml value.  

Associated fields

    ml

Associated functions
    
    curve_ml
    curve_tree_ml_5 (speculative)

Stage 7: complete
---------

All processing is finished.
