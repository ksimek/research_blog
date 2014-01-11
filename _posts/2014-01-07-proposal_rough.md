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

With recent developments in high-throughput genotyping, it has become relatively easy to extract ana analyze entire plant genomes.  

a wealth of data has emerged describing 

In order to understand the complex relationship between genotypes and phenotypes, researchers 

By understanding the complex relationship between genotype and phenotype, researchers can better understand the genetic components to practical issues 

The complex relationship between genetic variation and plant traits like drought resistance and crop yields remains a topic of active study.  
Relationship between a plant's genotype (hereditary information) and phenotype (observable properties).


One major impediment to progress is the gap between the success of high-throughput genotyping methods have provided a wealth of genetic information, while much phenotyping remains manual an painstaking

new interest in image-based phenotyping
    upsides
        inexpensive cameras
        precise measurement
        minimal invaseveness
    downsides
        human interaction
        dataset dependent
        largely 2D
            no 3d angle, torsion, bushiness, 

We propose a method for reconstructing 3D 

Computer vision techniques for 3D reconstruction
    


We seek a system that will construct a full 3D model of a plant from a images at several angles.  
We seek to construct a system for high-throughput 3D 

Problem statement
-------------------

We have collected a dataset consisting of multiple specimens of Arabidopsis Thaliana, imaged at several angles.  Specimens come from two different genetic strains, and imaging occurred at various stages of development.  The elapsed time between the first and last image is several minutes, and in many cases, plants exhibit noticible motion between the first and last image.  Our primary goal is to recover the full 3D branching structure of each specimen, but we also seek to recover the motion between frames as it may contain useful phenotype information.  Our reconstrution will be composed of geometric primitives, from which plant scientists may extract valuable phenotype traits like branch angle and curvature.

In a sense, our problem encompasses two complementary areas in computer vision, tracking and multi-view stereo.  In classical tracking, the camera is fixed and the goal is to recover motion; in stereo, the camera is moving and the goal is to recover the fixed structure.  In our problem, both structure and camera undergo motion, with each object's motion confounding inference of the other.  Is an object's 2D motion best explained by parallax or by motion in 3D?   Either of these conclusions (or both) could the case; underconstrained problems like these require additional assumptions to be solved uniquely.  We propose encoding these assumptions in the form of a prior distribution over structure and motion, and using Bayesian inference to recover both the optimal solution and a distribution over alternative solutions.  

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
    Middlebury metric.
    Evaluation of 
* Gaussian Process
* Miscellaneous

Preliminary Work
-----------------

###Data and Ground Truth Collection###

####Image Collection####

We have collected 36-view turntable images of 23 Arabidopsis specimens, each with an accompnying camera calibration image set.  For one of these specimens, we collected time-lapse images at 10 time-points spanning 12 days; other specimens were collected at only one time-point.  Nine specimens were deemed unusable either due to either poor image quality or the lack of relevant structure, leaving 14 total specimens.

####Ground Truth Collection####

We developed software in Matlab for semi-manual camera calibration and used it to calibrate cameras for all datasets.  Due to imperfections in both the calibration target and during the calibration procedure, camera calibrations contain minor errors, which our algorithm will be designed to be robust to.   

We also developed a GUI tool in C++/OpenGL for manual tracing of plant stems in 2D.  2D ground-truth is collected by drawing Bezier curves on each stem, and establishing correspondences of stems between views.  In addition, curve topology is collected by specifying each curve's parent.   We have collected 2D ground-truth for every fourth view in 11 of the 14 valid specimens, for a total of 44 fully annotated images.  In order to evaluate the quality of our algorithm's 3D reconstruction, we have developed an initial prototype that will triangulate 2D tracings into 3D, which will be used for our evaluation metrics.

####Branching Model####

We have developed a Gaussian process model to represent smooth curves arranged in a tree topology.  Within curves, the Gaussian process allows us to model continuous curves in a general way, while enforcing smoothness.  Between curves, we have adapted the traditional GP model to enforce connectivity constraints while retaining the linear-Gaussian property that enables tractibility.  

The branching Gaussian process's covariance function takes the form of a recursive function: 
    
    k(x_i,x_j) = \delta_{c_ic_j} k_\text{within}(x_i, x_j) + k_\text{inherited}(x_i, x_j)

where \(c_k\) is the index of the curve associated with index \(x_k\). Without loss of generality, assume \(c_a < c_b\) implies curve \(c_a\)'s topological depth is no greater than that of \(c_b\), and \(c_a = 1\) denotes the root curve.  The \(k_\text{within}\) implements a smooth-curve Gaussian process that contrains the initial point to be at the origin.  The recursive term \(k_\text{inherited}\) implements a constant offset for each curve, causing curves to initiate from the branch point of their parent curve.      

    k_\text{inherited}(x_i, x_j) = 
    \begin{cases}
        k_\text{inherited}(x_j, x_i) & \text{if } c_i > c_j \\
        \sigma_o^2 & \text{if } c_j = 1 \\
        k(x_i, b(x_j)) & \text{otherwise}
    \end{cases}

 Here, \b(x_k\) denotes the index of the branch point on the parent curve.  Note that if \(c_i \le c_j\), then \(k_\text{inherited}\) is constant with respect to \(x_j\).   Thus, each point on a curve inherits a constant covariance from the branch point on its parent.   Here, \(sigma_o\) is the root offset variance.  (Memoization can be used to compute each entry in the covariance matrix in amortize constant time.) 

####Temporal model####

To accomodate motion between views, we generalize the branching Gaussian process covariance function to include a temporal term.  We first replace spacial index \(x_i\) with the ordered pair \((x_i, t_i)\), where \(t_i\) is the temporal index associated with a particular view.  The covariance function for the temporal branching Gaussian process is then

    k\left((x_i, t_i), (x_j, t_j) \right) = k_\mu(x_i, x_j) + f(t_i, t_j) k_\delta(x_i, x_j)

where \(k_\mu\) and \(k_\delta\) are both branching Gaussian process covariance functions, but with different metaparameters.  \(k_\mu\) models the mean process, while \(k_\delta\) models perturbations from the mean over time.  The temporal covariance function \(f\) modulates the perturbation based on temporal locality.  We have experimented with several possible choices for \(f\), and have found the Ornstein-Uhlenbeck process to be effective:
    
    f(t_i, t_j) = \exp\{-|t_i - t_j|/l_t \}

This covariance is similar to white-noise, but with a tendency to revert to the mean over time.  This places few constraints on the shape of the motion, aside from it being continuous and not drifting too far from the general shape defined by \(k_\mu\).  Note that for any value of f(), \(k()\) becomes is the sum of two branching Gaussian processes, which is itself a branching Gaussian process.  For any particular point, its self-covariance over time is greatest when \(|t_i - t_j| = 0\), with correlation weakening as indices become more separated in time.  In the limit, the covariance of the second term becomes zero, leaving only the mean process \(k_\mu\) remaining, indicating the views are independence conditioned on the mean structure.

Laplace approximation

TODO: this isn't Laplace per-se, but Taylor-series approximation that exploits the independence of 

We model the log-likelihood as the negative sum of squared reprojection error.

TODO: EQUATION HERE
 
While our GP prior distribution is Gaussian, this image likelihood function involves nonlinear perspective projection, causing the posterior to have nonlinear form.  In general, maximization of nonlinear functions is inefficient in high dimensions and marginalization of such functions is intractible, even with numerical approximations.  Our 3D reconstruction method will require both of these operations, so we seek an approximation that permits efficient inference.

As shown in figure XXXa, the likelihood for an individual point forms a cone-shaped isosurface.  We observe that if the true posterior is sufficiently peaked, the shape of the point-likelihood is irrelevant in regions with low posterior support.  Thus, we can replace the true likelihood with a denerate Gaussian function, which has cylindrical-shaped isosurfaces.  As shown in figure XXXc, the maximum relevant error is small if the point's angular size is small and the posterior is peaked.  The former condition holds if the point is reasonably far from camera, and the latter holds if there are multiple views of the scene.  

The smoothness prior acts to resolve the one-dimensional ambiguity in the point-wise likelihood, by sharing position information between nearby views. The resulting posterior is a non-degenerate Gaussian distribution.

We have implemented maximum a-posteriori 3D reconstruction of 2D ground-truth data, and initial results are promising (see figure XXX).  Ultimately, we plan on 

####Extending to general likelihood functions####

Often additional evidence is available in the form of non-linear likelihood functions that aren't well approximated by a Gaussian.  Many functions over pixel maps fall into this category, for example intensity-, silhouette-, texture-, or edge-based likelihood functions \cite{TODO}.   We have developed a sampling approach for approximate inference in these scenarios, using the Gaussian posterior we developed in the previous section as a proposal distribution.

Consider the case of marginalizing over 3D reconstructions.  Let \(\theta\) be the 3D point positions, \(D_1\) be the corresponding observed points in 2D, and \(D_2\) be arbitrary additional evidence.  Assuming \(D_1\) and \(D_2\) are conditionally independent given \(\theta\), the marginal likelihood is given by

    p(D_1, D_2) = \int p(\theta) p(D_1 | \theta) p(D_2 | \theta) d\theta

We can exploit the linear-Gaussian form of the partial-data posterior, \(p(\theta | D_1)\), to perform Monte-Carlo intergration of the full posterior:

    p(D_1, D_2) = \int p(\theta | D_1) p(D_1) p(D_2 | \theta) d\theta \\
                = p(D_1) \int p(\theta | D_1) p(D_2 | \theta) d\theta \\
                \approx p(D_1) \sum_\theta^{(i)} p(D_2 | \theta^{(i)}) 

where \(\{\theta^{(i)}\}_i\) are i.i.d. samples from \(p(\theta | D_1)\).  The number of smaples needed for a good approximation is problem-specific.  However, in many cases, \(p(\theta | D_1)\) is strongly peaked in a region where \(p(D_2 |\ \theta)\) is relatively constant, and a single sample is sufficient for a good approximation.

Maximum \it{a posteriori} inference of \(\theta\) can be performed by replacing the sum operation with an argmax operation.  Thus, arbitrary nonlinear likelihoods can be incorporated into our modelling framework, without sacrificing tractibility of approximate inference.

###Likelihoods###

-- non-rigid, self-intersecting silhouette rendering (with figure)
-- GPU likelihood function



###Correspondence heuristic###
    
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

foliage doesn't significantly obscure branching structure.



Potential Outcomes, Contributions to Knowledge
-------------------------



Proposed Chapters
------------------

TODO
---
* We model stems as a set of points along the medial axis of a tube with circular cross-sections.
