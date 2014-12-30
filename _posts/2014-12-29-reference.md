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

Let \\(\{v_1^A, ..., v_M^A \}\\) be the vertices in graph A, with 2D positions \\(X^A = \{x_1^A, ..., x_M^A\}\\).  We model the position of point \\(x_i^A\\) in view B as arising from a Gaussian process centered at  \\(X^A\\).  We assume dimensions are independent *a-priori*, and define the one-dimensional prior covariance between the \\(i\\)th and \\(j\\)th vertices as:

<div>
\[
  k(i,j) = \theta_0 + \theta_1 x_i^T x_j + \theta_2 \exp \right \{ -frac{\theta_3}{2} \| x_i - x_j  \|^2 \left \} + \theta_4 \exp \right \{ -frac{\theta_5}{2} d( v_i, v_j) \left \}  \.\.(1)
\]
</div>

Here, \\(d(v_i, v_j)\\) is the geodesic graph distance, i.e. the closest path between vertices \\(v_i\\) and \\(v_j\\).  The first three terms are the same as Serradell et al. -- the first two terms define an affine transformation and the third is a nonlinear distortion term encouraging local geometry in A to remain similar in B.   However, we recognize that points with dissimilar 3D position may appear similar in 2D due to projection.  The significant parallax shift between such points violates the assumption of this Euclidean-distance covariance function.  We introduce a new term using geodesic distance, which we observe to be much less distorted by projection than Euclidean distance.   This provides a better explanation for parallax shift between points at similar Euclidean positions, but dissimilar positions in the graph.  


