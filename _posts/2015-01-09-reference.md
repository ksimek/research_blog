---
layout: post
title: "Projection of point onto line using distance from two reference points"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}

Consider two known points A, and B, an unknown point C. If we know the distances between C and the other two points, we can recover \\(\pi\_{AB}(C)\\), the projection of C onto the line AB.

The distance between \\(\pi\_{AB}(C)\\) and A is 

<div>
\[
\begin{align}
d(A, \pi_{AB}(C)) = d(A,B) (1+g) / 2 \text{, where} \\
g &= \left ( d(A,C)^2 - d(B,C)^2 \right ) / d(A,B)^2
\end{align}
\]
</div>

This can be derived using the pythagorean theorem and fact triangles AC\pi(C) and BC\pi(C) share a side.

This can be used to derive an expression for \\(\pi\_{AB}(C)\\) using a weighted sum of A and B:

<div>
\[
\begin{align}
\pi_{AB}(C) &= (A(1-g) + B(1+g) ) / 2
\end{align}
\]
</div>

