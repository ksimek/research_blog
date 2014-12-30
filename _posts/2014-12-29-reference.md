---
layout: post
title: "Graph matching with epipolar constraints"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}

What follows is a variation on the work of Serradell et al. (CVPR 2012), in which we inroduce an epipolar constraint and use a covariance function based on geodesic distance.

Consider a 3D tree structure observed in two views as 2D trees.  We seek a correspondences between points in the 2D trees.  We treat this as a problem of matching graphs embedded in \\(\mathbb{R}^2\\), which we solve using nonlinear Gaussian process regression using epipolar constraints to ensure the result is consistent with the known camera configuration.

Consider a embedded graph in two views, A and B.  We model the graph in B as arising from an affine transform of the graph in A plus a nonlinear deformation.  The goal is to find a correspondence between the graph vertices that minimizes the distortion between them.  

Epipolar constraints
----------------------

We can use the known relationship between two cameras to constrain we expect points \\(X_A\\) to appear in view B.  The fundamental matrix \\(F\\) between view A and view B is a 3x3 matrix that constrains points in \\(X_A\\) to lie on their epipolar line in view B.  Because we expect both the points and the fundemental matrix to include some error, we relax this constraint and assume each point lies near its epipolar line with variance \\(\sigma\^2_e\\).  

For any point \\(x\\) in A, epipolar line in view B is given by \\(\mathbf{l} = F\^T [\mathbf{x}\^\top 1]\^\top \\).  The normal vector perpendicular to the epipolar line is \\(\hat {\mathbf{l}}_n = [l_1 l_2]\^\top / \\| [l_1 l_2] \\|\\).  The penalized epipolar constraint can be expressed as a Gaussian distribution \\(\mathcal{N}(\mathbf{e}', \Sigma_e)\\), where \\(\mathbf{e'}\\) is the epipole in view B, and \\(\Sigma_e\^{-1} = \sigma_e\^2 (\mathbf{l_n} \mathbf{l_n}\^\top)\\).  Note that the precision matrix \\(\Sigma_e\^{-1}\\) is rank-deficient, indicating infinite variance along the epipolar line. 

The joint likelihood of all points \\(X\^A = \mathbf{x}\^A_1, ..., \mathbf{x}\^A_M\\) with epipolar normals \\(\boldsymbol{l}_{n1}, ..., \boldsymbol{l}_{nM}\\) is

<div>
\[
\begin{align}
\mu_E &= [\mathbf{e}'^\top \mathbf{e}'^top ...]^\top \\
\Sigma^{-1}_E &= S S^T \text{, where} \\
S &= \sigma_e \begin{array}{ccc} \left ( 
    \mathbf{l_{n1}} & 0 & \dots & 0 \ 
    0 & \mathbf{l_{n2}} & \dots & 0\
    \vdots & \vdots & & \vdots\ 
    0 & 0 & \dots & \mathbf{l_{nM}}
    \right )
    \end{array}
\end{align}
\]
</div>

Prior 
-----

Let \\(\{v_1^A, ..., v_M^A \}\\) be the vertices in graph A, with 2D positions \\(X^A = \{x_1^A, ..., x_M^A\}\\).  We model the position of point \\(x_i^A\\) in view B as arising from a Gaussian process centered at  \\(X^A\\).  We assume dimensions are independent *a-priori*, and define the one-dimensional prior covariance between the \\(i\\)th and \\(j\\)th vertices as,

<div>
\[
  k(i,j) = \theta_0 + \theta_1 x_i^T x_j + \theta_2 \exp \right \{ -frac{\theta_3}{2} \| x_i - x_j  \|^2 \left \} + \theta_4 \exp \right \{ -frac{\theta_5}{2} d( v_i, v_j) \left \}  \.\.(1)
\]
</div>

Here, \\(d(v_i, v_j)\\) is the geodesic graph distance, i.e. the closest path between vertices \\(v_i\\) and \\(v_j\\).  The first three terms are the same as Serradell et al. -- the first two terms define an affine transformation and the third is a nonlinear distortion term encouraging local geometry in A to remain similar in B.   However, we recognize that points with dissimilar 3D position may appear similar in 2D due to projection.  The significant parallax shift between such points violates the assumption of this Euclidean-distance covariance function.  We introduce a new term using geodesic distance, which we observe to be much less distorted by projection than Euclidean distance.   This provides a better explanation for parallax shift between points at similar Euclidean positions, but dissimilar positions in the graph.  

For any pair of index sequences \\(I, J\\), we define \\(k(I,J)\\) as the gram matrix of one-dimensional prior covariances \\(k(i,j)\\) for all pairs \\((i,j) \in I \cross J\\).
    
Although the prior treats the x and y dimensions as independent, our epipolar penalty introduces correlation between dimensions.  The kronecker product   Let \\(X_I\\) be the vertical concatenation of 2D points with indices \\(I = i_1, ..., i_n\\).  We define the prior covariance between point sets \\(X_I\\) and \\(X_J\\) as 

<div>
\[
\\(K(I,J) = k(I,J) \ocross I_2\\), 
\]
</div>

where \\(\ocross\\) denotes Kronecker product and \\(I_2\\) is a 2x2 identity matrix.  The Kronecker product converts the \\(|I|x|J| \\) covariance matrix over a sequence of 1D variables to a \\(2|I|x2|J|\\) covariance matrix over a sequence of stacked 2D variables with independent dimensions.

Correspondence matching
------------------------

To estimate correspondences between \\(X^A\\) and \\(X^B\\), we follow the coarse-to-fine matching strategy in Serradell et al. (2012), modified to introduce 2D correlations of the epipolar penalty.  Given a (possibly empty) set of \\(N\\) correspondences, we can derive a posterior distribution over possible locations for points \\(X^A\\) in view B.  Let \\(X^B_N\\) be the points in graph B corresponding to points in A with indices \\(J_N = j_{1}, ..., j_{N}\\).  Let \\(J\\) be the set of all vertex indices in graph A.  The marginal posterior for point \\(x^A_{i_*}\\) is

<div>
\[
  \begin{align}
  \mu_N(i_*) &=  K_*^T C^{-1}_N \begin{array}{c} X_N^B \\ \mu_E \end{array} \\
  \sigma^2_N(i_*) &= K(i_*, i_*) + \sigma_n^2 I_2 - K_*^T C_N^{-1} K_*  \text{, where} \\
  \C_N^{-1} &= \begin{array}{cc} \left (
  K(J_N, J_N) + \sigma_n^2 I & K(J, J_N) \\
  K(J_N, J) & K(J,J) + \Sigma_E
  \right )^{-1}
  \end{array}
\]
</div>

However, because \\(\Sigma_E^{-1} \\) is rank-deficient, we must rewrite \\(C_N^{-1}\\)  as

<div>
\[
  \begin{align}
  \C_N^{-1} &= 
  \begin{array}{cc} \left (
      0 & I \\
      0 & S
  \right ) \end{array}
  
  \begin{array}{cc} \left (
  K(J_N, J_N) + \sigma_n^2 I & S K(J, J_N) \\
  K(J_N, J) S & S^\top K(J,J) S + I
  \right )^{-1} \end{array}
  \begin{array}{cc} \left (
      0 & I \\
      0 & S^\top
  \right ) \end{array}
\]
</div>

Note that despite \\(\Sigma_E^{-1}\\) being rank-deficient, the expression above is non-singular.

Using the expression above, we can compute the Z-score of each point in B against each point in A.  Starting with an empty correspondence set, we construct a set of correspondence candidates whose z-score is below a threshold.  We sample a correspondence from that set, weighted by z-score, and update all candidate z-scores conditioning on the new correspondence set.  We repeat until no valid candidates exist.  To avoid spending time on bad matches, we quit early if the relative geodesic distances between corresponding graphs differ too greatly.
