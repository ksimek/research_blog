---
layout: post
title: "Marginal likelihood gradient (part 2)"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

Today, I'll cover some additional issues not covered in the earlier reference post on this topic.  First, the original gradient derivation was missing a term corresponding to the normalization constant (which isn't constant as a function of the index set).  Second, the previous write-up assumed 1-dimensional data; today we'll talk about generalizing the formulae to three dimensions.

Normalization constant
------------------------

Recall the gaussian equation, as a function of indices:

<div>
\[
\frac{k}{|\Sigma(x)|^{\frac{1}{2}}} \exp\left\{-2 (y - \mu)^\top \Sigma^{-1}(x) (y - \mu) \right\}
\]
</div>

Taking the log gives

<div>
\[
\log(k) - \frac{1}{2} \log(|\Sigma(x)|) + \left( -2 (y - \mu)^\top \Sigma^{-1}(x) (y - \mu) \right )
\]
</div>

When taking the derivative, the first term vanishes, and the third term was handled in the last writeup.  We need to find the derivative of the second term.


According to equation (38) of The Matrix Cookbook, the derivative of the log determinant is given by:

<div>
\[
\begin{align}
    \frac{\partial }{\partial x_i} \frac{1}{2} \log(|\Sigma(x)|) &=
\end{align}
\]
</div>
