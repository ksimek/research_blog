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

    Reconstructing 3D models from multiple images is a central area of computer vision.   Laurentini proposed an early algorithm for constructing what he called the "visual hull", the largest closed 3D mesh whose projection is consistent with silhouettes in multiple images \cite{Laurentini1994}.  Laurentini's method assumed the use could obtain high-quality foregorund, background segmentation, with minimial noise.  Other approaches achieve better robustness by using a voxel representation, and they reconstruct using a Hough transform-based vote-counting method \cite{TODO}.  These methods are effective at suppressing structure arising from noisy pixels, but as they are still essentially an intersection-based method, can omit 3D structure when intersection doesn't occur, for example in the presence of slightly miscalibrated cameras.  This shortcoming is particularly noticible when reconstructing thin structure, when most or all of the structure can be absent.  Some approaches have attempted to work around this shortcoming \cite{CVPR2013 paper}, but TODO: shortcoming.   Our approach sidesteps the intersection issue entirely by explicitly modelling the perturbations that cause failed intersections to occur.

* Tracking
* Bayesian Model Choice
* Curve models
* Edge-based likelihoods / energy functions
* Thin plate splines
* Deformable models
* Sampling-based Structure From Motion
* Misc Structure from Motion
* Model-based Reconstruction
* Evaluation
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
