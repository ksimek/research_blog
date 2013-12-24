---
layout: post
title: "Constant-length energy function - Hessian"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 15864
---
{% include JB/setup %}

Recall energy function
<div>
\[
\begin{align}
    E &= \frac{1}{2} x^\top D^\top D x + \frac 12 \mu^\top D^\top D \mu  - x^\top D^\top \eta \\

\end{align}
\]
</div>

and its gradient, 

<div>
\[
    E' = \frac{\partial E}{\partial x} = x^\top D^\top D + \mu^\top D^\top D J_\mu - \eta^\top D - x^\top D^\top J_\eta
\]
</div>

The derivative w.r.t. t_i of E' (i.e. the i-th row of the Hessian) is given by:
<div>
\[
\begin{align}
    \frac{\partial E'}{\partial t_i} &=
        (D^\top D)_{:i} + 
        (J_\mu^\top D^\top D J_\mu)_{:i} + 
        \frac{\partial J_\mu^\top}{\partial t_i} D^\top D \mu - 
        (D^\top J_\eta)_{:i} -  
        (J_\eta^\top D^\top)_{:i} - 
        \left \{ x^\top D^\top \frac{\partial J_\eta}{\partial t_i} \right \}^\top
\end{align}
\]
</div>

Of the six terms, the third and sixth are particularly problematic when generalizing to the full hessian, because they involve the Jacobian of a Jacobian, which is a 3D tensor.

To keep running time to \\(O(n^3)\\), we'll use diagonal approximations for those terms.

<div>
\[
\begin{align}
    \frac{\partial^2 \mu}{(\partial t_i)^2} &= \frac{\partial}{\partial t_i} (J_\mu)_{:i} \\

                                            &= \frac{\partial}{\partial t_i} \left [\operatorname{diag_{3x1}}(\Delta_{3x3} z) + \left( \Delta_{1x3} \right)^\top \odot \operatorname{repmat}(z_3 , N/3, 1) + K_* J_z \right ]_{:i} \\
                                            &= \frac{\partial}{\partial t_i} \left( 
                                                    \begin{array}{c}
                                                    0 \\ 0 \\ \vdots \\ \delta^\top_{i3x3} z \\ \vdots \\ 0 \\ 0
                                                    \end{array} \right )
                                                    + \delta_{i,3x1} \odot \operatorname{repmat}(z^{(3)}_i, N/3, 1) 
    + K_* (J_z )_{:i} \\
                                            &= \left( 
                                                    \begin{array}{c}
                                                    0 \\ 0 \\ \vdots \\ C^\top_{i3x3} z \\ \vdots \\ 0 \\ 0
                                                    \end{array} \right ) + 
                                                \left (
                                                    \begin{array}{c}
                                                    0 \\ 0 \\ \vdots \\ \delta^\top_{i3x3} z'_i \\ \vdots \\ 0 \\ 0
                                                    \end{array} \right )
                                                    + C_{i,3x1} \odot \operatorname{repmat}(z'^{(3)}_i, N/3, 1) 
    + K_* (J_z )_{:i} \\
\end{align}
\]
</div>
