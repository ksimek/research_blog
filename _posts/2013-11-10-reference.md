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
    \frac{\partial g(x)}{\partial x_i} = \frac{\partial}{\partial x_i} 
        \frac{1}{2}(-y^\top S^\top ( I + S K(x) S^\top)^{-1} S y)
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
    g + dg  &= -\frac{1}{2}y^\top S^\top (V + dV) S y \\
    g + dg  &= -\frac{1}{2}y^\top S^\top \, V \, S y - \frac{1}{2} y^\top S^\top \,dV \,S y \\
        dg  &= -\frac{1}{2}y^\top S^\top \,dV \,S y \\
        g'  &= -\frac{1}{2}y^\top S^\top \, V' \,S y \\
\end{align}
\]

Expanding \(V\) gives the final formula:
\[
\begin{align}
        g'  &= \frac{1}{2}y^\top S^\top U^{-1} S K' S^\top U^{-1} S y \\
        g'  &= \frac{1}{2}y^\top M K' M y \\
        g'  &= \frac{1}{2}z^\top K' z \tag{1}\\
\end{align}
\]

<p>
Here, \(M = S^\top U^{-1} S \), (which is symmetric), and \(z = M y\).  
</p>

<p>
This equation gives us a single element of the gradient, namely \(d g(x)/dx_i\).  However, once \(z\) is computed, we can reuse it  when recomputing (1) for all other \(x_j\)'s.  The cost of each subsequent gradient element becomes \(O(n^2)\), making the total gradient \(O(n^3)\), which is pretty good. (This assumes the K's can be computed efficiently, which is true; see below.)  However, we also observe that \(K'\) is sparse with size \(O(n)\), so we can do sparse multiplication to reduce the running time to linear, and <strong>the full gradient takes \(O(n^2)\)</strong>, assuming \(z\) is precomputed.  Cool! 
</p>

</div>
<p></p>



Derivatives of K(x)
-------------------

First, we'll layout the general form of K', whose elements are the full derivative of the kernel w.r.t.  \\(x_k\\).

<div>
\[
\frac{\partial K_{ij}}{\partial x_k} = \frac{\partial k(x_i, x_j)}{\partial x_i} \frac{d x_i}{d x_k} + \frac{\partial k(x_i, x_j)}{\partial x_j} \frac{d x_j}{d x_k}\\
\]
</div>

The first term is nonzero only on the i-th row of K', and the second term is nonzero on the i-th column of K'.  This suggests the following convenient sparse representation  for K'.

Let the vector \\(\delta_i\\)  be the vector whose j-th element is \\( \frac{\partial k(x_i, x_j) }{\partial x_i} \\).  Using this notation, we can rewrite \\(K'\\) as

<div>
\[
    \frac{\partial K}{\partial x_i} = K' = C + C^\top  \tag{4}
\]
</div>

where \\(C = \left(0 \, \dots \, \delta_i \, \dots \, 0 \right)  \\).



Below we derive the derivative \\(\frac{\partial k(x_i, x_j)}{\partial x_i}\\) for each of the three covariance expresssions.

*Cubic covariance*

Recall the cubic covariance expression:
    
<div>
\[
k(x_i, x_j) = (x_a - x_b) x_b^2 / 2 + x_b^3/3
\]

Where \(x_b = min(x_i, x_i)\) and \(x_a = max(x_i, x_i)\).
</div>

Taking the derivative w.r.t. \(x_i\) gives:

<div>
\[
\begin{align}
\frac{\partial k(x_i, x_j)}{\partial x_i} &= 
    \begin{cases}
         x_j^2 / 2 & \text{if } x_i >= x_j \\
         x_i x_j - x_i^2/2 & \text{if } x_i < x_i
    \end{cases} \\
            &= 
    \begin{cases}
         x_b^2 / 2 & \text{if } x_i >= x_j \\
         x_a x_b - x_b^2/2 & \text{if } x_i < x_j
    \end{cases} \\
\end{align}
\]
</div>

Or equivalently

<div>
\[
\frac{\partial k(x_i, x_j)}{\partial x_i} = 
         x_b \left ( x_j  - x_b/2 \right ) \tag{2}
\]
</div>

*Linear Covariance*

Recall the linear covariance expression:
    
<div>
\[
k(x_i, x_j) = x_i x_j
\]

The derivative w.r.t. \(x_i\) is simply \(x_j\).

</div>

*Offset Covariance*

Recall the offset covariance expression:
    
<div>
\[
k(x_i, x_j) = k
\]

The derivative w.r.t. \(x_i\) is zero.
</div>


*Implementation*

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

*Directional Derivatives*

I think we can get directional derivatives of \\(K\\) by taking the weighted sum of partial derivatives, where the weights are the component lengths of the direction vector.  I have yet to confirm this beyond a hand-wavy hunch, and in practice, this might not even be needed, since computing the full gradient is so efficient.

Full gradient
--------------

As we saw earlier, \\(\frac{\partial K}{\partial x_i}\\) is sparse, and has the form in equation (4).  We can use the sparsity to ultimately compute the entire gradient in a single matrix multiplication.

First we'll rewrite \\(g'\\) in terms if \\(\delta_i\\)
    
<div>
\[
\begin{align}
g' &= \frac{1}{2} z^\top K' z \\
   &= \frac{1}{2} z^\top C z + z^\top C^\top z \\
   &= \frac{1}{2} \left \{ (0 \, \dots \, z^\top \delta_i \, \dots \, 0) z + z^\top (0 \, \dots \, \delta_i^\top z \, \dots \, 0)^\top \right \} \\
   &= z_i (\delta_i \cdot z)
\end{align}
\]
</div>

We can generalize this to the entire gradient using matrix operations:

<div>
\[
\begin{align}
    \nabla g = z \odot (\Delta z) \tag{4}
\end{align}
\]

</div>

Where \\(\Delta\\) is the matrix whose ith row is \\(\delta_i\\), and \\(\odot\\) denotes element-wise multiplication.

To handle multiple dimensions, simply apply to each dimension independently and sum the results.
