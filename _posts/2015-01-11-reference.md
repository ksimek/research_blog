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

40-degree model
----------
Below are results for training a deformation model for a 40 degree rotation.

Training only local prior w/ noise_variance fixed at 1.0:
  
            noise_variance: 1
         geodesic_variance: 15.9174
            geodesic_scale: 0.0019
    branch_linear_variance: 0.0485
     branch_const_variance: 3.7438
           linear_variance: 0.0348
            const_variance: 685.7670

Training full model (local prior and epipolar prior) w/ noise variance fixed at 1.0

    log-likelihood = -2368.62

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

By comparison, below is a nearby local minimum, obtained by training all 9 parameters from scratch.

  log-likelihood:  -2370.05

           epipolar_variance: 4.6435
          euclidean_variance: 3.1113e-35
             euclidean_scale: 7.4415e+152
              noise_variance: 1
           geodesic_variance: 283.5387
              geodesic_scale: 3.9692e-04
      branch_linear_variance: 0.1236
       branch_const_variance: 6.5436
             linear_variance: 0.0746
              const_variance: 5.4990e-109

This model moves all epipolar prior variance into the iid epipolar_variance variables. Also the local prior's offset variance has been moved into the deformation variance, geodesic_variance, while shortening the scale.

10-degree model
----------
Below are results for training a deformation model for a 10 degree rotation.

         epipolar_variance: 4.5465
        euclidean_variance: 0.0422
           euclidean_scale: 4.2001e-07
            noise_variance: 1
         geodesic_variance: 2.0824
            geodesic_scale: 5.9410e-04
    branch_linear_variance: 0.0064
     branch_const_variance: 0.6186
           linear_variance: 0
            const_variance: 1.1533e-21

            ll: -2087.07 

I suspect overfitting here.  Fitting works best when scaling prior variance by 36.