---
layout: post
title: "Constant-length energy function -- revisited"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

My [earlier derivation]({{site.baseurl}}/2013/12/12/reference/) of the constant-length energy function was flawed, because it pooled the individual lengths before comparing them to the pooled index-spacing.  Thus, this energy function enforces the *sum* of squared lengths but not the individual lengths.  Chalk it up to trying to be too clever in avoiding a square root.

In what follows, I derive a new energy function and its gradient.  The Jacobians of \\(\mu\\) and \\(z\\) are re-used from the earlier treatment.

<div>
<p>
  Let \(\mu\) be the maximum posterior curve, given an index set, \(\mathbf{x}\), arranged as a single column in "xyzxyz" format.  Let \(\mu^{(3)}\) be the 3 by N/3 matrix obtained by rearranging the points of \(\mu\) into column vectors.  That is, the i-th column \(\mu^{(3)}_i\) is the i-th reconstructed point.  
  </p>

<p>
  Let \(\eta\) be the vector of absolute distances between adjacent points in \(mu^{3}\). Formally,
  
\[
    \eta_i = \| \mu^{(3)}_i - \mu^{(3)}_{i-1} \|.
\]

Note that \(\eta^\top \eta = \|\eta\|^2 = \mu^\top D^\top D \mu\), where \(D\) is the adjacent differences matrix, adapted to operate on column vectors in the "xyzxyz" format.

</p>
</div>

The constant width energy function is defined as

<div>
\[
\begin{align}
    E &= \frac{1}{2} \left ( Dx  - \eta \right ) ^2 \\
      &= \frac{1}{2} x^\top D^\top D x + \frac 12 \eta^\top \eta  - x^\top D^\top \eta \\
      &= \frac{1}{2} x^\top D^\top D x + \frac 12 \mu^\top D^\top D \mu  - x^\top D^\top \eta \\

\end{align}
\]
</div>

Gradient is given by 

<div>
\[
    \frac{\partial E}{\partial x} = x^\top D^\top D + \mu^\top D^\top D J_\mu - \eta^\top D - x^\top D^\top J_\eta
\]
</div>

where \\(J_z\\) is the Jacobian of \\(\mathbf{z}\\) w.r.t. \\(\mathbf{x}\\).

The Jacobian of \\(z\\) and \\(\mu\\) are derived in [this earlier post]({{site.baseurl}}/2013/12/12/reference/).  It remains to find the Jacobian of \\(\eta\\).

<div>
Note the identity \( \eta_i^2 = \| \mu^{(3)}_i - \mu^{(3)}_{i-1} \|^2 \) can be rewritten in terms of the full vector \(\eta\) as 

\[
\eta \odot \eta = \operatorname{sum_{3x1}}(D \mu \odot D \mu)
\]

where \(\operatorname{sum_{kx1}}\) implements k-way blockwise summation over columns of a matrix.  Formally, it is the function \(f : \mathbb{R}^{NxM} \rightarrow R^{(N/k)xM}\) (for any N divisible by k), such that 

\[
    (f(A))_{ij} = \sum_{s = (i-1)\times k+1}^{i \times k} A_{sj}
\]
</div>

The Jacobian of \\(\mathbf{\eta}\\) can then be given by

<div>
\[

\begin{align}
\frac{\partial \eta}{\partial x_i} &= \frac{\partial}{\partial x_i} \left ( \eta \odot \eta \right)^{\circ\frac12} \\
                                 &= \frac{\partial}{\partial x_i} \left ( \operatorname{sum_{3x1}}(D \mu \odot D \mu) \right)^{\circ\frac12} \\
                                &= \frac12 \left ( \eta \odot \eta \right)^{\circ \frac{-1}{2}} \frac{\partial}{\partial x} 
                                    \left ( \operatorname{sum_{3x1}}(D \mu \odot D \mu )\right) \\
                                &= \frac12 \eta^{\circ (-1)} 
                                     \left ( \operatorname{sum_{3x1}}(\frac{\partial}{\partial x} D \mu \odot D \mu )\right) \\
                                &= \frac12 \eta^{\circ (-1)} 
                                     \left ( \operatorname{sum_{3x1}}( 2 D \mu \odot D J_\mu )\right) \\
                                &= \eta^{\circ (-1)} \left ( \operatorname{sum_{3x1}}( D \mu \odot D J_\mu )\right) \\

\end{align}
\]

where \(x^{\circ(-1)} = \left( \frac{1}{x_{ij}} \right)\) is the Hadamard (i.e. element-wise) inverse, and \(x^{\circ \frac12}\) is the Hadamard root.
</div>






