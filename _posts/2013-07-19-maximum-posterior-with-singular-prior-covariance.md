---
layout: post
title: "Maximum posterior with singular prior covariance"
description: ""
category: 
tags: []
---
{% include JB/setup %}
{% include research/tulips_da2_meta %}

Consider the scenerio of Bayesian inference with a linear-Gaussian prior and likelihood.

It is sometimes the case that our prior has a singular covariance matrix, indicating that our variables are embedded in a lower-dimensional hyberplane, i.e. some dimensions are redundant.  In our 3D curve triangulation application, this situation arises when  the same 3D point is observed in from multiple views.  

We can still find the maximum posterior arising from such a prior, as long as the likelihood is non-singular.   We can interpret this as multiple observations of the rendant dimensions, and if we are careful with our math, we can handle it the same way as the case with a non-singular prior.  

Given a likelihood \\( \mathcal{N}(\mu_l, \Sigma_l) \\) and prior \\( \mathcal{N}(\mu_0, \Sigma_0) \\), recall that the posterior is given by  \\( \mathcal{N(\mu_P, \Sigma_P)} \\), where

<div>\[
\begin{align}
\Sigma_P &= (\Sigma_l^{-1} + \Sigma_0^{-1})^{-1} \\
\mu_P &= (\Sigma_l^{-1} + \Sigma_0^{-1})^{-1} (\Sigma_l^{-1} \mu_l + \Sigma_0^{-1} \mu_0)
\end{align}

\]
</div>

However, if \\(\Sigma_0 \\) is singular, we must avoid inverting it when computing \\( \mu_P  \\).  An equivalent equation for \\(\mu_P\\) that satisfies this condition is:

<div> \[
\mu_P = (\Sigma_0 \Sigma_l^{-1} + I)^{-1} (\Sigma_0 \Sigma_l^{-1} \mu_l + \mu_0)
\]
</div>

<div>This should be computable as long as the likelihood precision matrix \(\Sigma_l^{-1}\) has no infinite eigenvalues.  </div>

To see an example result, see [today's Work Log]({{site.baseurl}}/2013/07/19/work-log/) entry.

Implementation Notes
---------------
I tried implementing a version of this that uses Cholesky decomposition and backsubstitution instead of generic matrix inversion.  I needed a symmetric matrix, so I modified the equation for \\\(\mu_P\\):
            
<div> \[
\mu_P = \Sigma_0 (\Sigma_0 \Sigma_l^{-1} \Sigma_0 + \Sigma_0)^{-1} (\Sigma_0 \Sigma_l^{-1} \mu_l + \mu_0)
\]
</div>

This was not noticibly faster than general matrix inversion, because it involves two additional large matrix multiplications.  

Surprisingly, I *was* able to get a significant speedup (~7x) be using backsubstitution (Matlab's '\' operator) *without* Cholesky decomposition.  I always assumed that the lower-triangular form was what made backsubstitution so fast, but it is apparently also fast with dense matrices.  So we can avoid the extra expensive dens-matrix multiplications, and also avoid expensive matrix inversion.
