---
layout: post
title: "Mixing Noisy and Noise-free values in GP Posterior"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

When doing ancestral sampling of the posterior, each curve's conditional posterior depends on (a) it's relevant (noisy) observation and (b) the sampled (noise-free) values of the parent.  We can incorporate both in the posterior by treating the noise-free values as observations with zero variance in the likelihood.

In practice, theres a minor issue implementing this.  Recall that because 3D observations are degenerate in one direction (namely the backprojection direction), we prefer to work with the precision matrix, \\(\Lambda\\), instead of a covariance matrix.  Under this representation, noise-free values have infinite precision, so operations on \\(\Lambda\\) are invalid.  Instead, we take a hybrid appraoch, using both precisions and covariances.

Recall the standard formulation for the posterior mean:
    
<div>
\[
    \mu = K_* \left[ K + \Sigma \right]^{-1} y
\]
</div>

Without loss of generality, assume zero-noise observations appear after noisy observations.  We can rewrite the posterior in terms of the precision matrix \\(\Lambda\\) of the noisy values:

<div>
\[
\begin{align}
    \mu &= K_* \left[ K + \left( 
                \begin{array}{cc}
                    \Lambda^{-1} & 0 \\
                    0 & 0
                \end{array}
            \right) \right]^{-1} y \\
        &= K_* \left[
        
            \left( 
                \begin{array}{cc}
                    \Lambda & 0 \\
                    0 & I
                \end{array}
             \right) 
        K + 
            \left( 
                \begin{array}{cc}
                    I & 0 \\
                    0 & 0
                \end{array}
             \right) 

            \right]^{-1} 
            \left( 
                \begin{array}{cc}
                    \Lambda & 0 \\
                    0 & I
                \end{array}
             \right) 
            y \\
\end{align}
\]
</div>

We can implement this by slightly modifying our code for the precision-matrix formulation of posterior.  First, give all noise-free values a precision of 1.0 in \\(\Lambda\\), and then modify the \\(I\\) inside the parentheses by zeroing-out elements corresponding to noise-free values.  Using prime symbol to denote the modified matricies, the result is

<div>
\[
    \mu = K_* \left[ \Lambda' K + I' \right]^{-1} \Lambda' y
\]
</div>

The expression for posterior covariance is derived in the same way, and has similar form.
