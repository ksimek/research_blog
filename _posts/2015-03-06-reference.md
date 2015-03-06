---
layout: post
title: "Camera refinement"
description: ""
category: 'Reference'
tags: []
---
{% include JB/setup %}

To implement efficient camera refinement, I need to derive the Jacobian of the residial vector w.r.t. camera parameters.  

The parameterization of camera orientation deserves special discussion.  We prefer a parameterization that is free of constraints, so quaternions and rotation matrices aren't an option, leaving euler angles or an axis/angle vector. Both parameterizations have singularities, but we can avoid them by centering the parameterization at the camera's current orientation.  If we don't expect to drift too far from the current orientation, this should be okay; otherwise we can reparameterize after every step.  We follow Hartley and Zisserman's approach and use axis-angle parameterization.  For all other parameters, we will use no transformation.

Let the vector \\(\\mathbf{t}\_r\\) represent a rotation of angle \\(\\|\\mathbf{r}\_r\\|\\) around axis \\(\hat{\mathbf{t}}\_r\\), and let \\(R\_{\\mathbf{t}\_r}\\) be the corresponding rotation matrix.  Let \\(K\\) be the intrinsic matrix, and let \\(\mathbf{t}\_0\\) be the translation vector.

The transformation of a point from from world coordinates to homogeneous image coordinates is using the camera \\(P\\)
  
<div>
\[
    \mathbf{x}_h(P) = K \, R_{\mathbf{t}_r} , R \, (\mathbf{X} - \mathbf{t}_0) .
  \]
</div>

We seek the Jacobian of this transformation centered on the current camera, \\(P\\):

<div>
\[
    \begin{align}
    J_h(P) &= \frac{\partial x_h(P)}{\partial (f_x, f_y, s, x_0, y_0, \mathbf{t}_r, \mathbf{t}_0) } = \left ( J_K J_{\mathbf{t}_r} J_{\mathbf{t}_0} \right) \text{ , where} \\
      J_K &= \frac{\partial x_h(P)}{\partial (f_x, f_y, s, x_0, y_0 ) } \\
      J_{\mathbf{t}_r} &= \frac{\partial x_h(P)}{\partial (\mathbf{t}_r, \mathbf{t}_0) } \\
      J_{\mathbf{t}_0} &= \frac{\partial x_h(P)}{\partial (\mathbf{t}_0) }
    \end{align}
  \]
</div>

Deriving \\(J\_{\mathbf{t}\_r}\\)
------------------

When centered at the current camera, the rotation vector is zero, \\(\mathbf{t}\_r = (0,0,0)\\).  For small \\(\mathbf{t}\_r\\),  the rotation matrix is approximated by \\( R\_{\mathbf{t}\_r} = I + [\mathbf{t}\_r]\_\times \\).  The Jacobian of rotation \\( R\_{\mathbf{t}\_r} \mathbf{X}\\)  is then \\( -[\mathbf{X}]\_\times \\), and the jacobian of \\(x\_h\\) is 

<div>
\[
    J_{\mathbf{t}_r} = -K [\mathbf{X}_c]_\times
  \]
</div>

where  \\(\mathbf{X}\_c = R (\mathbf{X} - \mathbf{t}\_0)\\) is the point in camera coordinates.

Deriving \\(J\_{\mathbf{t}\_0}\\) and \\(J\_K\\)
-------------------------------------------------

The other derivatives are straightforward to derive.

The Jacobian w.r.t. translation is:

<div>
\[
    J_{\mathbf{t}_0} = -K R 
\]
</div>

The Jacobian w.r.t. intrinsic parameters is

<div>
\[
    J_K = \frac{\partial x_h}{\partial (f_x, f_y, s, x_0, y_0 ) } = \left ( \begin{array}{ccccc}
        X_{c,1} & 0 & X_{c,2} & X_{c,3} & 0 \\
        0 & X_{c,2} & 0 & 0 & X_{c,3}  \\
        0 & 0 & 0 & 0 & 0
        \end{array}\right )
  \]
</div>

Jacobian of residuals
--------------------

We've derived the jacobian of the transformation from world to homogeneous image coordinates w.r.t. each camera parameter.  To get the Jacobian of the residuals, it remains to transform to nonhomogeneous screen coordinates.  

<div>
\[
    \mathbf{x} = (x_{h,1} / x_{h,3}, x_{h,2} / x_{h,3})
  \]
</div>

The Jacobian of this is 

<div>
\[
\begin{align}
    J_\mathbf{x}(\mathbf{x_h}) &= 
    \left ( 
        \begin{array}{ccc}
        \frac{1}{x_{h,3}} & 0 & - \frac{x_{h,1}}{x_{h,3}^2} \\
        0 & \frac{1}{x_{h,3}} & - \frac{x_{h,2}}{x_{h,3}^2}
        \end{array}
    \right ) \\
      &=
      \frac{1}{x_{c,3}} 
    \left ( 
        \begin{array}{ccc}
        1 & 0 & - x_1 \\
        0 & 1 & - x_2
        \end{array}
    \right )
\end{align}
  \]
</div>

where \\(x\_{c,3}\\) is the point's depth in camera coordinates, and \\((x\_1, x\_2)\\) is the point in nonhomogeneous image coordinates.

The Jacobian of the residuals w.r.t. camera parameters is then

<div>
\[
\begin{align}
    J &= J_\mathbf{x} J_h \\
      &= J_\mathbf{x} [ J_K J_{\mathbf{t}_r} J_{\mathbf{t}_0} ]
\end{align}
\]
</div>

In what follows, we'll drop the \\(J\_\mathbf{x}\\) and use \\(J\_K\\) to refer to the Jacobian of the residuals (and likewise for \\(J\_{\mathbf{t}\_r}\\) and \\(J\_{\mathbf{t}\_0}\\)).  In other words, let \\(J\_K \leftarrow J\_\mathbf{x} J\_K\\).

Full Jacobian with Shared Intrinsics
-------------

We now derive the Jacobian of all residuals in all views, where cameras share the same intrinsic parameters.

Let \\(J\_{K\_{ij}}\\) be the Jacobian of residuals the \\(j\\)th point in view \\(i\\) w.r.t. intrinsic parameters, and let \\(J\_\\mathbf{R\_{i,j}}\\) be the same w.r.t. rotation.  Let \\(J\_{\mathbf{t}\_i}\\) be the Jacobian w.r.t. translation in view \\(i\\).

The full Jacobian  is a block matrix with form:
  
<div>
\[
J = 
\left (
    \begin{array}{c|c|c|c}
    \overbrace{
      \begin{array}{c}
        J_{K_{11}}  \\
        J_{K_{12}}  \\
        J_{K_{13}}  \\
           \cdots   \\
           \hline
        J_{K_{11}} \\
        J_{K_{12}} \\
        J_{K_{13}} \\
           \cdots \\
      \end{array}}^\text{All} & 
    \overbrace{
      \begin{array}{cc}
         J_{R_{11}} & J_{\mathbf{t}_1} \\
         J_{R_{12}} & J_{\mathbf{t}_1} \\
         J_{R_{13}} & J_{\mathbf{t}_1} \\
           \cdots & \cdots  \\
           \hline
         \mathbf{0} & \mathbf{0}       \\
         \mathbf{0} & \mathbf{0}       \\
         \mathbf{0} & \mathbf{0}       \\
           \cdots & \cdots  \\
      \end{array}}^\text{Camera 1} & 
      \overbrace{
      \begin{array}{cc}
          \mathbf{0} & \mathbf{0}  \\
          \mathbf{0} & \mathbf{0}  \\
          \mathbf{0} & \mathbf{0}  \\
           \cdots & \cdots  \\
           \hline
           J_{R_{11}} & J_{\mathbf{t}_1}  \\
           J_{R_{12}} & J_{\mathbf{t}_1}  \\
           J_{R_{13}} & J_{\mathbf{t}_1}  \\
           \cdots & \cdots 
       \end{array}}^\text{Camera 2} &
      \begin{array}{cc}
       \mathbf{0} & \cdots \\
       \mathbf{0} & \cdots \\
       \mathbf{0} & \cdots \\
           \cdots & \cdots & \cdots  \\
           \hline
       \mathbf{0} & \cdots \\
       \mathbf{0} & \cdots \\
       \mathbf{0} & \cdots \\
           \cdots & \cdots & \cdots  \\
      \end{array}
    \end{array}
    \right )
\]
</div>
