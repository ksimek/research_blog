---
layout: page
title: "TULIPS Project"
description: ""
---
{% include JB/setup %}

<div class="project-preamble">
<table>
    <tr>
    <th>Project</th>
    <td><a href="{{site.baseurl}}/projects/tulips.html">Tulips</a></td>
    </tr>
    <tr>
    <th>SVN path</th>
    <td>/projects/tulips/trunk/</td>
    </tr>
</table>
</div>

The TULIPS project is an effort to reconstruct 3D models of biological structure from images.  We follow a Bayesian generative modelling approach, in which the model generates 3D structure, which is projected and rendered using a camera model.  A likelihood function compares the result against camera data.  

The project originated with Joseph Schelcht's work on reconstructing fungus from microscopic image stacks.  Currently we are focusing on reconstructing branching plants using calibrated cameras.

Related Areas
----------------

* L-Systems
* Chamfer Matching
* Camera calibration
* Reversible Jump Markov Chain Monte Carlo
* Multiple-view reconstruction, Epipolar Geometry
* Chamfer-transform edge likelihood
* GPU-based edge metrics
* Branching Gaussian Processes

Etymology
------------------
Once upon a time, the TULIPS project stood for "Training and Unsupervised Learning and Inference of Plant Structure".

Though it made for a nice acronym, it was little more than a random collection of buzz-words that mostly fit.  Most problematic was the "Unsupervised" part, since our approach falls squarely into the category "supervised learning."  

Since the acronym is sooooo close to fitting, I've been looking on a better [backronym](http://wikipedia.org/wiki/backronym). 

One possibility is "Totally Uninvasive Learning and Inference of Plant Structure," which nicely describes a major benefit of the project, namely that plants don't need to be dissected in order to to be studied.  But "totally" is kind of a dumb word, and "uninvasive" isn't a word at all (see "[noninvasive](http://dictionary.reference.com/browse/noninvasive)").  Moving on...

We can punt on the 'T' and just use a [recursive acronym](http://en.wikipedia.org/wiki/Recursive_acronym), so that just leaves the 'U'.

My current favorite is "Tulips Utility for Learning and Inference of Plant Structure."  

Have a better suggestion?  [Drop me a line]({{ site.baseurl }}/contact.html)!

