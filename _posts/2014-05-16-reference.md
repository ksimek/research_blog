---
layout: post
title: "FIRE - Self-report clustering results."
description: ""
category: 'Reference'
tags: []
meta: 
---
{% include JB/setup %}

Results of initial clustering of self-report data.  (I showed these a few weeks ago, but never recorded them here).

**Data**: Five survey values, recorded once per each of nine visits, for a total of 45 dimensions per cluster.  Missed visits are treated as missing data and ignored during inference.

**Model, Inference**: Multivariate gaussians with diagonal covariance were fit to each cluster.  Cluster memberships and cluster parameters were fit with EM, with 100 different initializations to avoid local minima.  Number of clusters was varied between 2 and 50, and the optimal choice of three clusters was determined using BIC.

Results
-------

**Means**  

![]({{site.baseurl}}/img/2014-05-16-cluster_means.png)

**Standard Deviations**  

![]({{site.baseurl}}/img/2014-05-16-cluster_std_devs.png)

Disucssion
-----
PSS is in the 0.9-1.0 range for all clusters.

Note that FACT data has high standard deviation, making its curves harder to interpret.

Also note that unlike other variables, high FACT scores correspond to *negative* outcomes (e.g. high pain, high nausea, etc)

Third cluster is the "always good" cluster.

Second cluster is the "high emotional acceptance cluster".  Notable that DAS and SRI start low, but increase over time.  This suggests a hyptothesis that high emotional acceptance can result in improved outcomes over time.

First cluster is the "low emotional acceptance cluster".  SRI and DAS start low and never improve.
