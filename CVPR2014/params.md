---
layout: page
title: "CVPR 2014 System Parameters"
description: ""
---
{% include JB/setup %}

Official page for Matlab system parameters, CVPR 2014 (c. October 2014).

Any changes to the matlab parameters need to be updated here, with a corresponding update to the changelog.

`params`
===============


    params = 

             smoothing_variance_2d: 0.0100
                 noise_variance_2d: 0.3480
                  position_mean_2d: [265 198.5000]
              position_variance_2d: 15609
                  rate_variance_2d: 2.2500
                smoothing_variance: 0.0035
                    noise_variance: 0.3480
                     position_mean: [3x1 double]
                 position_variance: 1.2987e+03
                     rate_variance: 0.2652
                       index_delta: 2
                    index_delta_2d: 2
        perturb_smoothing_variance: 2.7745e-06
             perturb_rate_variance: 4.3973e-04
         perturb_position_variance: 0.6356
                     perturb_scale: 2.4900
             markov_blanket_radius: 2000
                        model_type: 3
                         num_views: 9
                     ml_block_size: 1000
                   ml_markov_order: 1000
                      ll2_spacing: 2
                       tube_radius: 1



Changelog
============

Most recent items first.

2013-10-26
------------

Initial import.  

Most prior parameters came from training on [August 16, 2013]({{site.baseurl}}/2013/08/16/work-log/), with the exception of `position_variance`, which was modified when we added the position_mean parameter.  The old `position_variance` was derived from an assumed mean of (0,0,0); after learning a mean, the variance naturally dropped.  The perturb parameters are actually slightly different from the August 16 results; not sure how the deviation aros, but they're still in the ballpark.  Retrain soon.

`index_delta` and `index_delta_2d` were hand-set heuristically.

`markov_blanket_radius` is basically "infinity"; all parent points are used when computing branch point.  This is a good candidate for tuning; IIRC, I set it this high during testing and never changed it back.  Lowering should improve `attach()` runtimes.

`model_type` is OU-perturb-model (i.e. 3).

`ml_block_size` and `ml_markov_order` were hand-set heuristically to be a good balance between speed and approximation accuracy (IIRC).  Possibly some room for improvement here.

`ll2_spacing` is a new parameter, the sampling period when evaluating the "second" likelihood, i.e. the pixel likelihood.  Arbitrary, untested.

`tube_radius` also pertains to the pixel likelihood.  Its the radius of the tubes rendered by opengl.  Hand-picked, relatively untested (but qualitatively reasonable.).
