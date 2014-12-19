---
layout: post
title: "GP with two constraints"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}

Consider a GP \\(f(x)\\) with covariance \\k(x,y)\\).  We can construct a new GP \\f'(x)\\) by constraining two points in \\(f(x)\\), which we'll call "endpoints".  Without loss of generality, assume the constraints occur at \\(x = 0 \\) and \\(x = 1\\).

We can derive the expression for covariance of the doubly-constrained function, \\(k''(x,y)\\).  Let \\(k_{a,b})\\) denote \\(k(a,b)\\).  Recall our [earlier result]({{site.baseurl}}/2014/12/07/reference/) for the singly-constrained GP at \\(x = 0\\):

<div>
\[
  k'(x,y) = k_{xy} - k_{x0} k_{y0} / k_{00}
\]
</div>
  
We can apply this tranformation twice to obtain \\(k''(x,y)\\):

<div>
\[
\begin{align}
  k''(x,y) &= k'_{xy} - k'_{x0} k'_{y0} / k'_{00} \\
           &= 
           (k_{xy} - k_{x0} k_{y0} / k_{00}) - 
              (k_{x1} - k_{x0} k_{10} / k_{00}) 
              (k_{1y} - k_{10} k_{y0} / k_{00})
              (k_{11} - k_{10} k_{10} / k_{00})^{-1}
           &= 
          \frac{1}{(k_{11} - k_{10} k_{10} / k_{00})^{-1}}
          \left [
            (k_{xy} - k_{x0} k_{y0} / k_{00})
            (k_{11} - k_{10} k_{10} / k_{00}) - 
            (k_{x1} - k_{x0} k_{10} / k_{00}) 
            (k_{1y} - k_{10} k_{y0} / k_{00})
          \right ] \\
          &= 
          \frac{1}{(k_{11} - k_{10} k_{10} / k_{00})}
          \left [
            (k_{xy} - k_{x0} k_{y0} / k_{00})
            (k_{11} - k_{10} k_{10} / k_{00})  - 
            (k_{x1} - k_{x0} k_{10} / k_{00}) 
            (k_{1y} - k_{10} k_{y0} / k_{00})
          \right ] \\
          &= 
          \frac{k_{00}}{k_{11}k_{00} - k_{10}^2}
          \left [
             k_{00} k_{11} k_{xy} 
            -k_{00} k_{11} k_{x0} k_{y0} /k_{00} 
            -k_{00} k_{xy} k_{10}^2/k_{00} 
            +k_{00} k_{x0} k_{y0} k_{10}^2/k_{00}^2
            -k_{00} k_{x1} k_{y1} 
            +k_{00} k_{x1} k_{y0} k_{10} /k_{00} 
            -k_{00} k_{x0} k_{y0} k_{10}^2/k_{00}^2
            +k_{00} k_{x0} k_{y1} k_{10} /k_{00} 
          \right ] \\
          &= 
          \frac{1}{k_{11}k_{00} - k_{10}^2}
          \left [
            k_{00} k_{11} k_{xy} 
           -k_{xy} k_{10} ^2
           +k_{x0} k_{y1} k_{10} 
           +k_{x1} k_{y0} k_{10} 
           -k_{x0} k_{y0} k_{11} 
           -k_{x1} k_{y1} k_{00} 
          \right ]
\end{align}
\]
</div>

It's important to note that this expression is symmetric w.r.t {0,1}. Also note that no pair of values appear more than once, making further simplification difficult.
