---
layout: post
title: "Branching ML Done"
description: 
category: "TODO"
tags: []
meta: 
    "SVN Revision": 15229
---
{% include JB/setup %}
{% include research/tulips_da3_meta %}

Finally finished implementing and confirming the multi-view branching ML.  Next steps:

Quick

* re-run tests with non-zero start index
* test three-levels of branching
    * reconstruction
    * ML vs. reference
* cleanup Corr fields
    * eliminate clean_ fields
    * group fields by processing stage 
* map-out processing pipeline

Medium

* finish ground-truthing (Friday night, Saturday)
* implement recursive update
* code for inferring branching parameters.
* Finish training
    * infer branching parameters
    * re-write training ML
    * re-train prior parameters with full ML
        * jointly train FG and BG using same 
* gibbs sampler
* evaluation code

Reach

* split-merge moves

