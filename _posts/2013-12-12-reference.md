---
layout: post
title: "Constant-length energy function"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 15864
---
{% include JB/setup %}

**Update: What follows is an early working of the constant-length energy function and much of which I learned to be invalid.**

Energy function and its gradient are:

<div>
\[
E = 0.5 (0.5 \mu^\top D^\top D \mu - 0.5 t^\top D^\top D t)^2 \\
\frac{\partial E}{\partial t_i} = 2E \left [ 0.5 \mu^\top D^\top D J_\mu - t^\top D^\top D  \right ]
\]
</div>

Mu and it's jacobian are:

<div>
\[
\begin{align}
\mu &= K_* S^\top \left( S K S^\top + I\right)^{-1} S y \\
    &= K_* S^\top U^{-1} S y \\
    &= K_* z \\
\frac{\partial \mu}{\partial t_i} 
    &= K'_* z + K_* z' \\
J_\mu &= \operatorname{diag_{3x1}}(\Delta_{3x3}) z + \left( \Delta_{1x3} \right)^\top \operatorname{repmat}(z_3 N/3, 1) + K_* J_z 
\end{align}
\]

where \(J_z\) is the Jacobian of \(z\), and \(z_3\) is the re-arrangement of \(z\) into columns of xyz vectors.  \(\Delta_{3x3}\) is the conversion of \(\Delta\) to 3D by block-diagonalizing three copies of \(\Delta\) and permuting rows and columns so each (x,y,z) is grouped together.  \(\Delta_{1x3}\) repeats \(\Delta\) over three columns and permuting columns.  \(\operatorname{diag_{3x1}}\) is a modified diagonalization operator where x is split into 3x1 matrices, which are arranged into block-diagonal form.
</div>



<div>
Let \(A = S^\top U^{-1} S \), so \(z = Ay \).
\[
\begin{align}
\frac{\partial z}{\partial t_i} &= \frac{\partial }{\partial t_i} D^\top U^{-1} S y \\
                              &= - S^\top U^{-1} \frac{\partial U}{\partial t_i} U^{-1} S y \\
                              &= - S^\top U^{-1} S \frac{\partial K}{\partial t_i} S^\top U^{-1} S y \\
                              &= - A \frac{\partial K}{\partial t_i} z \\
                              &= - A \left \{
                                      \left (
                                      \begin{array}{c} 
                                          \mathbf{0}             \\
                                          \vdots        \\
                                          \delta_i^\top \\
                                          \vdots        \\
                                          \mathbf{0}             \\
                                      \end{array} \right ) + 
                                      \left (
                                          \begin{array}{c}
                                          \mathbf{0} & \cdots & \delta_i & \cdots & \mathbf{0}
                                          \end{array} 
                                      \right) 
                                    \right \} z \\
         &= - A_i (\delta_i^\top z) - A \delta_i z_i \\
         &= - A_{3i:3i+2} (\delta_{i,3x3}^\top z) - A \delta_{i,3x3} z_{3i:3i+1} & \text{(3D version)} \\
J_z &= - \operatorname{sum_{1x3}}\left(A \odot \left( \Delta_{3x3} z \right)^\top \right) - A \left [ \left( \Delta_{1x3}  \right )^\top \odot \operatorname{repmat}(z_3, N/3, 1)^\top \right ]
\end{align}
\]
</div>


