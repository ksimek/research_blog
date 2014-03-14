---
layout: post
title: "iPlant Literature Review Planning Meetings"
description: ""
category: 'Meeting Notes'
tags: []
---
{% include JB/setup %}

Document discussion
------------------

Some random notes about issues to bring up in the final document.


Talk about representation vs. "features" (characteristics).  Clarify "features", don't use indescriminitively (call them high-level features, topological features, as opposed to image features).

Two ways to go about finding "features":

* "look directly for charactersitics/features"
* "look for model, find the other stuff"

i.e. looking for representations vs. characteristics

Bisque vs. Nonbisque?  Unclear what the final application will be, but if Bisque is the goal, some discussion of it's feasibility is probably warranted.  For example, interactive systems like the Clark paper might not be feasible for Bisque.

Taxonomy of curve-extraction methods
-----------------------------
Kobus mentioned the different "dimensions"  that the problem can be split into.  Some might be

* 3D vs 2D  
* imaging system type (microscope, MRI, camera, etc)
* temporal vs. nontemporal
* branching vs non branching
* biological vs. nonbiological

Research Topics
-----------

We can split the background reading into several areas, both in image processing/CV and biological application.
Kobus recommended splitting time between these broad areas.

*Image Processing Topics*

* "snakes" - active contours
* Medial axis filtering
* curve modelling (polynomial/splines, GP, level-set methods)
* finding branches

*Application Areas*

* pollen tube tracking
* root tracking
* Blood vessel literature / vascular segmentation
* Neuron tracing
* Alternaria / Fungus? 



Other stuff
-------
Other topics that might be worth looking into, but maybe of speculative value.

* Rhizotron - nondestructive underground root imaging system 

Data Inventory 
---------------
We currently have data sets from a handful of different applications/domains.

* Pollen tubes
* "Clark" root image (2D, one image)
* "Max Plank" root images 
* Neurons

Next steps
---------

Any questions for Martha?

Reading for next week: look into citations from Clark and Hypotrace

* Kate - related work, Clark Paper
* Andrew - related work, Hypotrace paper
* Kyle image processing

As we read, lets try to place each paper somewhere in the "Taxonomy" above.
        

