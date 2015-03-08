---
layout: post
title: "Deriving likelihood of curve parameters"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}

It occurred to me that naively doing camera fitting results in strong correlations between camera pose and reconstruction position.  Originally, I planned on alternating between optimizing the conditional curve density \\(p(x\_i | y\_i, c\_i)\\)  and the conditional camera density, \\(p(c\_i | y\_i, x\_i)\\).  The problem here is that the optimal curve \\(x\_i\\) for the current camera will be very close to the evidence \\(y_i\\), so optimizing the camera only needs to move the curve slightly.  We get into a situation where we move the camera slightly, which allows us to move the curve slightly, which allows us to move the curve slightly, etc. etc.  This is analogous to the problem in Gibbs sampling with strongly correlated variables, and like there, the solution is to integrate out one of the correlated variables.

We should be optimizing \\(p(c\_i | Y)\\) instead of \\( p(c\_i | x\_i, Y)\\).  For now, we'll assume the prior over \\(c\_i\\) is flat, so this reduces to optimizing the likelihood function \\(p(Y | c\_i) \\).  Let \\(Y_- = y_{1:i-1}\\) and let \\(Y_+ = y_{i+1:n}\\)  

<div>
\[
  \begin{align}
    p(Y | c_i) &= \int p(y_i | x_i, c_i) p(x_i | x_{i-1} x_{i+1}) p(Y_- | x_{i-1}) p(x_{i-1}) p(Y_+ | x_{i+1}) p(x_{i+1}) dx_i dx_{i-1} dx_{i+1} \\
    &\propto \int p(y_i | x_i, c_i) p(x_i | x_{i-1} x_{i+1}) p(x_{i-1} | Y_-) p(x_{i+1} | Y_+) dx_i dx_{i-1} dx_{i+1} \\
  \end{align}
\]
</div>
