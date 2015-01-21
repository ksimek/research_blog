---
layout: post
title: "Articulated Gaussian Processes"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

Consider an arbitrary undirected graph embedded in \\(\mathbb{R}^2\\), for example:

![]({{site.baseurl}}/img/2015-01-20-articulated_graph_1.png)

We want to generalize the Branching gaussian process to handle graphs with loops.  The basic idea is to model linear chains using a geodesic distance model and loops using 2D euclidean distance.  The result is an articulated set of plate-like subgraphs connected by  chain-like subgraphs.  We could call this an "articulated Gaussian process"; if a cubic-spline covariance model is used, this could be called an "articulated thin plate spline".   

First, we'll show how to identify chain-like and plate-like regions.  Then we'll show how to embed the graph in a high-dimensional Euclidean space such that each articulated region lies in an orthogonal hyperplane, while preserving some important distance properties.  Covariance functions over this space have nice properties, like conditional independence and piecewise smooth regions.

Partitioning into "Plates" and "Chains"
-------------------------------------

We first partition the graph into subgraphs we call "chains" and "plates."  Find biconnected components in the graph.  Biconnected components of size greater than 2 become "plates."  Biconnected components of size two are chain-links; maximal subgraphs of connected chain links are "chains."  Any vertex shared by two subgraphs is an "articulation point." By definition of biconnected components, at most one articulation point exists between two subgraphs.  Let \\(G^c = \\{G^c_i\\}\\) be the set of chain subgraphs and \\(G^p = \\{G^p_j\\}\\) be the set of plate subgraphs in the full graph, \\(G\\).

Constructing a Gaussian process
--------------------------------

Let \\(Z = \\{z_i\\}\\) be an embedding of vertices \\(V\\) in the Euclidean plane. We seek a Gaussian process over \\(Z\\) that satisfies three properties:  (a) the covariance between points on a chain is a function of their geodesic position (i.e. distance along the chain), (b) the covariance between points on a plate is a function of their Euclidean positions, and (c) points in different subgraphs (chains or plates) are independent conditioned on any articulation point on the path between them.  Naturally, we require that the covariance function be positive definite.

To guarantee positive definiteness, we will embed the graph in a high-dimensional Hilbert space and then use a standard covariance function in this space.  This allows our model to be agnostic to choice of covariance function, a hoice which we will not discuss further.  It what remains, we descibe how to construct such a space.  Briefly, to satisfy constraints (a) and (b), we embed vertices such that within subgraphs, relative vertex positions (geodesic or euclidean) are preserved.  To satisfy (c), subgraphs will lie in mutually orthogonal hyperplanes, connected only at articulation points.  

Constructing the index-space
==============================

For each plate-type subgraph \\(G\^p\_i \in G\^p \\), we define a displacement function \\(d\^p\_i : V\^2 \rightarrow \mathbb{R}\^2 \\) as the displacement \\(\boldsymbol{z}\_i - \boldsymbol{z}\_j)\\ between vertices \\(v\_i, v\_j\\) if they both are in \\(G\^p\_i\\), or \\((0,0)\\) otherwise.  Similarly, for each chain-type subgraph \\(G\^c\_i \in G\^c\\), we define a displacement \(d\^c\_i : V\^2 \rightarrow \mathbb{R} \\) as the geodesic displacement between vertices if they are both in \\(G\^c\_i\\), or zero otherwise.  We will use these pairwise subgraph displacements to construct a Hilbert space over vertices of the full graph.

For each vertex \\(v\_i \in V\\), we assign an index \\(x\_i \in \mathbb{R}\^{|G\^c| + 2\,|G\^p|} \\). We arbitrarilly pick a vertex \\(v\_0\\) to be the graph's root, and set its index to \\(x\_0 = \mathbf{0}\\).  For each vertex \\(v\_i \in V \\ v\_0\\), let \\(p(i)\\) be the index of its predecessor, using depth-first search ordering.  We define the index of \\(v\_i\\)  as

<div>
\[
x_i = x_{p(i)} + d(v_i, v_{p(i)}
\]
</div>

where \\(d : V\^2 \rightarrow \mathbb{R}\^{|G\^c| + 2\,|G\^p|}\\) is the concatenation of displacement functions, i.e. d(v,v') = \right ( d\^c\_1(v,v'), \dots, d\^p\_1(v,v'), \dots \right) \\).  Note that since every edge (v,v') can lie in exactly one subgraph, all but one of \\(d\_i\\) are zero in \\(d(v,v')\\).

Under this transformation, index displacement between two vertices is equal to the sum of pairwise displacements along the depth-first search path connecting them.  For vertices with a subgraph, this summation takes a very simple form.  The biconnected property implies that for any two vertices within a subgraph, the search path connecting them lies entirely within the subgraph.  Thus, for any two vertices \\((v,v')\\) in subgraph \(G_i\), their indices \\((x,x'\\)) differ only by \\(d_i(v,v')\\).   As a result, each subgraph lies on an axis-aligned hyperplane (2D for plates, 1D for chains) corresponding to its individual displacement function.  Furthermore, all such hyperplanes are mutually orthogonal and touch only at articulation points.  Also, within subgraphs, this index space preserves relative (Euclidean or geodesic) position from the original 2D embedding.


Covariance functions
-------------------

When using a cubic-spline covariance function, the only dimensions that are nonzero are those corresponding to shared ancestors.  The position along the curve only matters when comparing points on the same subgraph.  For trees, this exactly corresponds to the BGP covariance I derived in my dissertation proposal.  Plate regions act like thin-plate splines.

When using a radial-basis covariance function like squared exponential, the squared L2 distance has a nice interpretation.  Take the path between two nodes, and split it into subpaths at articulation points.  The squared L2 distance is the sum of the distances between articulation points, plus the squared distance between the endpoints and their nearest articulation points.  This is similar to the squared geodesic distance between the points, but modified to restart the distance measurement from zero at each articulation point.

Generalizations
------------------

It may be interesting to model plates as being superimposed on an underlying chain, for example, in the circled plate below:

![]({{site.baseurl}}/img/2015-01-20-plate_in_chain_2.png)


In this case, 1,2,3,4 is probably well modelled as a smooth curve (i.e. a chain), but 2,3,5 is also clearly a plate.   We might want to let point 5's position influence points 2 and 3, without violating smoothness of 1,2,3,4.  To handle this, we relax the requirement that the plate and chain must lie in orthogonal hyperplanes.  Instead of taking the index of its predecessor (e.g. vertex 3), the first term in the index equation for vertex 5 can be the linear interpolation between indexes 3 and 4.  This lets subgraph 2,3,5 act a little bit like a chain and a little bit like a plate.  How to implement this linear interpolation is up for debate, but two possibilities are: (a) relative euclidean distance, or (b) relative geodesic distance.  
