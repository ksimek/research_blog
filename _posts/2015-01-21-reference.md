---
layout: post
title: "Fitting the Deformation Model"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}


Fitting the deformation model:
{% highlight matlab %}
  
    % pass 1: construct the decomposed prior and initial model
    [trained_prior, trained_lik_bg, trained_lik_fb] = prep_training(...)
    [tree_curves, parents, branch_distance] = ... % read from ground truth (or hack them out of prep_training)
    widths = ... % read fg probability map; threshold; construct distance transform, draw curves over it, grab widths (or hack them out of prep_training)
    F = ... % read two cameras and convert to fundamental matrix (or hack it out of prep_Training)
    fg_prob_map = imread(...) ; %(data)


    max_iterations = 500;
    temperature = 3000;
    [x_initial, mu, U, D] = test_optim(trained_prior, trained_lik_bg, trained_lik_fg, tree_curves, parents, branch_distance, widths, F, fg_prob_map, max_iterations, temperature, [], [],[],[], 200, []);

    % pass 2: do fitting

    % to combat overfitting:
    prior_temperature = 36; 

    % optional: use only first N eigenvectors
    ndims = 60;
    likelihood_scale = 3; % Third pyramid level, i.e. 1/2^(3-1) = 0.25

    [x_final] = test_optim(trained_prior, trained_lik_bg, trained_lik_fg, tree_curves, parents, branch_distance, widths, F, fg_prob_map, max_iterations, temperature, mu, Kc, U, D*prior_temperature, ndims, likelihood_scale, x_initial);

    likelihood_scale = 1; % full resolution
    [x_final] = test_optim(trained_prior, trained_lik_bg, trained_lik_fg, tree_curves, parents, branch_distance, widths, F, fg_prob_map, max_iterations, temperature, mu, Kc, U, D*prior_temperature, ndims, likelihood_scale, x_initial);

    plot_curves(mat2cell(reshape(mu + U*x_final', 2, []), 2, lengths))
{% endhighlight %}


For trained prior parameters, see [Trained Prior Parameters]({{site.baseurl}}/2015/01/11/reference/) reference post.
