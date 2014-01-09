---
layout: post
title: "Roughing out Proposal"
description: ""
category: 'Work Log'
tags: []
---
{% include JB/setup %}

Summary
----------

Problem Statement
-------------------

Difficulties

* Unknown dimensionality
* irregular topology
* 
* Nonrigid motion
* thin, High curvature surfaces with little texture
* 


The proposed work will

The primary contribution of this research will be a novel method for robust reconstruction of thin, textureless structure from multiple views, a specific case of multiple view reconstruction that is rarely considered.  To this end, our work will make novel contributions in several areas, including
    
* A probabilistic generative model for branching structure in 3D that is applicable across many domains and problem settings.
* A Bayesian formulation of multiple-view 4D reconstruction of thin branching structure that is robust to camera miscalibration and nonrigid motion.
* Several novel edge-based likelihood functions, which are robust to noise and missing data and can be evaluated efficiently on GPU hardware.
* A novel formulation of multiple-view reconstruction as a Bayesian data-association problem, and an approach for appoximate inference.
* An efficient dynamic programming algorithm for dense multiple-view point correspondences of linear structure.
* A novel, principled approach to the problem of Bayesian model selection in the presence of nonlinear likelihood terms.  


Importance of Topic
-----------------------

###Plant biology, food source###

Researchers estimate that global food production must double by 2050 to meet the expected growth in demand \cite{tilman2011}.  Advances in high-throughput genotyping have yielded great advancements in the understanding of plant biology at the micro- level, but without efficient methods for macro-level analysis, the relationship between genetic variation and practical measures like crop yields or drought resistance remains difficult to study.  High-throughput phenotyping provides a way to bridge this micro-/macro- gap by automatically quantifying observable traits (e.g morphology, behavior), allowing macro-level study of plants from different genetic strains at a large scale.

Existing high-throughput systems 

and demand for simpler, lower-cost systems has increased in recent years

The earliest high throughput phenotyping platforms (HTPPs) used expensive sensing equipment, proving the effectiveness of HTPPs but illustrating a need for lower-cost solutions \cite{TODO}.  TODO:  Make an argument about the lack of 3D analysis of full branching architecture.  Use \cite{fiorani2013} to survey existing methods,  use \cite{biskup2007} as example similar to ours.

High-throughput phenotyping 
    understanding mutatations
    phenotyping is a limiting factor in breeding
    high-throughput genotyping has left a gap in the phenotyping 
    relating genes to biological traits (e.g. crop yields, drought resistance, root system efficiency)
    Understand the effects of genetic variation in terms of practical measures like crop yields or drought resistance.
    understand connections between genetics and macro structure

###Reconstruction###

Multiple view 3D reconstruction is a widely-studied area in computer vision.  While this area has seen great success in recent years, most research has focused on reconstructing large structures with considerable surface area \cite{TODO}.  Most of these approaches fail in the presence of thin, textureless structure like those exhibited by plant stems.  The applications for multiple-view reconstruction are 

###

    By separating the concerns of modelling and inference, our approach should generalize well to other research areas that involve branching linear systems, like neuron tracing \cite{TODO}, vascular segmentation \cite{TODO}, and root structure architecture \cite{TODO}.  We intend to 





Prior Research
-----------------

* Biological application

RSA, Hypotrace, etc.

* Multi-view Reconstruction

*Visual Hull*

    Reconstructing 3D models from multiple images is a central area of computer vision.   Laurentini proposed an early algorithm for constructing what he called the "visual hull", the largest closed 3D mesh whose projection is consistent with silhouettes in multiple images \cite{Laurentini1994}.  Laurentini's method assumed the use could obtain high-quality foregorund, background segmentation, with minimial noise.  Other approaches achieve better robustness by using a voxel representation, and they reconstruct using a Hough transform-based vote-counting method \cite{TODO}.  These methods are effective at suppressing structure arising from noisy pixels, but as they are still essentially an intersection-based method, can omit 3D structure when intersection doesn't occur, for example in the presence of slightly miscalibrated cameras.  This shortcoming is particularly noticible when reconstructing thin structure, when most or all of the structure can be absent.  One problem with visual hull reconstructions is that only false positives are penalized, which Amy Tabb's work addresses by penalizing both false positives and false negatives equally \cite{Tabb2013}.  We consider the larger problem to be the fact that in the presence of imperfect data, perfect intersection is *impossible*.  Our approach addresses this by explicitly modeling the perturbations that cause intersections to fail.

*PMVS first attempt*

    The well-known patch-based multiple view stereo algorithm (PMVS) uses full-color images to reconstruct a 3D mesh \cite{furukawa2010}, making them effective when a silhouette is unavailable.  For each image patch, a similar image patch is sought in other views such that both appearance and depth are roughly consistent between matches.  However, due to ambiguities that arise in flat image regionts, the algorithm starts by matching special keypoints whose surface exhibit distinct texture, and filling-in patches in-between.  In our situation, our surfaces are extremely thin (often three pixels or fewer in width) and exhibit no notable texture features, causing patch-based reconstructions to fail.  Further, PMVS assumes rigid structure and perfectly calibrated cameras; our plant's slight movements and our miscalibrated cameras would likely cause the algorithm's consistency checks to fail.

*PMVS Second attempt*

    The well known asdfjl;kj uses appearance consistency to estimate the depth of image patches.  It relies heavilly on texture data to find inital matches, which makes it ineffective at reconstructing textureless structure like plant stems.  Futhermore, like the visual-hull based methods, our miscalibrated cameras and slightly moving plant structure would cause the consistency checks in this algorithm to fail.

* Tracking
* Bayesian Model Choice

    Model selection is challenging problem in statsitical modelling that arises whenever the dimensionality of the model is unknown.  Posterior densities of differing dimension cannot legitimately be compared any more than the area of a square be compared to the volume of a cube.  Proper Bayesian model selection requires integrating over all of the model parameters, an operation that usually lacks a closed-form solution and numerical integration is intractible in high dimensions.  
    
    Peter Green's reversible-jump Markov-chain Monte Carlo (RJMCMC) sampler \cite{TODO green 96} proposes a dimension-matching method by which a sampler can move between similar models of differing dimension in an unbiased way; asymtotically, the number of samples from each model obeys the marginal posterior distribution over models.  However, naively constructed reversible jump moves usually exhibit poor mixing, which prevents the sampler from exploring the solution space efficiently.  Several methodologies have been developed for constructing efficient RJMCMC moves. The data-driven MCMC  framework (DDMCMC) uses bottom-up methods to generate good candidates for up-moves (moves to higher dimension)\cite{TODO song-chun zhu} \cite{dellaert2005}, but fails to address down-moves in regions without candidates, and evaluating proposal probabilities requires integrating over all possible candidates .  Moment-matching heuristics \cite{brooks2007} improve acceptance of up-moves by optimizing the position and scale of the proposal distribution, but like DDMCMC, evaluating proposal probabilities involves marginalizing over all proposal paths, making it intractible in many scenarios.   Delayed acceptance \cite{al-awadhi2004} and delayed rejection \cite{green2001} provide modest improvements in acceptance rates, but do not obviate the need to construct quality jump proposals.  Even with good transdimensional mixing, RJMCMC requires a huge number of samples before the optimal model can be chosen with confidence, making it computationally expensive.

    Another approach to model selection is to replace the intractible integral with a tractible approximation; several such methods are described in \cite{gilks1995}.  In scenarios where the posterior is well approximated by a second order Taylor series expansion, Laplace's method can be applied as in \cite{azevedofilho1994}.  When gradient and hessian are too expensive to compute directly, the Laplace-Metropolis method can be applied to approximates them using existing MCMC samples \cite{Lewis1997}.  These linearization methods are central to our approach to Bayesian model selection.

* Curve prior model

    Methods for modeling smooth curves and surfaces have been widely studied since the early days of computer vision.  The popular active countour or "snakes" algorithm models smoothness by an energy functional penalizing discontinuities in position or higher-order derivatives \cite{asdf}.  When the energy function penalizes the second-derivative, the model becomes equivalent to Euler's "elastica" model of an ideal elastic rod, which also mimicks the classic mechanical splines used in traditional drafting and shipbuilding \cite{levien2008}.  Other spline models have been developed for different applications, including visual modelling, data interpolation (e.g. cubic splines), data smoothing (cubic smoothing splines), and visual modelling (B-splines).  In computer vision, splines provide a convenient representation for nonrigid structure and motion.  Thin-plate splines \cite{wood2003} have been applied to reconstruction of deformable surfaces \cite{schmid} \cite{mcinerney1993} \cite{perriollat2011}.

    Gaussian process (GP) theory provides an elegant probabilistic representation of continous curves and surfaces\cite{williams2006}.  As shown in \cite{wahba1990}, classic cubic smoothing splines can be reformulated as the maximum posterior curve under a particular GP prior and i.i.d. Gaussian noise.  Other GP models can acheive different types of smoothness, like simple continuity (white noise process), or \(C^\inf\) smoothness (squared-exponential covariance process).  By formulating the curve model probabilisitically, GP's can represent and propagate uncertainty in continuous curves in a principled and tractible manner .  

    Gaussian processes have been applied in computer vision for 2D category recognition \cite{kapoor2007}, 3D human pose tracking \cite{urtasun2006} \cite{wang2006},  asdf asdf asdf.  .  Brau et al. used smooth GP models as motion priors for multiple-target tracking applications \cite{brauXXX} \cite{brauXXX}.  

* Curve models
* Edge-based likelihoods / energy functions
* Thin plate splines
* Deformable models
* Sampling-based Structure From Motion
* Misc Structure from Motion
* Model-based Reconstruction
* Evaluation
    In the seminal work of Seitz et al., several multiple-view reconstruction algorithms are compared using a novel metric that 
    Evaluation of 
* Gaussian Process
* Miscellaneous

Preliminary Work
-----------------

###Data and Ground Truth Collection###

A 


data collection

likelihood + tests

Correspondence heuristic
    
    
Branching model + tests
    discrete, continuous

Temporal model + tests
    




    

Model, etc (research approach)
-------------

Proposed Work
---------------

MCMCDA

Evaluation

Leaf detection

Other datasets

Color?

Species identification




Limitations or Key Assumptions
------------------------------

Potential Outcomes, Contributions to Knowledge
-------------------------



Proposed Chapters
------------------
