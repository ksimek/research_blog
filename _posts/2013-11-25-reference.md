---
layout: post
title: "Marginal likelihood gradient (part 2)"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

Today, I'll cover some additional issues not covered in the [earlier reference post on this topic]({{site.baseurl}}/2013/11/10/reference/).  First, the original gradient derivation was missing a term corresponding to the normalization constant (which isn't constant as a function of the index set).  Second, the previous write-up assumed 1-dimensional data; today we'll talk about generalizing the formulae to three dimensions.

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

When taking the derivative, the first term vanishes, and the third term was handled [in the last writeup]({{site.baseurl}}/2013/11/10/reference/) as \(\nabla g\).  We need to find the derivative of the second term.  Let \(Z(x) = \frac{1}{2} \log(|\Sigma(x)|) \). Also, let \(C_{(i)} = S \, \delta_i \, S_i^\top \), so \(U'_{(i)} = C_{(i)} + C_{(i)}^\top\)
</div>



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
\begin{align}
    \nabla Z(x) &= \text{diag}(S^\top U^{-1} S \Delta^\top \\
    &= \sum_i (S \odot U^{-1} S \Delta^\top )_{(i:)} \tag{1}
\end{align}
\]
</div>

Note that we conly care about the diagonal elements of the matrix product.  The second expression avoids computing the off-diagonal elements by taking only the dot product of matrix rows/columns that result in the diagonal elmeents.  To do this, we use the Hadamard product, \\(\odot\\), and then sum over rows.

Generalizing to three dimensions
-----------------------------------

We replace several matrices with their 3D version.

The 3D version of \\(\delta_i\\) is:

<div>
\[
\delta_i^{(3)} = P \left ( \begin{array}{ccc}\delta_i & 0 & 0 \\ 0 & \delta_i & 0 \\ 0 & 0 & \delta_i \end{array}\right) 
\]
</div>

Here, P is a permutation matrix such that PM converts the rows of M from \\((x_1, x_2, ..., y_1, y_2, ..., z_1, z_2, ...)\\) to \\((x_1, y_1, z_1, x_2, y_2, z_2, ...)\\).

Similarly, the 3D version of \\(\Delta\\) is

<div>
\[
\Delta^{(3)} = P \left ( \begin{array}{ccc}\Delta & 0 & 0 \\ 0 & \Delta & 0 \\ 0 & 0 & \Delta \end{array}\right)  P^\top
\]

The vector \(S_i\) becomes a three-column matrix, \([ S_{x_i} S_{y_i} S_{z_i}]\), corresponding to the noise-covariance of the i-th 3D point.
</div>


The expression for \\(\frac{\partial Z(x)}{\partial x_i}\\) is no longer a dot product, but the trace of a 3x3 matrix.  In practice, this is easy to implement, by replacing all matrices in eq (1) with their 3D equivalent, and then suming each (xyz) block in the resulting vector.  In matlab, we can do this cheaply by reshaping the vector into a 3x(N/3) matrix and summing over rows. If the old expression was

    grad_Z = sum(S .* inv(U) S Delta')

the new expresssion becomes
    
    grad_Z_3d = sum(reshape(sum(S .* inv(U) S Delta_3d'), 3, []));

Applying to \\(\nabla g\\)
--------------------------

We can apply a similar transformation to the other term of the gradient (which we called \\(\nabla g\\) [in this post]({{site.baseurl}}/2013/11/10/reference/).  Recall the old expression for a single elements of the graident was

<div>
\[
\begin{align}
    \frac{\partial g}{\partial x_i} = \frac{1}{2} z^\top K'_{(i)} z \tag{2}
\end{align}
\]
</div>

Recall that \\(K'\\) in 1D is sparse, having the form

<div>
\[
    K' = 
    \left( \begin{array}{c} 
        0 & 0 & \cdots & \delta_i & \cdots & 0
    \end{array}\right )
    +
    \left( \begin{array}{c} 
        0 & 0 & \cdots & \delta_i & \cdots & 0
    \end{array}\right )^\top
\]

Generalizing to the 3D equivalent, \(K'^{(3)} \), the equation becomes:
</div>


<div>
\[
\begin{align}
    K'^{(3)} &= 
    P \left( \begin{array}{c} 
        0 & 0 & \cdots & \delta_i^{(3)} & \cdots & 0
    \end{array}\right ) 
    +
    \left( \begin{array}{c} 
        0 & 0 & \cdots & \delta_i^{(3)} & \cdots & 0
    \end{array}\right )^\top P^\top
\end{align}
\]
</div>

In other words, the \\(\delta_i\\) in \\(K'\\) is replaced with a permuted block-diagonal matrix of three \\(\delta_i\\)'s.
The dot product in equation (2) then becomes the sum of the three individual dot products for x, y, and z coordinates.

We can use this observation to apply this generalization to the full gradient equation.  Recall the 1D equation for the full gradient,

<div>
\[
\begin{align}
    \nabla g = z \odot (\Delta' z) \tag{4}
\end{align}
\]

Like in the case of a single element of the gradient, we can generalize to 3D by simply taking the sum of the result for each of the x, y, and z dimensions.  We can accomplish this in a vectorized way by replacing \(\Delta\) with it's 3D equivalent \(\Delta^{(3)}\), and then sum each block of (xyz) coordinates in the resulting vector, like we did for \(\nabla Z\).  (Note that here, we assume \(z\) is computed using the 3D prior covariance, \(K^{(3)}\), and needs no explicit lifting to 3D).  In matlab, this looks like

</div>

    grad_g = sum(reshape(z .* (Delta_3d' * z), 3, []))

Mathematically, we can represent this summation by right-multiplying by permuted stack of identity matriceces.

<div>
\[
\begin{align}
    \nabla g^{(3)} = \left [ z \odot (\Delta^{(3)\top} z) \right ] P \left ( \begin{array}{c} I \\ I \\ I \end{array} \right )
\end{align}
\]
</div>


