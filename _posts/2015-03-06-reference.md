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

Let the vector \\(\\mathbf{t}\_r\\) represent a rotation of angle \\(\\|\\mathbf{r}\_r\\|\\) around axis \\(\\hat \\mathbf{t}\_r\\), and let \\(R\_{\\mathbf{t}\_r}\\) be the corresponding rotation matrix.  Let \\(K\\) be the intrinsic matrix, and let \\(\mathbf{t}\_0\\) be the translation vector.

The transformation of a point from from world coordinates to homogeneous image coordinates is using the camera \\(P\\)
  
<div>
\[
    \mathbf{x}_h(P) = K * R_{\mathbf{t}_r} * R * (\mathbf{x} - \mathbf{t}_0) .
  \]
</div>

We seek the jacobian of this transformation centered on the current camera, \\(P\\):

<div>
\[
    \begin{align}
    J(P) &= \frac{\partial x_h(P)}{\partial (f_x, f_y, s, x_0, y_0, \mathbf{t}_r, \mathbf{t}_0) } \\
      &= \left ( J_K J_{\mathbf{t}_r} J_{\mathbf{t}_0} \right) \text{ , where} \\
      J_K = &= \frac{\partial x_h(P)}{\partial (f_x, f_y, s, x_0, y_0, \mathbf{t}_r, \mathbf{t}_0) }
      J_{\mathbf{t}_r} = &= \frac{\partial x_h(P)}{\partial (\mathbf{t}_r, \mathbf{t}_0) }
      J_{\mathbf{t}_0} = &= \frac{\partial x_h(P)}{\partial (\mathbf{t}_0) }
    \end{align}
  \]
</div>
