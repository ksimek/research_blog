---
layout: post
title: "Track stages"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 15229
---
{% include JB/setup %}

A track's "stage" is a description of where it is in the processing pipeline. 

Each stage has one or more track fields associated with it.  No stage may modify fields from the previous stages.

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

Stage 5
---------

Marginal likelihood has been computed for this track, conditioned on its parent.

Note: in the current implementation, ml field is not set, and curve_ml simply returns the ml value.  This will change in the near future to comply with the multi-stage model described in this post.

Associated fields

    ml

Associated function
    
    curve_ml

Running all stages
------------------

In many cases, it's not necessary to construct tracks from scratch.   Reversing a curve only requires re-running stages 3 through 5.  Attaching or detaching a curve only requires re-running Stages 4 and 5.

However, some cases require a full end-to-end running of stages 1 through 5.  The function that does this is:
    
    build_track

This function is also a nice reference of how to run each stage.
