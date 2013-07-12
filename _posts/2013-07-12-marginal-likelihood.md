---
layout: post
title: "Direct Evaluation of the Marginal Likelihood"
description: ""
category: 
tags: []
---
{% include JB/setup %}
{% include research/tulips_da2_meta %}

Previously, we've always used hacks to evaluate the marginal likelihood, because evaluating it directly was apparently impossible because of an infinite normalization constant.  I've discovered that this isn't actually true; the infinite normalization constant arose due to our approximation of the likelihood.  The trick in correctly computing the ML is to replace the usual normalization constant with a corrected one.  

Our old method required knowledge of the maximum posterior solution, which was costly to compute.  The new approach is straightforward to describe, more accurate than our previous method, and can be evaluated in linear time by exploiting its Markovian structure.  

Below is a rough-draft writeup of my derivation of the marginal likelihood function.


Direct Evaluation of the Marginal likelihood
------------------------------------------------

The 3D marginal likelihood function arises as the sum of a 3D curve process and a 3D perturbation process.  Both are gaussian (the second is approximate), this the result is a Gaussian function, the convolution of two Gaussians.  However, the perturbation process has infinite variance in the direction of backprojection, which arises from the fact that perturbation actually occurs in 2D, we are just backprojecting it to 3D for tractibility.  In other words, the ML isn't a distribution in 3D, it's a distribution in 2D, and we need to determine the appropriate normalization constant for the 3D function to it generates 2D ML densities.

The likelihood function is given by

<div>\[
\begin{align}
p(y | x) &= \prod p(y_i | x_i) \\
         &= \prod \mathcal{N}(y_i; \rho_I(x_i), \sigma_n^2 I) \\
         &\approx \prod \frac{1}{\sqrt{2 \pi \sigma^2}^2} \mathcal{G}(Y_i; x_i, S_i^{-1}) \\
         &= \prod \frac{1}{\sqrt{2 \pi \sigma^2}^2} \exp\{(Y_i - x_i)^\top S_i (Y_i - x_i)\} \\
         &= \frac{1}{\sqrt{2 \pi \sigma^2}^{2n}} \exp\{(Y - x)^\top S (Y - x)\} \\
         &= \frac{1}{Z_l} \exp\{(Y - x)^\top S (Y - x)\}
\end{align}
\]</div>

Where 
    
* \\(\rho_i(x)\\) is the projection of x into the I-th view, 
* \\(Y_i\\) is the estimated backprojected position of observation \\(y_i\\),  
* \\(S_i\\) is the curvature of the 3d likelihood function w.r.t. \\(x_i\\) evaluated at $Y_i$, 
* \\(Y\\), \\(S\\) and \\(x\\) are the concatenation of \\(Y_i\\), and \\(x\\)
* \\(S\\) is the block-diagonal matrix of \\(S_i\\)'s
* \\(\mathcal{G}\\) is a Gaussian function (an unnormalized normal distribution).
* \\(Z_l\\) is a normalization constant.

We have transformed the likelihood into a log-linear function of x, by rewriting the PDF in terms of only 3D entities.  Note that \\(S_i\\) has zero curvature in the backprojection direction, resulting in infinite variance in the Gaussian function.   Also note that the normalization constant isn't the standard one for a 3D gaussian distribution, because this isn't a distribution over x.  The normalization constant is chosen so the approximate likelihood in 3D agrees with the exact 2D likelihood when perturbation is zero (i.e. when \\(Y_i\\) lies anywhere on the backprojection line).
    
This approximation ignores the nonlinearity of projection; the likelihood function as a function of \\(x_i\\) would actually look like a cone whose axis-perpendicular slices are Gaussians, whereas our function is cylinder-shaped.  In practice, the approximation error has minimal effect on the marginal likelihood computation, assuming $Y_i$ is a good estimate of the posterior depth, and the posterior is reasonably peaked.  (A graphic to illustrate would be good here).

The prior is given by

<div>\[
\begin{align}
p(x) &= \mathcal{N}(x; \mathbf{0}, K) \\
     &= \frac{1}{Z_p} \exp\{x^\top K^{-1} x\}
     \end{align}
\]</div>

where \\(K\\) is the covariance matrix arising from the Gaussian process kernel, and Z_p is the standard Gaussian normalization constant. 

The marginal likelihood is defined as

<div>\[
\begin{align}
p(y) &= \int p(y|x) p(x) dx \\
     &= \int \left ( \frac{1}{Z_l} \exp\{(Y - x)^\top S (Y - x)\} \right ) \left ( \frac{1}{Z} \exp\{x^\top K^{-1} x\} \right ) \\
     &= \frac{1}{Z_l Z_p}\int   \exp\{(Y - x)^\top S (Y - x)\}   \exp\{x^\top K^{-1} x\} \\
     \end{align}
\]</div>

The expression within the integral is the convolution of two unnormalized zero-mean Gaussians, so the integral is a zero-mean Gaussian whose covariance is the sum of the inputs' covariances.  If the input Gaussians **were** properly normalized, the normalization constant would be \\(1/Z\\);  since they are not, the normalization constant is \\((Z_1 Z_2 / Z)\\), where \\(1/Z_1\\) and \\(1/Z_2\\) are the would-be normalization constants for the first and second Gaussian, respectively.  Note that the second Gaussian's normalization constant is \\(1/Z_p\\), so this results in the cancellation we see below

<div>\[
\begin{align}
p(y) &= \frac{1}{Z_l Z_p} \int   \exp\{(Y - x)^\top S (Y - x)\}   \exp\{x^\top K^{-1} x\} \\
     &= \frac{1}{Z_l Z_p} \left ( \frac{Z_{l,3d} Z_p}{Z} \exp\{x^\top (S^{-1} + K)^{-1} x \} \right ) \\
     &= \frac{Z_{l,3d} }{Z_l}\frac{1}{Z} \exp\{x^\top (S^{-1} + K)^{-1} x \}
     \end{align}
\]</div>

<div>
    Where \( Z_{l,3d} \) is the would-be 3D normalization constant for our likelihood Gaussian.  Since \(S\) is rank-deficient, the normalization constants based on \(S^{-1}\) will be infinite (i.e. \(Z_{l,3d}\) and \(Z\)).  However, the terms involving determinants of \(S^{-1}\) should cancel in the ratio, resulting in a gaussian with infinite variance, but non-infinite normalization constant. **(Need to show this mathematically next time)** 
    </div>
