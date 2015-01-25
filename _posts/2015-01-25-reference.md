---
layout: post
title: "Tree fitting - refactor"
description: ""
category: 'Reference'
tags: []
meta: 
#    "SVN Revision": 
---
{% include JB/setup %}
    % READ INPUT TREE FROM GROUND TRUTH FILE
    gt_fname = 'test_input/gt.txt';
    map1_fname = 'test_input/001_med_map.jpg';
    view1_index = 1;
    % scale and shift transform
    dx = 0.75; 
    dy = 0.25;
    scale = [diag([0.25/0.12, -0.25/0.12]) [dx*0.25/0.12; (-397+dy)*-0.25/0.12]];
    tree1 = construct_tree_from_ground_truth(gt_fname, map1_fname, view1_index, scale);

    % initialize search 
    initial_tree = tree1;
    initial_tree.pts = []; % (i.e. use prior mean)

    % load training and prior models
    likelihood = load('training_output/likelihood.mat')
    prior_params = load('training_output/prior.mat');
    pert_prior = construct_tree_perturbation_prior(tree, F, prior_params);
    % soften prior
    pert_prior.D = pert_prior.D * 36;
    % read evidence
    data_map = imread('test_input/002_med_map.jpg');
    % run fitting
    ll_temperature = 3000;
    ll_pyramid_levels = 3;
    max_iterations = 30e3;
    init_search_size = [];
    ndims = 60;
    out_tree = fit_tree_perturbation(initial_tree, likelihood, ...
                                     pert_prior, data_map,  ...
                                     ndims, ll_temperature,  ...
                                     ll_pyramid_levels, max_iterations,  ...
                                     init_search_size);
