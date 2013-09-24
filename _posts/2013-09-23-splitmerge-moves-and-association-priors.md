---
layout: post
title: "Split/Merge moves and Association Priors"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 15229
---
{% include JB/setup %}

Thinking again about split/merge moves, and the problem of the exploding number of split moves as the nubmer of observations increases.

Part of the problem is the fact that we're treating all associations as equal under the prior.  This has the side-effect that the prior strongly prefers more curves in a model as opposed to fewer.  Consider a scenario with N observations, and M curves.  There are M^N number of ways to assign these observations to M curves.  Compare this with a model with one curve -- there's only one possible assigment.  Since all assignments are equal under the prior, the model with M curves is more favored by the prior by a factor of M^N.   

For this reason, I propose that a more sensible prior is one that is uniform over the number of curves in the scene.  Then, given the number of curves, the prior over associations is uniform.  In other words, given an association, it's prior should be 1/M^N, where M is the number of curves represented in the association.

When running a split move, the number of ways to split is 2^K, where K is the number of observations associated with the original curve.  If chosen uniformly, the Metropolis-Hastings proposal probability is 2^K.  This should cancel nicely with the prior term in the MH acceptance ratio.  

