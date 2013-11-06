---
title: "CVPR 2014 Summary"
layout: page
---

Summary of completed work, work to be done.

Summary 
-----------
* Developed analytical methods for marginalization/maximization that working with rank-deficient precision matrices.
* Improved inference of index-set
* Trained model
* Attachment functionality
* **Developed per-view model** (temporal model)
* Re-formulated attachment in terms of GP kernel, instead of a matrix operation* **Incorporated non-gaussian pixel model (opengl silhouette rendering, CUDA)**
* revived, refactored old silhouette rendering code, blurred-difference edge likelihood code
* Fixed errors in ground-truth, finished incomplete ground-truth
* Ran reconstruction on all ground-truth

TODO
------

* Address [problems with ground-truth reconstruction]({{site.baseurl}}/2013/09/30/work-log/)
* Improve 2nd likelihood speed.
* End-to-end sampling 
    * Add new likelihood
    * Split/merge
    * Idea: bias using foreground/background pixel probabilities
* Evaluation
* Find 2nd Dataset (neurons?)
* Add boost_system to KJB build system
* Handle non-constant curve widths

