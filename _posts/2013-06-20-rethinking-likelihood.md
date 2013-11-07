---
layout: post
title: "Rethinking Likelihood"
description: ""
category: "Work Log"
tags: []
---
{% include JB/setup %}
{% include research/tulips_da2_meta %}

Testing and debugging `clean_correspodnence2.m` has revealed some significant problems with the current approach to constructing the likelihood function.

** 5%-10% of fragements have correspondences that are nonsensical. **

I hypothesize that this is due to bad correspondences early on, when there is little evidence to drive a good correspodnence.  These bad correspodnences are propagated as new curves are added that could suggest a better correspodnence.

** Large lateral gaps in triangulation result in large axial gaps in posterior curve.  **

The problem is that the index set is computed from the triangulation.  The current fix for this -- smooth, re-index, repeat -- is very limited in the severity it can overcome.  In practice, most gaps are only partially reduced.

Rethinking "Correspondence to Likelihood"
-------------------------------------------

Corresondence is good for constructing a decent-quality 3d curve, but isn't good for computing fine-grained pointwise likelihood, due to sporradic terrible correspondences and gaps.

Instead of continuously Band-Aiding these issues that keep arising, its time to re-think how the likelhood is constructed.  

** 1. the mean of 3d gaussians should project to the 2D position of the corresponding data point **

** 2. the depth should be based on the corresponding position in the unobserved curve **

Two issues here.  First, how to localize the unobserved curve without having the likelihood already (chicken and egg).  Second, how to identify the corresponding point of the unobserved curve?  

In the old method, the answer to both was "use the correspondence matrix." 

In the new method, we still use the correspondence matrix to triangulate, but we smooth the result using the prior and then throw away correspondence information.  



Killing the correspondence grid
--------------------------------

The corresponence matrix artificially forces points from different views to correspond to the same point.  This is out of necessity -- we need correspondence to achieve triangulation.  But we don't need to adhere to this to compute the likelhood.  Indeed, observed points may fall anywhere in the continuous index set, not into a discrete set of predefined cells.  

* Observations can correspond to any index in \\([0 t_{end}]\\).
* Unobserved curve is modelled at a uniform grid.
* Previously, the dimensionality of the unobserved curve grew with the number of observations. Now it grows with the range of the index set (i.e. the length of the curve).`


Random thoughts
------------------

* evaluate marginal likelihood directly?  then add extra normalization from triangulation (jacobian?)
    * evaluate linearly using markov conditional probabilities
    * extend to poly model
        * grid-structured Bayes net 
        * topological sort for evaluation
        * use scope variables to manage dependencies generally





