---
layout: post
title: "Rethinking covariance functions"
description: ""
category: 
tags: []
---
{% include JB/setup %}


Noticed a problem with the cubic spline perturbation model.  As the view number increases, the variance marginal prior of the curve in that view approaches infinity.  This means that the "smoothness" prior is ignored more and more in later views.

Squared Exponential perturbation model
----------------------------

A better model would have the same marginal prior for all views, but with correlation between nearby views.  This allows curves to revert to the prior as temporally correlated evidence becomes less informative.  I believe the squared exponential covariance function has this property.  Instead of adding the sq-exp covariance to the existing covariance function, we should multiply it, so self-covariance is unchanged, but pairwise correlation is non-zero.   

An added benefit of this is that it only has one tunable parameter.

It should be easy to incorporate into our test-bed, along with the other two newly proposed foreground models.

Ornstein Uhlenbeck perturbation model
-----------------------------------
Digging deeper into Williams and Rasmussen, I found precisely the GP I was looking for a few days ago:  the Ornstein–Uhlenbeck (OU) process.  This   process describes brownian motion under the influence of a regularizing force that pulls toward the mean.

In other words, I can model correlation between views without affecting the marginal prior of the curve any particular view.  This is also accomplished by the squared-exponential model, but the OU process is probably more realistic, because the plant's motion looks non-smooth.


Modelling the mean or not?
----------------------------
I'm struggling with whether or not to explicitly model a "mean" curve with the SE and the OU processes.  

If I did model the mean, each curve's covariance function would be the sum of a standard covariance plus a perturbation covariance.  The standard covariance models the "mean" curve, and it would be the same for all views (100% correlated).  The perturbation covariance would be partially correlated between the views, using the SE or the OU process.  The bayes net has the following structure:

            O   <-- mean curve
         / /\ \
       /  /  \  \
     /   |    |   \
    O--->O--->O--->O   <- per-view curves
    |    |    |    |
    O    O    O    O   <- observations

The alternative is to model the per-view curves directly:

    O--->O--->O--->O   <- per-view curves
    |    |    |    |
    O    O    O    O   <- observations

Under this model, each view's curve has a cubic-spline marginal distribution, and the SE or UO process controls the correlation between them.

What isn't clear is whether the perturbations in the latter model will be independent between points.  We need to model within-view perturbations as correlated, otherwise the marginal likelihood will drop too low.  There is no explicit description of how perturbations of adjacent points correlate.  

What follows is me thinking out-loud...
---------------------------------------

Intuitively, points nearby in curve-space (have similar \\(\tau\\)'s) can never be more correlated than they are when they appear in the same view.  Separating them in time (view) will decreases their correlation, until finally, there is no correlation; the only remaining correlation is between points in the same view.  The SE kernel modulates that correlation.  The SE kernel doesn't explicitly model correlation between perturbations, but this doesn't mean the correlation doesn't exist -- it is implicit in the original kernel.

There is an analogy here with the classic krigging example.  In there models, the squared exponential over a 2D landscape (i.e. joint function over \\(\mathbb{R}\\)^2 space) is equal to the product of 1D squared exponentials (i.e. two functions over \\(\mathbb{R}\\)^1 space).  In other words, the 2D kernel is constructed by the product of 1D kernels.  There is no worry that the delta between nearby "slices" of the surface are uncorrelated, because the marginal covariance within that slice will enforce that smoothness.  

In our case, we also have a product of 1D covariance functions constructing a 2D covariance function.  The difference is that one of the kernels (the curve-space kernel) is a cubic-spline process, while the other (the time-dimension kernel) is squared exponential (or Ornstein-Uhlenbeck).  Despite this difference, my intuition is that the conclusions are the same - the deltas will be smooth (i.e. correlated), because they will be the difference between two smooth curves.  

Considering the marginals in both directions further illustrates why this works.  Obviously, a slice in the curve-direction will always look curve-like, since the marginals are all the same cubic-covariance GP prior.  In the time-direction, a single point will follow a GP or OU process, with initial conditions dictated by the first curve.  

**...BUT...**

...in the absence of data, each individual point will drift over time to the prior mean, I.e. **zero**.  In other words, the 3D curve observed in view infinity gains no information from curve observed at time zero.

This is **not** realistic.  In reality, these points shouldn't drift far from some "sensible" center curve, implying that a mean curve exists.  

The time-slice of any particular point *should* look like either a OU or SE process, but the mean needs to be explicit.  This implies an additive model, with distinct models for the unobserved "mean curve" and the deviations from it, which are summed to get the 3D curve seen in each view.

Modeling perturbation
-------------------------
So if we must model perturbation, how should we model it?

One thing is clear: the marginal prior for the curve in any view **must** still be a cubic-spline process.

This implies that the perturbation must be a cubic-spline process, too.

However, the variances for each component (offset, linear, and cubic) are likely to be different for the perturbation model, compared to the mean-curve model.  Most importantly, the magnitude of the offset variance must be large in the mean-curve model but will be _much_ lower (relative to linear and cubic variance) in the perturbation model.  

I was hoping to avoid adding four extra parameters to our model (perturbation offset, linear and cubic variance, plus perturbation scale-length).  The mean-free model only adds one parameter - scale-length.  I guess this is the price we pay for a better model -- and for higher marginal likelihoods.  Ideally, the occam's razor quality of the marginal likelihood will allow us to avoid overfitting this many parameters (7 total).  Any parameters that are superfluous should become near-zero during training.

...I hope.  


