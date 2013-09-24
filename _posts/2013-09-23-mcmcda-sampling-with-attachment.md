---
layout: post
title: "MCMCDA Sampling with Attachment"
description: ""
category: 'Strategy'
tags: []
meta: 
#    "SVN Revision": 15229
---
{% include JB/setup %}

The old MCMCDA gibbs sampler runs into trouble now that we allow attachment.  

Previously, for any observation, we would compute the ML of grouping it with each candidate, and select a candidate from those weights.  

The problem now is that regrouping an observation sometimes causes it's old group to vanish, and the question of what to do with the group's children is unanswered.  The same problem occurs if a regrouping makes a curve shorter, and children were attached to the now-missing structure.  

Metropolis Hastings
---------------------------

Things become much easier if we move away from Gibbs sampling.  Gibbs was nice for a proof of concept, because we never failed to pick embarrassingly good candidates, and we almost always moved toward a better result with each step.  However, it was very expensive, and now we have a question of how to compute the ML of a candidate whose attachment property is unknown.

So, we'll move to Metropolis Hastings.  We resolve the attachment issue by using a simple rule:  every time a track's association changes, we re-sample its the attachment and the attachment of its former children.

Sampling Associations.
-----------------------

When sampling associations, we'll use two types of moves:

* **swap**: re-assign a single observation
* **split/merge** re-assign a group of observations

The swap move will be similar to the existing Gibbs move, except we'll choose from candidates uniformly at random.  Split/merge proposals will be naive; we'll incorporate an association prior to counter the exploding number of split moves.

Re-sampling attachment
--------------------

After sampling a new association, we'll re-sample attachment.  For this, we'll introduce a new function `sample_attachment`, which will be responsible for constructing a list of reasonable candidates and attachment parameters (Start point and branch position), and selecting one at random (probably based on geometry, i.e. not uniform).  It returns the sampled attachment, along with the proposal probability.  It can optionally receive a `hint` parameter, which is a list of attachment candidates, along with a guess as to the attachment parameters.  The candidate of "no attachment" should always be an option.

We'll also need a function that returns the probabiliy of selecting a specific attachment, according to `sample_attachment`, for computing the reverse move.

Topology moves
-------------

In addition to association moves, we'll also have topology moves.  This will consist of simply calling `sample_attachment` without a sampling an association beforehand.
