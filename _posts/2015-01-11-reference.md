---
layout: post
title: "Trained prior parameters"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}

Training only local prior w/ noise_variance fixed at 1.0:
  
            noise_variance: 1
         geodesic_variance: 15.9174
            geodesic_scale: 0.0019
    branch_linear_variance: 0.0485
     branch_const_variance: 3.7438
           linear_variance: 0.0348
            const_variance: 685.7670

Training full model (local prior and epipolar prior) w/ noise variance fixed at 1.0

         epipolar_variance: 4.5465
        euclidean_variance: 0.0422
           euclidean_scale: 4.2001e-07
            noise_variance: 1
         geodesic_variance: 233.9050
            geodesic_scale: 4.3327e-04
    branch_linear_variance: 0.1079
     branch_const_variance: 7.0217
           linear_variance: 0.1016
            const_variance: 2.4123e+03

  Notice significantly larger geodesic variance, and much longer scale length (48 vs 22 pixels).  All other variances increased too.  This is probably because we've treated the two priors as independent, but they aren't, so multiplying them results in too little overall variance.
