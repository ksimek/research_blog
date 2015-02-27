---
layout: post
title: "Projecting Prior and Backprojecting Posterior"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

We have existing machinery that lets us find the optimal (maximum a-posteriori) 2D curve tree, given a 2D Gaussian prior and a foreground probability map.

We'd like to use that to perform tracking when we know a 3D Gaussian distribution over the tree position, given previous evidence.  
 
Given: \\(p(x_n | y_{1:n-1}) \\) 

Estimate: \\(p(x_n | y_{1:n}) \\)


1. Rotate/scale the 3D prior to be aligned with the image plane in pixel coordinates, i.e. u,v, and depth
2. Estimate the marginal posterior in (u,v) coordinates using our warping code
3. Estimate the depth terms of the posterior analytically
4. Un-rotate and unscale the posterior into world space.

Step 1
-----------

Let \\(p(x_n | y_1, ..., y_{n-1})\\) be the prior of \\(x_n)\\), conditioned on all previous data.  At the current prior mean, \\(\mu\\), the projection function \\(\pi(x)\\) has Jacobian, \\(J(\mu)\\), which can be decomposed using RQ decomposition into \\(J = (R 0) Q\\), where Q is a rotation and R is square, upper triangular, and nonsingular.  This corresponds to rotating to face the camera, followed by scaling and/or shearing corresponding to foreshortening at the given depth.  The projection function can be then approximated using taylor series expansion:
  
<div>
\[
  \pi(x) = \pi(\mu) + (R \,| \,0) Q (x - \mu)
  \]
</div>

We can project the 3D prior to 2D using this transformation:
  
<div>
\[
  \mathcal{N}(\mu_{2D}, A^{-1}_{2D}) = \mathcal{N}(\pi(\mu_{3D}), (R\,|\, 0) (Q A_{3D} Q^\top)^{-1} (R \, | \, 0)^\top)
  \]
</div>

Here \\(A\_{2D}\\) and \\(A\_{3D}\\) are precision matrices.

Step 3
---------

For this section, let \\(\mu = \mu\_{2D}\\) as derived above, let \\(A = Q A\_{3D} Q^\top\\)  and let \\(x' = \pi(x)\\) be the projected point.
Let \\(p(y\_n | x'\_n) = \mathcal{N}([R^{-1} \; 0]^\top \mu\_L, \, [R^{-1} \;  0]^\top L^{-1} [R^{-1} \; 0] )\\) be the image likelihood in 3D space, where \\(\mu\_L\\) is \\((x'\_1, x'\_2)^\top\\), and \\(L\\) is a 2x2 precision matrix.  Let \\(L' = R^{-\top} L R^{-1}\\) and \\(\mu'\_L = R^{-1} \mu\_L\\) Running warping in step 2 gives us the hessian \\(H\\) of the marginal in-plane posterior.  This is the negative marginal posterior covariance for the (u,v) space.  Since the likelihood is uninformative in the dpeth directiom, the deriving the full posterior covariance, \(Z\), is straightforward:

<div>
\begin{align}
      Z &= A + \left( \begin{array}{cc}L' & 0 \\ 0 & 0\end{array} \right)  \\
       &= \left ( \begin{array}{cc} -H & A_{1:2,3} \\ A_{3,1:2} & A_{3,3} \end{array} \right )
\end{align}
</div>

Warping also gives us the marginal posterior mean \\(\pi\_x, \pi\_y\\), in the image space.  Let \\(\pi'\_x = \pi(\mu) + R^{-1} \pi\_x\\) and \\(\pi'_y = R^{-1} \pi_y\\) be the marginal posterior interse-transformed by the lineariezed projection function.  Deriving \\(\pi'_z\\) takes a few steps  (primes are omitted below, all quantities are assumed to be in rotated 3D space)

<div>
\begin{align}
      \mathbb{\pi} &= \left[ A + \left( \begin{array}{cc}L & 0 \\ 0 & 0\end{array} \right)\right]^{-1} \left [ A \mu + \left ( \begin{array}{c}L \mu_L \\ 0\end{array} \right ) \right ]  \\
      \mathbb{\pi} &= Z^{-1} \left [ A \mu + \left ( \begin{array}{c}L \mu_L \\ 0\end{array} \right ) \right ]  \\
      Z \mathbb{\pi} &= \left [ A \mu + \left ( \begin{array}{c}L \mu_L \\ 0\end{array} \right ) \right ]  \\
\end{align}
</div>
Let \\(A = (\mathbb{a_1}  \mathbb{a_2} \mathbb{a_3} )^\top \\) be the rows of A.   Omitting all but the third row gives:
<div>
\begin{align}
      \mathbb{z_31} \pi_x + \mathbb{z_32} \pi_y + \mathbb{z_33} \pi_z &= \mathbb{a_3^\top} \mu \\
        \pi_z &= (a^\top_3 \mu - \pi_x z_{31} - \pi_y z_{32}) / z_{33} 
\end{align}
</div>

Observing that \\(z_3i = a_3i\\), 

<div>
\begin{align}
        \pi_z &= a_{33}^{-1} \left ( \mathbb{a}^\top_3 \left (\mu - \left ( \begin{align}{c} \pi_x \\ \pi_y\end{align}\right)\right)\right)
\end{align}
</div>

Written compactly:

<div>
\begin{align}
        \pi_z &= \mu_3 + a_{33}^{-1} a_{3,1:2}(\mu_{1:2} - \pi_{1:2});
\end{align}
</div>

Testing in matlab:
    
  A = rand(3,3); A = A * A';
  L = rand(2,2); L = L * L';
  mu = randn(3,1);
  mu_L = randn(2,1);
  pi = inv(A + [L zeros(2,1);0 0 0]) * (A * mu + [L*mu_L; 0]);
  true_pi_z = pi(3);
  test_pi_z = mu(3) + A(3,1:2)*(mu(1:2) - pi(1:2))/A(3,3);
  err = test_pi_z - true_pi_z

  err =

    -2.2204e-16

It remains to rotate \\(\mathbb{\pi}\\) and \\(A\\)  by \\(Q^\top\\) to convert back to world space.

