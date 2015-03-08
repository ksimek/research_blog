---
layout: post
title: "Deriving likelihood of camera parameters"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}

It occurred to me that naively doing camera fitting causes strong correlations between camera pose and reconstruction position.  Originally, I planned on alternating between optimizing the conditional curve density \\(p(x\_i | y\_i, c\_i)\\)  and the conditional camera density, \\(p(c\_i | y\_i, x\_i)\\).  The problem here is that the optimal curve \\(x\_i\\) for the current camera will be very close to the evidence \\(y_i\\), so optimizing the camera will only move the curve slightly.  We get into a situation where we move the camera slightly, which allows us to move the curve slightly, which allows us to move the curve slightly, etc. etc.  This is analogous to the problem in Gibbs sampling with strongly correlated variables, and like there, the solution is to integrate out one of the correlated variables.

We should be optimizing \\(p(c\_i | Y)\\) instead of \\( p(c\_i | x\_i, Y)\\).  For now, we'll assume the prior over \\(c\_i\\) is flat, so this reduces to optimizing the likelihood function \\(p(Y | c\_i) \\).  Let \\(Y\_- = y\_{1:i-1}\\) and let \\(Y\_+ = y\_{i+1:n}\\)  

<div>
\[
  \begin{align}
    p(Y | c_i) &= \int p(y_i | x_i, c_i) p(x_i | x_{i-1}, x_{i+1}) p(Y_- | x_{i-1}) p(Y_+ | x_{i+1}) p(x_{i-1}, x_{i+1}) dx_i dx_{i-1} dx_{i+1} \\
    &\propto \int p(y_i | x_i, c_i) p(x_i | x_{i-1}, x_{i+1}) p(x_{i-1}, x_{i+1} | Y_-, Y_+) dx_i dx_{i-1} dx_{i+1} \\
    &\approx\int p(y_i | x_i, c_i) p(x_i | x_{i-1}, x_{i+1}) p(x_{i-1}, x_{i+1}| Y)  dx_i dx_{i-1} dx_{i+1} \\
  \end{align}
\]
</div>

Below are the definitions of the terms above.

<div>
\[
\begin{align}
    p(x_{i-1}, x_{i+1} | Y) &= \mathcal{N}(\mu_*, \Sigma_*) \\
    p(x_i | x_{i-1}, x_{i+1}) &= \mathcal{N}(\mu_i, \Sigma_i) \\
    p(y_i | x_i, c_i) &= \mathcal{N}(\mu_y, \Sigma_y) \\
    \mu_i &= \mu_0 + A x_\pm \\
    x_\pm &= \left ( \begin{array}{c} x_{i-1} \\ x_{i+1}\end{array} \right ) \\
    A &= K_* K_{(i-1)(i+1)}^{-1}  \\
    \Sigma_i &= K_i - A * K_*^\top \\
    \mu_y &= d + J x_i \\
    d &= \pi_c(\mu_i) - J \mu_i \\
\end{align}
\]
</div>

Here, \\(\mu_0\\) is the 3D prior mean, \\(\pi\_c(X)\\) is the projection of 3D point \\(X\\),  \\(J\_c\\) is the Jacobian of \\(\pi\_c\\) centered at \\(\mu\_i\\), \\(\Sigma\_\*\\) is the posterior covariance of \\((x\_{i-1}, x\_{i+1})\\), \\(\Sigma\_y\\) is the likelihood covariance, and \\(K\_\*\\) is the prior cross covariance between \\(x\_i\\) and \\((x\_{i-1}, x\_{i+1})\\).

The integral above is a convolution that represents the sum of random variables.  We represent this sum below, where \\(\epsilon_M \sim \mathcal{N}(0, M) \\).

<div>
\[
  \begin{align}
    Y | c_i &= \mu_y + \epsilon_y \\
            &= d + J x_i + \epsilon_y \\
            &= (\pi_c(\mu_i) - J \mu_i) + J (\mu_i + \epsilon_i ) + \epsilon_y \\
            &= \pi_c(\mu_i) + J\epsilon_i + \epsilon_y \\
            &= \mathcal{N} \left (\pi_c(\mu_i), J \Sigma_i J^\top + \Sigma_y \right ) \\
  \end{align}
\]
</div>

Both the covariance and prior depend on the camera (because the camera determines \\(\Sigma\_y\\)), but if we assume the covariance is nearly isotropic, maximizing the expression above is equivalent to minimizing the norm of the residuals, \\(\| Y - \pi_c(\mu_i) \|\\).

Recall that we never explicitly have an expression for the data Gaussian, so Y isn't known.  We could derive this from the posterior and the prior, but a simple approximation is to just use the posterior mean, under the weak assumption that the likelihood is much more peaked than the prior.  The optimization procedure is then:

1. Find the maximum posterior of the \\(x\_{i+1}\\), \\(x_i\\) and \\(x\_{i-1}\\) (from Kalman smoother step).
2. Predict the current curve \\(x\_i\\), given the only the adjacent curves.
3. Find the camera that minimizes the residual between the maximum posterior and the predicted curve using nonlinear least squares (derived in yesterday's post).

In practice, isotropism isn't necessarily a good assumption,  so we can transform the residuals by the square-root inverse covariance before evaluating the error.  The square root and inverse operations will get expensive if performed at each iteration, so we can either only update it every Nth iteration, but my intuitions says the isotropic assumption should be good enough.  It would be nice to have a better argument for this.
