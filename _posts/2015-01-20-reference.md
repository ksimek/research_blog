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

Another example is the skeletonization of a binary image, in which each skeleton pixel is a vertex, and adjacent skeleton pixels have an edge between them.  Below is an example of a skeletonized neuron image:
  
![]({{site.baseurl}}/img/2015-01-20-neuron_skeleton.png)

We want to generalize the Branching gaussian process to handle graphs with loops.  The basic idea is to model linear chains using the traditional 1D covariance based on curve-distance, and model loops using a 2D covariance based on euclidean position (e.g. 2D squared exponential covariance).  The result is an articulated set of plate-like subgraphs connected by  chain-like subgraphs.  We could call this an "articulated Gaussian process" as a generalization to "branching Gaussian processes".

First, we'll show how to separate the graph into chain-like and plate-like regions.  Then we'll show how to embed the graph in a high-dimensional Euclidean space wuch that traditional covariance functions over this space have nice properties, like conditional independence and piecewise smooth regions.

Partitioning into "Plates" and "Chains"
-------------------------------------

We first partition the graph into subgraphs we call "chains" and "plates."  First, find [biconnected components](http://en.wikipedia.org/wiki/Biconnected_component) in the graph using Tarjan's algorithm.  Biconnected components of size greater than 2 become "plates."  Biconnected components of size two are chain-links; maximal subgraphs of connected chain links are "chains."  Any vertex shared by two subgraphs is an "articulation point."  Let \\(G\^c = \\{G\^c\_i\\}\\) be the set of chain subgraphs, \\(G\^p = \\{G\^p\_j\\}\\) be the set of plate subgraphs.

Below is such a partition, with chains and plates identified:

![]({{site.baseurl}}/img/2015-01-20-biconnected_components_reprise.png)


Constructing a Gaussian process
--------------------------------

Let \\(Z = \\{z_i\\}\\) be the 2D position of vertices \\(V = \\{v_i\\}\\) embedded in the Euclidean plane. We seek a Gaussian process over \\(Z\\) that satisfies three properties:  (a) the covariance between points on a chain must be a function of their geodesic position (i.e. distance along the chain), (b) the covariance between points on a plate must be a function of their Euclidean positions, and (c) points in different subgraphs must be independent conditioned on any articulation point on the path connecting them.  Naturally, we require that the covariance function be positive definite.

To guarantee positive definiteness, we will embed the graph in a high-dimensional Hilbert space and then use a standard covariance function on this space.  This allows our model to be agnostic to choice of covariance function.  In what follows, we descibe how to construct such a space, which we call the graph's _index space_.  Briefly, we satisfy constraints (a) and (b) by embedding vertices such that relative positions within subgraphs are preserved.  To satisfy (c), subgraphs will be embedded in mutually orthogonal hyperplanes, connected only at articulation points.    

Constructing the index-space
==============================

For each plate-type subgraph \\(G\^p\_i \in G\^p \\), we define a local displacement function \\(d\^p\_i : V\^2 \rightarrow \mathbb{R}\^2 \\):
    
<div>\[
d^p_i(v,v') = \begin{cases}
    z - z' & \text{ if } v,v' \in G^p_i \\
      0 & \text{ otherwise,}
      \end{cases}
\]
</div>

where \\((z,z')\\) are the 2D Euclidean position of vertices \\((v,v')\\). Similarly, for each chain-type subgraph \\(G\^c\_i \in G\^c\\), we define a local displacement \\(d\^c\_i : V\^2 \rightarrow \mathbb{R} \\).  For any two vertices \\(v,v'\\) connected by path \\(\mathcal{P}\\), we define the local displacement by the geodesic distance between the points:

<div>\[
  d^c_i(v,v') = \begin{cases}
    \sum_{(j,k) \in \mathcal{P}} ||z_j - z_k|| & \text{ if } v,v' \in G^c_i \\
      0 & \text{ otherwise}
      \end{cases}
  \]
  </div>

Note that for chains, exactly one such path exists, making the above expression well-defined. 

We define the full displacement \\(d : V\^2 \rightarrow \mathbb{R}\^{|G\^c| + 2|G\^p|}\\) as the concatenated outputs of all local displacements, i.e. \\(d(v,v') = (d\^c\_1(v,v'), d\^c\_2(v,v'), \dots, d\^p\_1(v,v'), d\^p\_2(v,v'), \dots)\\).  The full displacement will be central to defining the index-space.

We arbitrarilly pick a vertex \\(v\_0\\) to be the graph's root and use depth-first search to impose a tree topology over the other vertices.  Because the subgraphs are biconnected, this also defines a tree-topology over subgraphs.  We define the "local origin" of a subgraph as the vertex first encountered in a depth-first search.    For all non-root vertices \\(v_i\\), we introduce the concept of a "predecessor" vertex \\(v_{\pi(i)}\\).  The predecessor of a local origin is the the parent subgraph's local origin; the predecessor of all other vertices is the local origin of the subgraph that contains it.

For each vertex \\(v\_i \in V\\), we assign an index \\(x\_i \in \mathbb{R}\^{|G\^c| + 2\,|G\^p|} \\).  Let the root vertex \\(v_0\\) have index \\(x_0 = \mathbf{0}\\).  For all other vertices, we define the index recursively:

<div>
\[
  x_i = x_{\pi(i)} + d(v_i, v_{\pi(i)})
\]
</div>


Because vertices within a subgraph differ only by their local displacement, each subgraph lies on an axis-aligned hyperplane (2D for plates, 1D for chains).  All such hyperplanes are mutually orthogonal and touch only at articulation points.  Also, within hyperplanes corresponding to plates (resp. chains), relative Euclidean (geodesic) position is preserved from the original 2D embedding.


