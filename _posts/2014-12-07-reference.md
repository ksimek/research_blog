---
layout: post
title: "Generalizing the brownian bridge"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

the Brownian bridge is a modified Weiner process a constrained that f(0)=0 and f(1)=0.  According to the [Wikipedia page](http://en.wikipedia.org/wiki/Brownian_bridge), its covariance is \\(k(x,y) = min(x,y) (1-max(x,y))\\).  

What if we want something like a Brownian bridge, but with a different base distribution?  Or a more general question: how can we derive a covariance function for a Gaussian process with a constained point?  Consider a general covariance function, \\(k_0(x,y)\\), and a constraint, \\(f(x_c) = z\\).  After conditioning on f(x_c), the new covariance function is \\(k = k_0(x,y) - k(x, x_c) k(x_c, y) / k(x_c, x_c)\\).  Notice that applying this to thw Weiner process covariance, \\(k_0(x,y) = min(x,y)\\) results in the Brownian bridge covariance: \\(k(x,y) = min(x,y) - min(x,1) min(1,y) / min(1,1) = min(x,y) - x y = min(x,y) (1 - max(x,y))\\. QED.  Deriving the mean curve in closed form is more difficult, and is likely impossible if the GP has infinite basis.  In the special case where the original mean function is zero and the constraint value is zero, the conditoinal mean is also zero.

If we want to condition both ends of the distribution to pass through constraints, we can apply the above formula twice.
