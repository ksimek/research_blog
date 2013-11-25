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

When taking the derivative, the first term vanishes, and the third term was handled in the last writeup.  We need to find the derivative of the second term.  Let \\(Z(x) = \frac{1}{2} \log(|\Sigma(x)|) \\).


According to equation (38) of The Matrix Cookbook, the derivative of the log determinant is given by:

<div>
\[
\begin{align}
    \frac{\partial Z(x) }{\partial x_i} &= \frac{1}{2} \text{Tr}\left[ U^{-1} U' \right] \\
                &= \frac{1}{2} \text{Tr}\left[ U^{-1} (C + C^\top )\right] \\
                &= \frac{1}{2} \text{Tr}\left[ U^{-1} C \right]  + \text{Tr}\left[ U^{-1}  C^\top \right] \\
                &= \frac{1}{2} \text{Tr}\left[ U^{-1} S \delta_i S_i^\top \right]  + \text{Tr}\left[ U^{-1}  S_i \delta_i^\top S^\top \right] \\
                &= \frac{1}{2} \text{Tr}\left[ S_i^\top U^{-1} S \delta_i \right]  + \text{Tr}\left[ \delta_i^\top S^\top U^{-1}  S_i \right] \\
                &= \frac{1}{2} 2 \text{Tr}\left[ S_i^\top U^{-1} S \delta_i \right]  \\
                &= \frac{1}{2} 2 \text{Tr}\left[ S_i^\top U^{-1} S \delta_i \right]  \\
                &= S_i^\top U^{-1} S \delta_i \\
\end{align}
\]
</div>

Since this inner product gives us a single element of the gradient, we can get the entire gradient using matrix multiplication.
<div>
\[
    \nabla Z(x) &= \diag(S^\top U^{-1} S \Delta^\top
    \nabla Z(x) &= \sum_i (S \odot U^{-1} S \Delta^\top )_{i:}
\]
</div>

Note that we conly care about the diagonal elements of the matrix product.  The second expression avoids computing the off-diagonal elements by taking only the dot product of matrix rows/columns that result in the diagonal elmeents.  To do this, we use the Hadamard product, \\(\odot\\), and then sum over rows.
