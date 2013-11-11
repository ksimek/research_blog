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

<p>
Here, \(M = S^\top U^{-1} S \), (which is symmetric), and \(z = M y\).  
</p>

<p>
This equation gives us a single element of the gradient, namely \(d g(x)/dx_i\).  However, once \(z\) is computed, we can recompute (1) for all other \(x_j\)'s at a cost of \(O(n^2)\), making the total gradient \(O(n^3)\), which is pretty good. (This assumes the K's can be computed efficiently, which is true; see below.)  However, we also observe that \(K'\) is sparse with size \(O(n)\), so we can do sparse multiplication to reduce the running time to linear, and **the full gradient takes \(O(n^2)\). ** Cool! 
</p>

</div>
<p></p>

Derivatives of K(x)
-------------------

The structure of \\(\frac{\partial K}{\partial x_i}\\) is sparse; only the i-th row and i-th column are nonzero. We can find the values of the nonzero elements by taking the derivative of the kernel function.

** Cubic covariance **

Recall the cubic covariance expression:
    
<div>
\[
k(x_1, x_2) = (x_a - x_b) x_b^2 / 2 + x_b^3/3
\]

Where \(x_b = min(x_1, x_2)\) and \(x_a = max(x_1, x_2)\).
</div>

Taking the derivative w.r.t. \(x_2\) gives:
<div>
\[
k(x_1, x_2) = 
    \begin{cases}
         x_2^2 / 2 & \text{if } x_2 >= x_1 \\
         x_1 x_2 - x_2^2/2 & \text{if } x_2 < x_1 
    \end{cases}
\]

Or equivalently

\[
k(x_1, x_2) = 
         x_2 \left [ \max(x_1,x_2)  - x_2/2 \right ]
\]
</div>

** Linear Covariance **

Recall the cubic covariance expression:
    
<div>
\[
k(x_1, x_2) = x_1 x_2
\]

The derivative w.r.t. \(x_2\) is simply \(x_1\).
</div>

** Offset Covariance **

Recall the offset covariance expression:
    
<div>
\[
k(x_1, x_2) = k
\]

The derivative w.r.t. \(x_2\) is zero.
</div>


** Implementation **

Implemented end-to-end version in `kernel/get_model_kernel_derivative.m`; see also components in `kernel/get_spacial_kernel_derivative.m` and `kernel/cubic_kernel_derivative.m`.

These functions return all of the partial derivatives of the matrix with respect to the first input.   The i-th row of the result make up the nonzero values in \\(\frac{\partial K}{\partial x_i}\\).  Below is example code that computes all of the partial derivative matrices.

    N = 100;
    % construct indices
    x = linspace(0, 10, N);
    % construct derivative rows
    d_kernel = get_model_kernel_derivative(...);
    d_K = eval_kernel(d_kernel, x, x);
    % construct dK/dx_i, for each i = 1..N
    d_K_d_x = dcell(1,N);
    for i = 1:N
        tmp = sparse(N, N);
        tmp(i,:) = d_K(i,:);
        tmp(:,i) = d_K(i,:)';
        d_K_d_x{i} = tmp;
    end

** Directional Derivatives **

I think we can get directional derivatives of \\(K\\) by taking the weighted sum of partial derivatives, where the weights are the component lengths of the direction vector.  I have yet to confirm this beyond a hand-wavy hunch, and in practice, this might not even be needed, since computing the full gradient is so efficient.
