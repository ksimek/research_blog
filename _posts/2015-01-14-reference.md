---
layout: post
title: "Prior, visualized"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}

Input tree.  (Mean of the local prior)

![]({{site.baseurl}}/img/2015-01-14-input_tree.png)
  
Training tree.

![]({{site.baseurl}}/img/2015-01-14-training_tree.png)

Sample from the locality prior only:

![]({{site.baseurl}}/img/2015-01-14-local_prior_sample.png)

![]({{site.baseurl}}/img/2015-01-14-local_sample_2.png)

![]({{site.baseurl}}/img/2015-01-11-smooth_sampled_tree.png)

Samples from full prior (including epipolar constraints)

![]({{site.baseurl}}/img/2015-01-12-full_prior_samples.png)

![]({{site.baseurl}}/img/2015-01-14-full_prior_samples.png)

Notice how all corresponding points lie on the same epipolar line.

The plot of eigenvalues of the prior covariance matrix suggest a very low-dimensional embedding:
  
![]({{site.baseurl}}/img/2015-01-14-full_prior_eigs.png)

Plotting log-sqrt eigenvalues compresses the dynamic range, making it easier to read:
  
![]({{site.baseurl}}/img/2015-01-14-log_sqrt_prior_eigs.png)
