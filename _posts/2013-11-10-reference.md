---
layout: post
title: "Gradient w.r.t. Indices"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

To optimize indices, we'll need to compute the derivative of the marginal log-likelihood w.r.t. changing indices.  

I first tried to derive this using the generalization of the chain rule to matrix expressions (see matrix cookbook, section 2.8.1), but the computation exploded.  Since ultimately, the derivative is a simple single-input, single output function, we can use differentials to derive the solution.


Let the marginal likelihood as a function of indices be \\(g(x)\\):
    
<div>
\[
    \frac{\partial g(x)}{\partial x_i} = \frac{\partial}{\partial x_i} y^\top S^\top ( I + S K(x) S^\top)^{-1} S y
\]

Let \(U = I + S K(x) S^\top\), and \(V = U^{-1}\).  Working inside out, lets find \(\frac{\partial U}{\partial x_i}\).

\[
\begin{align}
    U + dU  &= I + S (K + dK) S ^\top \\
            &= I + S K S^\top + S dK S ^\top \\
        dU  &= S \, dK\, S^\top \\
        U'  &= S K' S^\top
\end{align}
\]

Where \(M'\) is the derivative of the elements of \(M\) w.r.t. \(x_i\).  Next, \(\frac{\partial V}{\partial x_i}\), which comes from the matrix cookbook, equation (36).

\[
    dV = -U^{-1} \, dU \, U^{-1} \\
    V' = -U^{-1} U' U^{-1}
\]

Finally,  \(\frac{\partial g(x)}{\partial x_i}\):
    
\[
\begin{align}
    g + dg  &= y^\top S^\top (V + dV) S y \\
    g + dg  &= y^\top S^\top \, V \, S y + y^\top S^\top \,dV \,S y \\
        dg  &= y^\top S^\top \,dV \,S y \\
        g'  &= y^\top S^\top \, V' \,S y \\
\end{align}
\]

Expanding \(g'\) gives the final formula:
\[
\begin{align}
        g'  &= y^\top S^\top U^{-1} S K' S^\top U^{-1} S y \\
        g'  &= y^\top M K' M y \\
        g'  &= z^\top K' z \tag{1}\\
\end{align}
\]

Here, \(M = S^\top U^{-1} S \), (which is symmetric), and \(z = M y\).  

This equation gives us a single element of the gradient, namely \(d/dx_i\).  However, once \(z\) is computed, we can recompute (1) for all other \(x_j\)'s at a cost of \(O(n^2)\), making the total gradient \(O(n^3)\), which is pretty good. (This assumes the K's can be computed efficiently, see below.)  Also note that this equation isn't limited to axis-oriented directions, we can find the directional derivative for any direction \(v\), as long as we can find \(\frac{\partial K}{\partial v}\), which we'll cover next.  In this way, we can find the derivative in a small number of principal directions, k, resulting in an improved running time of \(O(n^2 k)\).  The hard part is picking a good set of principal directions; the eigenvectors of K might not be a bad choice, but computing them efficiently becomes the crux of the problem.

</div>

Derivatives of K(x)
-------------------


