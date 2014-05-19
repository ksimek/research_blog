---
layout: post
title: "FIRE - immunity data transformations"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}

this is a follow-up to [this earlier post], in which immunity data is plotted as histograms for each "plate".

After log-transforming the variables the extreme outliers now look more sensible, and the distributions are far more symmetric, with the exception of a few TNF-\\(alpha\\) plates.
    

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
    <img src="{{site.baseurl}}/img/2014-05-18-ifng_plates.png" />
    </div>
    <div id="il10_plates">
    <img src="{{site.baseurl}}/img/2014-05-18-il10_plates.png" /><br />
    </div>
    <div id="IL1B_plates">
    <img src="{{site.baseurl}}/img/2014-05-18-il1b_plates.png" />
    </div>
    <div id="il6_plates">
    <img src="{{site.baseurl}}/img/2014-05-18-il6_plates.png" /><br />
    </div>
    <div id="il8_plates">
    <img src="{{site.baseurl}}/img/2014-05-18-il8_plates.png" />
    </div>
    <div id="tnfa_plates">
    <img src="{{site.baseurl}}/img/2014-05-18-tnfa_plates.png" /><br />
    </div>
    <div id="il2_plates">
    <img src="{{site.baseurl}}/img/2014-05-18-il2_plates.png" />
    </div>
</div>
