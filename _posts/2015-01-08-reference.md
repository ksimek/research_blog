---
layout: post
title: "Geodesic distance kernel and BGP kernel -- simplified representation"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}

With a nod to Mercer's theorem, we can represent gaussian processes over graph-structured points in a very simple way.  We may transform our input space over graph nodes into a new eucliean space.  

For trees with N branches, we denote a point a distance x along the i-th branch by the ordered pair \\(i, x\\).  For each branch i, its parent is denoted by p(i), and its branch point is denoted by b(i).  If branch i has not parent, we define p(i) = b(i) = 0.  We can define a transformation \\(\phi : \mathbb{N}\times\mathbb{R} \rightarrow \mathbb{R}^N\\), whose k-th dimension is:
    
  <div>
  \[
    \phi_k(i,x) = \begin{cases}
        x & \text{ if } i == k \\
        0 & \text{ if } i == 0 \\
        \phi_k(p(i), b(i)) & \text{ otherwise.}
        \end{cases}
  \]
  </div>.

If branch k is the root of a subtree containing (i,x), \\(\phi_k\\) is the branch position of sub-subtree containing (i,x).  

This formulation makes it easier to define covariance functions over tree structures.  O

It is often useful to model each tree branch as a squared-exponential curve.  This is sometimes falsely implemented as squared exponential covariance function over geodesic distance instead of Euclidean distance.  However, this covariance function isn't positive definite (need illustration).  Instead, if we define a distance function \\(d(i,x,i',x')\\) as the sum of squared geodesic distances between adjacent junctions along the path between (i,x) and (i',x').  Using this distance metric with a squared-exponential covariance function results in exactly the model we seek.

<div>
  k(i,x,i',x') = \exp\{-d(i,x,i',x')\}
</div>

We can use our transformation above to represent this more succinctly:

<div>
  k(\phi, \phi') = \exp\{- \| \phi - \phi' \|^2\}
</div>

Since each dimension in phi corresponds to exactly one branch, \\( \phi - \phi \\) is a vector of distances between branch points on the each curve corresponding to (i,x) and (i',x').  The squared l2 norm of this expression is equivalent to d(i,x,i',x').  Note that the fact that we can represent this covariance function using a standard covariance function with transformed inputs shows that it is positive definite.  

A second useful tree model is the one I introduced in my dissertation proposal -- the branching cubic spline model.  The covariance function for this model involved a recursive function that was complicated and wasn't previously proven to be positive definite.  Using our input transformation, this simplifies to:
  
<div>
\[
  k(\phi, \phi) = \sum_i k_c(\phi_i, \phi'_i)
  \]
</div>

where k_c() is the cubic spline covariance function.  The recursive nature of the definition of \\(\phi\\) ensures that each curve inherits the covariance of its parent curve.  And because \\(k_c(0,x) == 0\\), points on different subtrees only receive covariance from their shared ancestors.  Again, this formulation suffices to show that our original covariance function is positive definite.

Loopy graphs
---------------

Non-tree structured graphs are more difficult, but I have a few possible approaches.

One way of interpreting a loop is as two separate branches (one at each junction) that gradually blend into one another.  Implementing a transformation \\(\phi\\) is easy under this interpretation -- just linearly interpolate between the two independent lines in \\(\phi\\).  Unfortunately, the resulting embedding doesn't preserve distances between nearby points. I tried a similar approach with cubic Hermite splines instead of linear interpolation, but again, distances aren't preserved.  This could be solved if we could (a) guarantee that the bridging curve has exactly the right length and (b) the mapping between graph points and the bridging curve in \\(\phi\\) preserves distance.  Both of these result in equations that can't be solved analytically, but numerical techniques could work if we cared enough.

We could try something similar, but use a spherical arc to connect the two branch points in \\(\phi\\).  This would preserve total length and adjacent distances, but it violates the property that the curve's endpoint is orthogonal to its parent.

Both of these bridging techniques also violate the elegant property of the tree-based covariance, namely that the L1 distance between points is equal to thier geodesic distance.

A third possibility is to simply use the distance function \\(d(i,x,i',x')\\) we introduced before.  The down side of this is I con't think of a proof for its positive-definiteness.  But if it is PD, it should have the properties we want, and is relatively easy to implement.

