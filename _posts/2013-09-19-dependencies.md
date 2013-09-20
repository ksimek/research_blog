---
layout: post
title: "Summary of Dependency relationships"
description: ""
category: reference
tags: []
meta: 
    "SVN Revision": 15229
---
{% include JB/setup %}
{% include research/tulips_da3_meta %}

The dependency between individual variables is a bit complicated, but if we group variables together, the relationship between the groups is simple.  We group parameters into "self" parameters and "inherited" parameters.

Self parameters are immune to changes to parents or children.
Inherited parameters are affected by any changes to parent.  

* SELF PARAMETERS
    * *reconstruction fields*: assoc, corr, ll_*, 
    * start index
    * prior_K
* INHERITED PARAMETERS
    * branch distance, branch_index
    * *branch distribution*:  mu_b, mu_Sigma, branch_mu, branch_Sigma
    * Marginal likelihood.

This can be summarized as follows:

> Any time a curve is changed in any way, we must recursively update all inherited parameters.  

This "if anything changes, update everything" rule is a bit broad, and we can use a finer-grained definition to update fewer inherited fields, but in general, we only avoid updating fields that are inexpensive to update anyway.  For heavy-wieght fields (e.g. branch distribution and ML), they are affected by everything, so we're forced to update them after every change.  Thus, the simpler rule is only nominally less efficeint, and much easier to implement and understand.

