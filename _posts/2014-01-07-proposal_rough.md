---
layout: post
title: "Roughing out Proposal"
description: ""
category: 'Work Log'
tags: []
---
{% include JB/setup %}

Simultaneous stereo and tracking of nonrigid structure for semantic reconstruction

Summary
----------

Problem statement
-------------------

We have collected a dataset consisting of multiple specimens of Arabidopsis Thaliana, imaged at several angles.  Specimens come from two different genetic strains, and imaging occurred at various stages of development.  The elapsed time between the first and last image is several minutes, and in many cases, plants exhibit noticible motion between the first and last image.  Our primary goal is to recover the full 3D branching structure of each specimen, but we also seek to recover the motion between frames as it may contain useful phenotype information.  Our reconstrution will be composed of geometric primitives, from which plant scientists may extract valuable phenotype traits like branch angle and curvature.

In a sense, our problem encompasses two complementary areas in computer vision, tracking and multi-view stereo.  In classical tracking, the camera is fixed and the goal is to recover motion; in stereo, the camera is moving and the goal is to recover the fixed structure.  In our problem, both structure and camera undergo motion, with each object's motion confounding inference of the other.  Is an object's 2D motion best explained by parallax or by motion in 3D?   Either of these conclusions (or both) could the case; underconstrained problems like these require additional assumptions to be solved uniquely.  We a Bayesian approach to the problem, encoding these assumptions in the form of a prior distribution over structure and motion, and using Bayesian inference to recover both the optimal solution and a distribution over alternative solutions.  

Phenotype traits:
* branch depth,
* branch angles,
* stem curvature,
* torsion,
* phototropism,
* interbranch distances,
* biomass,
* etc.


In modelling branching stem structures, we propose a representation that is simultaneously expressive and tractible.

(The following might be best posed in related work, after describing SfM and SfS backgroun)

In addition to the difficulties interent to simultaneous inference of structure and motion, the nature of plant structure poses specific challenges to the reconstruction task.  Our primary structures of interest are plant stems, which are nearly absent of texture features.  Most structure-from-motion algorithms use so-called keypoints to find matches between images, and high quality keypoints cannot be found without strong texture features.   The thin geometry of plant stems also poses difficulties, especially with popular shape-from-silhouette algorithms.  The thin backprojection cones that arise from stems often fail to intersect, because cameras are imperfectly calibrated and stems undergo motion between views.  Algorithms exist to improve camera pose estimates by minimizing reconstruction error, but these algorithms assume structure is stationary.  

Plant structure also poses challenges on the on the tracking side, 

      * nonrigid/nonparametric structure
      * nonrigid motion

Modelling challenges
      * unknown topology, cardinality
      
the primary difficulty is that the object and camera move simultaneously.  Since our goal is 3D tracking, 


**By jointly modeling camera error, 3D spatial structure, and temporal motion, we seek to improve upon existing approaches that ignore one or more of these aspects, while providing a rich description of the 4D scene.**

We propose a Bayesian 




Model camera, structure, motion directly


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


*PMVS first attempt*

    The well-known patch-based multiple view stereo algorithm (PMVS) uses full-color images to reconstruct a 3D mesh \cite{furukawa2010}, making them effective when a silhouette is unavailable.  For each image patch, a similar image patch is sought in other views such that both appearance and depth are roughly consistent between matches.  However, due to ambiguities that arise in flat image regionts, the algorithm starts by matching special keypoints whose surface exhibit distinct texture, and filling-in patches in-between.  In our situation, our surfaces are extremely thin (often three pixels or fewer in width) and exhibit no notable texture features, causing patch-based reconstructions to fail.  Further, PMVS assumes rigid structure and perfectly calibrated cameras; our plant's slight movements and our miscalibrated cameras would likely cause the algorithm's consistency checks to fail.

*PMVS Second attempt*

    The well known asdfjl;kj uses appearance consistency to estimate the depth of image patches.  It relies heavilly on texture data to find inital matches, which makes it ineffective at reconstructing textureless structure like plant stems.  Futhermore, like the visual-hull based methods, our miscalibrated cameras and slightly moving plant structure would cause the consistency checks in this algorithm to fail.

* Tracking
* Bayesian Model Choice


* Curve prior model

    Methods for modeling smooth curves and surfaces have been widely studied since the early days of computer vision.  The popular active countour or "snakes" algorithm models smoothness by an energy functional penalizing discontinuities in position or higher-order derivatives \cite{asdf}.  When the energy function penalizes the second-derivative, the model becomes equivalent to Euler's "elastica" model of an ideal elastic rod, which also mimicks the classic mechanical splines used in traditional drafting and shipbuilding \cite{levien2008}.  Other spline models have been developed for different applications, including visual modelling, data interpolation (e.g. cubic splines), data smoothing (cubic smoothing splines), and visual modelling (B-splines).  In computer vision, splines provide a convenient representation for nonrigid structure and motion.  Thin-plate splines \cite{wood2003} have been applied to reconstruction of deformable surfaces \cite{schmid} \cite{mcinerney1993} \cite{perriollat2011}.

    Gaussian process (GP) theory provides an elegant probabilistic representation of continous curves and surfaces\cite{williams2006}.  As shown in \cite{wahba1990}, classic cubic smoothing splines can be reformulated as the maximum posterior curve under a particular GP prior and i.i.d. Gaussian noise.  Other GP models can acheive different types of smoothness, like simple continuity (white noise process), or \(C^\inf\) smoothness (squared-exponential covariance process).  By formulating the curve model probabilisitically, GP's can represent and propagate uncertainty in continuous curves in a principled and tractible manner .  


* Curve models
* Edge-based likelihoods / energy functions
* Thin plate splines
* Deformable models
* Sampling-based Structure From Motion
* Misc Structure from Motion
* Model-based Reconstruction
* Evaluation
    Middlebury metric.
    Evaluation of 
* Gaussian Process
* Miscellaneous


    



Limitations or Key Assumptions
------------------------------

foliage doesn't significantly obscure branching structure.



Potential Outcomes, Contributions to Knowledge
-------------------------



Proposed Chapters
------------------

TODO
---
* We model stems as a set of points along the medial axis of a tube with circular cross-sections.
