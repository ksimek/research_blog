---
layout: post
title: "FIRE immunity plots"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}


Below are histograms of raw immunity readings for each marker.

TNF-\\(\alpha\\), IL-2, and IL-6 have sensible distributions.  

IL-1b and IL-10 have weirdly peaked distribution with heavy tails.  Perhaps outliers are isolated to specific plates (investigated next).

IFN and IL-8 are borderline; peaked with heavy tails but not as bad as IL-1b and IL-10.

<script>
    $(function() {
        $( "#hist_tabs" ).tabs();
    });
</script>

<div id="hist_tabs">
  <ul>
    <li><a href="#IFN">IFN-g</a></li>
    <li><a href="#TNFa">TNF-\(\alpha\)</a></li>
    <li><a href="#IL1B">IL-1b</a></li>
    <li><a href="#IL2">IL-2</a></li>
    <li><a href="#IL6">IL-6</a></li>
    <li><a href="#IL8">IL-8</a></li>
    <li><a href="#IL10">IL-10</a></li>
  </ul>
    <div id="TNFa">
        <img src="{{site.baseurl}}/img/2014-05-15-tnfa.png" />
    </div>
    <div id="IL2">
        <img src="{{site.baseurl}}/img/2014-05-15-IL2.png" />
    </div>
    <div id="IL8">
        <img src="{{site.baseurl}}/img/2014-05-15-IL8.png" />
    </div>
    <div id="IL6">
        <img src="{{site.baseurl}}/img/2014-05-15-IL6.png" />
    </div>
    <div id="IL1B">
        <img src="{{site.baseurl}}/img/2014-05-15-IL1B.png" />
    </div>
    <div id="IFN">
        <img src="{{site.baseurl}}/img/2014-05-15-IFN.png" />
    </div>
    <div id="IL10">
        <img src="{{site.baseurl}}/img/2014-05-15-IL10.png" />
    </div>
  </div>
</div>

Per-plate distributions.
----------------------------

<script>
    $(function() {
        $( "#plate_hist_tabs" ).tabs();
    });
</script>
<div id="plate_hist_tabs">
    <ul>
        <li><a href="#ifng_plates">IFN-g</a></li>
        <li><a href="#tnfa_plates">TNF-\(\alpha\)</a></li>
        <li><a href="#IL1B_plates">IL-1b</a></li>
        <li><a href="#il2_plates">IL-2</a></li>
        <li><a href="#il6_plates">IL-6</a></li>
        <li><a href="#il8_plates">IL-8</a></li>
        <li><a href="#il10_plates">IL-10</a></li>
    </ul>
    <div id="ifng_plates">
    <img src="{{site.baseurl}}/img/2014-05-15-ifng_plates.png" />
    <br />
    One of the worse plates in terms of missing/unreadable data (331/710).  Irregular between and within plates.
    </div>
    <div id="il10_plates">
    <img src="{{site.baseurl}}/img/2014-05-15-il10_plates.png" /><br />
    <p>
        Another reasonably strong variable in terms of missing data (637/710).  Plots seem somewhat irregular, but possibly due to excessible outliers in plates 10, 7, 8, 4.  This could be a good argument for a clustering/mixture model, as it might explain the heavy tails in the aforementioned plates.
    </p>

    </div>
    <div id="IL1B_plates">
    <img src="{{site.baseurl}}/img/2014-05-15-IL1B_plates.png" />
    <p>
    In terms of missing data, this variable is borderline (550/710).  Plates seem to split between (a) seemingly exponential-distrubted data (2,3,4,7,8, 10), and (b) irregular data (plates 1,5,6,9).  This could pose problems for our inference efforts.
    </p>
    <p>
    Note <em>massive</em> variation between plates.  e.g. plate 8 has a maximum at 60, while plate 1 stops at 1.3.
    </p>
    </div>

    <div id="il6_plates">
    <img src="{{site.baseurl}}/img/2014-05-15-il6_plates.png" /><br />
    <p>
    Very little missing data in this variable (699/710 observed).  Seems much more consistent than most other datasets. Scale and shape vary a bit, but no glaring inconsistencies, aside from a few outliers (e.g. plate 9).
    </p>
    <p>
    Lots of between-plate variability (e.g. plate 7 vs. 10).
    </p>
    </div>
    <div id="il8_plates">
    <img src="{{site.baseurl}}/img/2014-05-15-il8_plates.png" />
    <p>
        An excellent variable in terms of missing data (710 of 710 readings within range). The results seem very regular compared to other variables.  Seems to be Gamma-distributed or log-normal distributed but some big outliers.  Plates 5 and 10 have extreme outliers
    </p>
    </div>
    <div id="tnfa_plates">
    <img src="{{site.baseurl}}/img/2014-05-15-tnfa_plates.png" /><br />
    <p>
    The best plate in terms of missing data (710/710), TNF-\(\alpha\) seems very regular within-plates.  Note the strong gaussian shapes here, compared to the full-dataset histogram earlier.  
    </p>
    <p>
    Variation between plates is notable (see plate 5 vs. plate 8).  Supports a regularization approach.
    </p>
    </div>
    <div id="il2_plates">
    <img src="{{site.baseurl}}/img/2014-05-15-il2-plates.png" />
    <p>
    This is one of the strongest plates in terms of missing data (710 of 710 observed).  Several plates have decent gaussian distributions, albeit with heavy tails (1, 7, 9), but several are irregular (4, 5, 8, 9), and others look more exponential (2, 3, 10). 
    </p>
    </div>
</div>
