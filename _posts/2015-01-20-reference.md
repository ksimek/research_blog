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

We want to generalize the branching gaussian process to handle graphs with loops.  The basic idea is to model linear chains using a geodesic distance model and loops using 2D euclidean distance.  The result is an articulated structure of plate-like regions connected by  wire-like regions.  We call this an "articulated Gaussian process"; if a cubic-spline covariance model is used, this could be called an "articulated thin plate spline".   

We construct the model as follows.  Find biconnected components in the graph.  Any biconnected component of size greater 2 becomes a link in a chain.  Biconnected components of size greater than 2 become "plates".  For each vertex, we assign an index of dimension 2P+C, where P is the number of plates, and C is the number of chains.    Perform a depth-first search of the graph.  Each point's index is given by

x_i = x\_{p(i)} + 

Each chain occupies a 1D Euclidean space, where the coordinate of each vertex un the subspace is defined as its geodesic displacement from an origin vertex on the chain (to be defined later).  Each plate occupies a 2D Euclidean space, where the coordinate of each vertex is defined as the Euclidean displacement from an origin vertex on the plate.  The entire graph occupies the cartesian product of all of these spaces, which has dimension C + 2P, where C is the number of chains, and P is the number of plates. Each vertex \\(v_i\\) has a coordinate \\(x_i \in \\mathbb{R}^{C+2P}\\), defined as follows.

Take an arbitrary vertex \\(v_0\\) as the root of the graph, and let \\(x_0 = mathbf{0}\\).  Then for each vertex \\(v \in V \\ v\_0\\), we defined its predecesor \\(p(v)\\) using depth-first search.  The index \\(x_i\\) for vertex \\(v_i\\) is defined in terms of its predecessor index \\(x\_p(i)\\) as follows:

<div>
\[
  x_i = x_{p(i)} + d(v_i, p(v_i))
\]
</div>

For any two adjacent vertices v,v', the edge (v,v') occupies exactly one of the plate or chain subspaces above.  We define d(v,v') as the displacement vector within that subspace, and zero in all other dimensions.
Here, d(v, v') is function a displacement vector between vertices in their corresponding subspace (chain or plate).  

Each edge in the graph is either a chain edge or a plate edge.  

x_
