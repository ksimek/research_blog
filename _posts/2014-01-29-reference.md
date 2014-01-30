---
layout: post
title: "GPLVM & GPDM notes"
description: ""
category: 'Reference'
tags: []
---
[1] N. Lawrence, “Probabilistic Non-linear Principal Component Analysis with Gaussian Process Latent Variable Models,” The Journal of Machine Learning Research, vol. 6, Dec. 2005.

Beautifully illustrates the relationship between GPLVM and kernel PCA with a unifying objective function.  PPCA marginalizes the input values and maximizes the linear parameters.  GPLVM marginalizes the "linear parameters" (more generally, the kernel that generalizes the linear parameters), and maximizes the inputs.

Paper provides the derivative of the marginal likelihood w.r.t. K, which greatly simplifies our derivations in [this post]({{site.baseurl}}/2013/11/25/reference/) and this one({{site.baseurl}}/2013/11/10/reference/).  We used inside-out derivation, Lawrences uses forward method, which is clearer.

[1] R. Urtasun, D. J. Fleet, A. Hertzmann, and P. Fua, “Priors for people tracking from small training sets,” presented at the Computer Vision, 2005. ICCV 2005. Tenth IEEE International Conference on, 2005, vol. 1, pp. 403–410.

Application: golf swing, walk

Learn inputs, \(\mathbf{x}\), with independent prior, \(exp(-\mathbf{x}^\top \mathbf{x})/2\).  



\partial L / \partial K = K^{-1} Y Y^\yop K^{-1} - D K^{-1}`
