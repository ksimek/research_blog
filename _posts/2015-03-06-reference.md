---
layout: post
title: "Camera refinement"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

To implement efficient camera refinement, I need to derive the Jacobian of the residial vector w.r.t. camera parameters.  

Let the transformation of a point from world to homogeneous image coordinates be:
  
<div>
\[
    x_h = (K+dK) * dR * R * (x - t - dt)
  \]
</div>

Here, \\(dR\\) is 
