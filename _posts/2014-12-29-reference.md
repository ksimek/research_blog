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

<div>\[
  \def\CV#1{\boldsymbol{#1}}
  \def\cross{\times}
  \def\ocross{\otimes}
  \]</div>

What follows is a variation on the work of [Serradell et al. (CVPR 2012)](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CCUQFjAA&url=http%3A%2F%2Fcvlab.epfl.ch%2Ffiles%2Fcontent%2Fsites%2Fcvlab2%2Ffiles%2Fpublications%2Fpublications%2F2012%2FSerradellGKMF12.pdf&ei=YDWjVMXYCpWwogSmj4HYDQ&usg=AFQjCNFCQfO_wNWnnFZa_35HQtW9xA3ogA&bvm=bv.82001339,d.cGU), which we modify to introduce an epipolar constraint and use a covariance function based on geodesic distance.  The epipolar constraint requires significant rework of the original derivation, which assumes the x and y dimension are independent.  The use of geodesic distance is necessary to handle parallax motion not present in Serradell's data.

Consider a 3D tree structure observed in two views as 2D trees.  We seek a correspondence between points in the 2D trees.  We treat this as a problem of matching graphs embedded in \\(\mathbb{R}^2\\), which we solve using nonlinear Gaussian process regression, using epipolar constraints to ensure the result is consistent with the known camera configuration.

Consider a embedded graph in two views, A and B, with vertex positions \\(X\_A = \\{x\^A\_1, \dots, x\^A\_{M\_A}\\}\\) and \\(X\_B = \\{x\^B\_1, \dots, x\^B\_{M\_B}\\}\\).  We model the graph in B as arising from an affine transform of the graph in A plus a nonlinear deformation.  The goal is to find a correspondence between the graph vertices that minimizes the distortion between them.  Because the graph structures may be noisy, we seek an approach that is robust to graphs with minor differences in topology.

Epipolar constraints
----------------------

We can use the known relationship between two cameras to constrain we expect points \\(X_A\\) to appear in view B.  The fundamental matrix \\(F\\) between view A and view B is a 3x3 matrix that constrains points in \\(X_A\\) to lie on their epipolar line in view B.  Because we expect both the points and the fundemental matrix to include some error, we relax this constraint and assume each point lies near its epipolar line with variance \\(\sigma\^2_e\\).  

For any point \\(\boldsymbol{x}\\) in view A, the epipolar line in view B is given by \\(\boldsymbol{l} = F\^T [\boldsymbol{x}\^\top 1]\^\top \\).  The normal vector perpendicular to the epipolar line is \\(\hat {\boldsymbol{n}} = [l_1 l_2]\^\top / \\| [l_1 l_2] \\|\\).  The penalized epipolar constraint can be expressed as a Gaussian distribution \\(\mathcal{N}(\boldsymbol{e}', \Sigma_e)\\), where \\(\boldsymbol{e'}\\) is the epipole in view B, and \\(\Sigma_e\^{-1} = (\hat{\boldsymbol{n}} \hat{\boldsymbol{n}}\^\top) / \sigma_e\^2 \\).  Note that the precision matrix \\(\Sigma_e\^{-1}\\) is rank-deficient, representing infinite variance along the epipolar line. 

The joint likelihood of all points \\(X\^A = \\{\boldsymbol{x}\^A_1, \dots, \boldsymbol{x}\^A_M\\}\\) with epipolar normals \\(\\{\boldsymbol{\hat{n}}\_1, \dots, \boldsymbol{\hat{n}}\_M\\}\\) is \\(\mathcal{N}(\mu_E, \Sigma_E)\\), where

<div>
\[
\begin{align}
\mu_E &= [\boldsymbol{e}'^\top \boldsymbol{e}'^\top \dots]^\top \\
\Sigma^{-1}_E &= S S^\top \\
S &= (1/\sigma_e) \left ( \begin{array}{cccc} 
    \boldsymbol{\hat{n}}_{1} & 0 & \dots & 0 \\
    0 & \boldsymbol{\hat{n}}_{2} & \dots & 0 \\
    \vdots & \vdots & & \vdots \\ 
    0 & 0 & \dots & \boldsymbol{\hat{n}}_{M}
    \end{array}
    \right ).
\end{align}
\]
</div>

Nonrigid deformation prior 
-----

We assume the motion of points from view A to view B arise as an affine transformation plus some nonrigid deformation.  The main cause of nonrigid deformation is parallax motion, but other less predictable factors like camera lens distortion of small scene movements are possible too.

Assuming motion in the x and y direction are independent, single-dimensional prior covariance between the \\(i\\)th and \\(j\\)th points is

<div>
\[
  k(i,j) = \theta_0 + \theta_1 x_i^T x_j + \theta_2 \exp \left \{ -\frac{\theta_3}{2} \| x_i - x_j  \|^2 \right \} + \theta_4 \exp \left \{ -\frac{\theta_5}{2} d( v_i, v_j) \right \}.  \;\;(1)
\]
</div>

Here, \\(d(v_i, v_j)\\) is the geodesic graph distance, i.e. the closest path between vertices \\(v_i\\) and \\(v_j\\).  The first three terms are the same as Serradell et al. -- the first two terms define an affine transformation and the third is a nonlinear distortion term that penalizes local geometry in A being distorted in B.   However, we recognize that points with dissimilar 2D position may appear similar in 2D due to projection.  The significant parallax shift between such points violates the locality assumption of the third covariance term.  The fourth term in (1) introduces deformation based on geodesic distance.  We observe that relative geodesic distances are better preserved under projection than relative Euclidean distances.   This term provides a better explanation for parallax shift between points at similar Euclidean positions but dissimilar positions in the graph.  

Equation (1) applies to one-dimensional points; we need an expression relating two-dimensional points.  The x and y dimensions are independent under the prior, so the covariance matrix over 2D points is simply a block-diagonal matrix of two covariance matrices over 1D points.  We permute this matrix so dimensions are ordered first by increasing point index, then spatial dimension.  Formally, let \\(X\_I\\) and \\(X\_J\\) be the vertical concatenation of 2D points with indices \\(I = \\{i\_1, \dots, i\_m\\}\\) and \\(J = \\{j\_1, \dots, j\_n\\}\\).  Define \\(k(I,J)\\) as the gram matrix of covariances \\(k(i,j)\\) for each pair \\((i,j) \in I \cross J\\).  We define the prior covariance between point sets \\(X\_I\\) and \\(X\_J\\) as 

<div>
\[
K(I,J) = k(I,J) \ocross I_2, 
\]
</div>

where \\(\ocross\\) denotes Kronecker product and \\(I\_2\\) is a 2x2 identity matrix.  The result is a \\(2 \vert I \vert \times 2 \vert J \vert\\) covariance matrix over a sequence of stacked 2D variables with independent dimensions.

Correspondence matching
------------------------

To estimate correspondences between \\(X\^A\\) and \\(X\^B\\), we follow the coarse-to-fine matching strategy in Serradell et al. (2012).  We first find a coarse set of correspondences between branch points and tips using the method below.  A fine-grained correspondence is then found between the densely spaced remaining points, conditioned on the coarse correspondences.  

Given a (possibly empty) set of \\(N\\) correspondences, we can derive a posterior distribution over possible locations for points \\(X\^A\\) in view B.  For a given correspondence of size N, let \\(X\^B\_N\\) be the points in graph B corresponding to points in A with indices \\(J\_N = \\{j\_{1}, \dots, j\_{N}\\}\\).  Let \\(J = \\{1, \dots, M\\}\\) be the set of all vertex indices in graph A.  The marginal posterior for point \\(x\^A\_{i\_\*}\\) is

<div>
\[
  \begin{align}
  \mu_N(i_*) &=  K_*^T C^{-1}_N \left ( \begin{array}{c} X_N^B \\ \mu_E \end{array} \right ) \\
  \sigma^2_N(i_*) &= K(i_*, i_*) + \sigma_n^2 I_2 - K_*^T C_N^{-1} K_*  \text{, where} \\
  C_N^{-1} &= 
  \left (
  \begin{array}{cc} 
  K(J_N, J_N) + \sigma_n^2 I & K(J, J_N) \\
  K(J_N, J) & K(J,J) + \Sigma_E
  \end{array}
  \right )^{-1}
  \end{align} \\
  K_* = K(J_N, i_*)
\]
</div>

However, because \\(\Sigma_E^{-1} \\) is rank-deficient, we must rewrite \\(C_N^{-1}\\)  as

<div>
\[
  \begin{align}
  C_N^{-1} &= 
  \left (
  \begin{array}{cc} 
      I & 0 \\
      0 & S
  \end{array}
  \right ) 
  
  \left (
  \begin{array}{cc} 
  K(J_N, J_N) + \sigma_n^2 I & S K(J, J_N) \\
  K(J_N, J) S & S^\top K(J,J) S + I
  \end{array}
  \right )^{-1}

  \left (
  \begin{array}{cc} 
      I & 0 \\
      0 & S^\top
  \end{array}
  \right ) 
  \end{align}
\]
</div>

Note that despite \\(\Sigma_E^{-1}\\) being rank-deficient, the expression above is non-singular.

Using the expression above, we can compute the z-score of each point in B against the image of each point in A.  Starting with an empty correspondence set, we construct a set of correspondence candidates whose z-score is below a threshold.  We use z-score as weights to sample a correspondence from that set, and use that correspondence to update the z-scores of all remaining candidates by conditioning on the new correspondence set.  We repeat until no valid candidates exist.  Unclaimed vertices are treated as outliers.  We repeat this process several times and keep the best fit.  To avoid spending time on bad matches, we quit early if the relative geodesic distances between corresponding graphs differ too greatly.  

Fine-grained correspondences between remaining points can be found using the Hungarian algorithm using pairwise z-score as a cost metric.

3D reconstruction
--------------------

The simplest approach to 3D reconstruction is to triangulate the corresponding points in two views.  Multiple views can be chained together from pairwise correspondence using transitivity.  A better approach would be to use my BGP model to find an optimal registration between sequences of recovered 3D trees.  I don't know if I could fit both the above and that into a single conference paper, because the temporal BGP model is a bit complicated.  I have a simpler model in mind that might work better, and might be easier to squeeze into the end of a paper.  

Results
-------
None yet, working on it.

