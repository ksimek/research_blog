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

We'll denote the covariance for a constrained GP by k(x,y ; a, b), where a,b are the constraint  indices.

Curve trees with runners
--------------------------

We can modify the curve tree model to introduce "runners" -- special curves that are connected on both ends to curve tree curves.  The introduction of runner curves transforms a curve tree into a curve DAG.  In general, it isn't possible to unambiguously identify runners by inspecting a DAG, because there are always at least two ways to break a loop.  Thus, we need to augment our directed graph with labels to indicate runners explicitly.

A runner differs from a normal curve in two ways.  First, that it always has two parents, which define its endpoints.  Second, its gaussian process differs from a standard curve, due to it being constrained on both ends.  The runner curve process is a linear process connecting its two endpoints, plus a smooth curve process that allows deviations from the linear curve.  The latter process must be constrained on both ends to pass through the endpoints, using the derivation above.

### Deriving the runner covariance

Let \\(A\\) and \\(B\\) be random variables representing endpoints of a runner curve, lying somewhere on its parent curves.  A straight line between those curves is given by 

<div>
\[
  f(t) = t A + (1-t) B
\]
</div>

Let us derive the covariance of two points \\(X = f(s) \\) and \\(Y = f(t)\\) on the line.  

<div>
\[
\begin{align}
  cov (X,Y) &= E[XY] - E[X]E[Y] \\
           &= E[XY] - 0 \text{(assiming zero mean curves)} \\
           &= E[ \right ( tA + (1-s) B \left) \right ( tA + (1-t) B \left) ] \\
           &= E[ ts A^2] + E[t(1-s)BA] + E[s(1-t)BA] + E[(1-t)(1-s)B^2 ]
           &= ts var(A) + cov(B,A) [t (1-s) + s (1-t)] + (1-t)(1-s)var(B)
\begin{end}
\]
</div>

The GP above assumes endpoints occur at 0 and 1. We can relax this to end at \\(T_\mathrm{max}\\), giving us the "linear interpolation gaussian process:
  
<div>
\[
\begin{align}
  k_l(s,t; T_\mathrm{max}) &= 1/T_\mathrm{max}^2 \right ( ts var(A) + cov(B,A) [t (T_\mathrm{max}-s) + s (T_\mathrm{max}-t)] + (T_\mathrm{max}-t)(T_\mathrm{max} - s)var(B) \left )
\begin{end}
\]
</div>


This gaussian process will form the backbone of the runner curv.   To allow deviations from the linear path, we add a smooth curve GP with covariance \\(k_c\\).  This GP must be constrained to pass through zero at \\(0\\) and \\(T_\mathrm{max}\\) using the derivation above.  For any two points on the runner, the covariance is given by:

<div>
\[
\begin{align}
  k(x,y) &=  \right( k_l(x,y ; T_\mathrm{max}) + k_c(x,y ; 0,T_\mathrm{max})  \left ) + 
\begin{end}
\]
</div>

If \\(x\\) lies on the runner and \\(y\\) lies elsewhere on the curve DAG, the covariance is:

<div>
\[
\begin{align}
  cov(X,Y) &= E[XY] \\
           &= E[(sA + (1-s)B) Y] \\
           &= E[sAY] + E[(1-s)BY ] \\
           &= s \mathrm{cov}(AY) + (1-s)\mathrm{cov}(BY) \\
\begin{end}
\]
</div>

i.e. the linear intpolation of its endpoint covariances.

One notable property of the runner curve is that it introduces no additional attachment between its parent curves.  For this reason, we can first construct the curve tree covariance matrix without runners, and then add runner blocks in a second pass.  This is nice, because the runner equation doesn't fit nicely into the recursive equation for BGP covariance.
