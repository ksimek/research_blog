---
layout: post
title: "Foreground Curve Models as Gaussian Process Covariance Function"
description: ""
category: 
tags: []
---
{% include JB/setup %}
{% include research/tulips_da2_meta %}

Background
-------------
 This weekend, I worked out the math for two new foreground models, which differ in how 3D perturbations between views are modelled.  The first assumes a single "mean" curve, and all observations are small 3D perturbations of it.  The second assumes the unobserved curve follows Brownian motion over time.

Covariance functions as models
---------------
I realized this weekend that all of the models I've considered are achievable by using different covariance functions.

The original model is given by

<div> \[
k_1(i,j) = \sigma_s k_{\text{cubic}}(i,j) + \sigma_o  k_{\text{offset}}(i,j) + \sigma_r k_{\text{linear}}(i,j)
\] </div>

where

<div> \[
\begin{align}
k_{\text{cubic}}(i,j) &= \frac{|\tau_i - \tau_j| \min(\tau_i, \tau_j)^2}{2} + \frac{\min(\tau_i, \tau_j)^3}{3} \\
k_{\text{linear}}(i,j) &= \tau_i \tau_j  \\
k_{\text{offset}}(i,j) &= 1 \\ 
\end{align}
\] </div>

The cubic model penalizes non-zero second derivative over the length of the curve.  The offset and linear model penalize zero and first derivative initial conditions.

White noise perturbation model
------------------------------------
Both of the two new models expand on the original by modelling how the observed curve differs between views.  That is, the model for the curves are the same as before (they are cubic spline curves), but we additionally model **how they are perturbed between views**.

The first new model I call the "White Noise" perturbation model, which treats each view of the curve as arising from a white noise process that perturbs a "master curve", I.e. the unobserved mean curve.  Its covariance is:
    
<div> \[
k_{\text{white}}(i,j) = k_1(i,j) + \delta(v_i-v_j) k_{\text{w}}(i,j)
\] </div>


where \\(v_i\\) is the view that captured the \\(i\\)th point and \\(k_w\\) is

<div> \[
k_w(i,j) = \sigma_{o,w}  k_{\text{offset}}(i,j) + \sigma_{r,w} k_{\text{linear}}
\] </div>

This model adds extra covariance that is independent per-view.  This treats the perterbations from the mean curve as independent.

The perturbations themselves are assumed to be purely to the curve's initial conditions, i.e. its position and direction.

This model is motivated by the assumption that perturbations arise due to camera mis-calibrations, which result in mostly translation and small rotational changes.

Brownian motion perturbation model
------------------------------------
The second model treats perturbations as arising from Brownian motion, i.e. each curve is independent, conditioned on the previous view's curve.  The covariance function is:
    
<div> \[
k_{\text{brown}}(i,j) = k_1(i,j) + \min(\tau_i, \tau_j) k_{\text{b}}(i,j)
\] </div>


where \\(k_b\\) is

<div> \[
k_b(i,j) = \sigma_{s,b} k_{\text{cubic}}(i,j) + \sigma_{o,b}  k_{\text{offset}}(i,j) + \sigma_{r,b} k_{\text{linear}}
\] </div>


This model assumes perturbations arise by motion of the plant during imaging, like moving closer to a light source, or responding to a temperature gradient in the room.  "View index" is a surrogate for a time variable, since time between captures is roughly constant.  The use of Brownian motion means the magnitude of perturbation increases by the square root of the distance between the views (time).  \\(k_b\\) models the nature of the perturbation; we use the cubic-spline kernel which says that point-wise perturbations are strongly correlated and increase in magnitude the further they get from the base of the curve.   

This \\(k_b\\) is possibly overkill;  using the simpler \\(k_w\\) from the white-noise model might work just as well.  This simpler model implies curves drift in position and direction only, and these perturbations are correlated over time.

End stuff
----------

After some consideration, I think implementing these models in the current system will will very simple.  Training them will be harder; some more ground truthing will be needed.

Of the two new models, I suspect that the white noise model will be sufficient to get the gains in marginal likelihood we seek.  It is a much better explanation for misaligned data-points compared to the old model models all point perturbations as independent.  

The brownian motion model will give us something to compare against in evaluation.
