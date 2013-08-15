---
layout: post
title: "Dissecting the Camera Matrix, Part 3: The Intrinsic Matrix"
description: ""
category: 
tags: []
---
{% include JB/setup %}
{% include research/tulips_da2_meta %}

Earlier we studied the extrinsic camera matrix, and examined three different interpretations of its parameters.  Today I'll demonstrate two equivalent interpretations of the camera matrix.  First, we'll see how the camera parameters correspond the geometry of real physical camera.  Then I'll show how each of the intrinsic parameters corresponds to a simple 2D transform.  Finally,  give a 3D demo illustrating both interpretations

This is an entry in the series "Camera matrix, an interactive tour."  To read the other entries in the series, see the table of contents, here. (TODO)

The intrinsic matrix is:
    
    ** EQUATION HERE **

We usually interpret the intrinsic matrix as a transformation from 3D non-homogeneous camera coordinates to 2D homogeneous image coordinates by projecting onto the image plane.  I call this the "camera-centric" interpretation of the intrinsic matrix, where each of the parameters represents a physical aspect of our pinhole camera's geometry:
    
* **Focal length**: \\(f_x\\), \\(f_y\\) - The distance between the pinhole and the image plane (in pixels; all intrinsic values are measured in pixels -- more on this later).
* **Principal Point Offset**: \\(x_0\\), \\(y_0\\) - The position of pinhole's projection onto the camera's film, relative to the film's origin.  This projection is called the "principal point", and the line from the principal point through the pinhole is called the "principal axis".  Increasing \\(x_0\\) by 10 shifts the pinhole right by 10 pixels, or equivalently, shifts the film left by 10 pixels.
* **Axis skew**: \\(s\\) - As far as I know, there isn't any analogue for this in a traditional camera, but [apparently some digitization processes can cause nonzero skew](http://www.epixea.com/research/multi-view-coding-thesisse8.html#x13-320002.2.1).

At first glance, it seems like these 5 parameters couldn't completely describe the pinhole camera.  The focal length and principal point offset amount to simple translations of the film in space.  There must be other ways to transform the film relative to the pinhole, for example, rotation or scaling, right?  Lets address these one-by-one.

First we'll consider rotations of the film around the principal axis.  This is traightforward:  this is handled in the extrinsic matrix's rotation parameters (as the "roll" parameter if you're using a pitch-yaw-roll formulation).

What about other rotations that cause the film to be non-perpendicular to the pinhole?  This question is a bit ill-posed, because it assumes the pinhole has an orientation.  In truth, the pinhole in our camera model doesn't care what "direction" the camera is pointing -- light passes through it in all directions.  The orientation of the camera is defined by the film's orientation, which (again) is handled in the extrinsic camera matrix.  If the film is rotated around a point not lying on the prinpical axis, it will also result in changes to the focal length and principal point, too.

What if the film doubles in size, but stays in the same position?  This scenario changes the clipping bounds of the image, which isn't actually modelled by the intrinsic matrix.  In graphics systems like OpenGL, this is modelled by adding an extra orthographic projection after the intrinsic matrix is applied, which maps image coordinates to Normalized Device Coordinates.  This is described in more detail in my post on [calibrated cameras in OpenGL]({{site.baseurl}}/2013/06/03/calibrated_cameras_in_opengl/).  


Why are values measured in pixels?

Imagine doubling all the physical dimensions of your pinhole camera: the film size and the focal length.  The resulting image would be unchanged (assuming the film's resolution remains constant).  The intrinsic matrix is only concerned with how points in 3d space are projected into pixel coordinates, and thus, it only represents relative dimensions.  The transformation is invariant to scaling of the camera dimensions; by representing dimensions in pixel units, we naturally capture this invariance.  

If you know the size of your film (or digital sensor) in world units, you can convert focal length from pixels to world units.  If \\(w\\) is the width of the image in pixels, \\(W\\) is the width in world units, and the focal length in pixels is \\(f_x\\), you can use similar triangles to find the focal length in world units \\(F_x\\):
        
<div> F_x = f_x * \frac{W_x}{w_x} </div>

Other parameters \\(f_x\\), \\(x_0\\), and \\(y_0\\) can be found in a similar way.  

Intrinsic parameters as 2D transformations

If we instead interpret our 3-vectors not as 3D image coordinates but as 2D homogeneous coordinates, we can come to an alternative interpretation of the intrinsic matrix: as a sequence of 2D affine transformations.  We can decompose the intrinsic matrix into the product of a scaling, translation, and shear amtrix, corresponding to focal length, principal point offset, and axis skew, respectively:
    
    TODO: equation here

This interpretation implies that the intrinsic camera transformation occurs *post-projection*.  One notable result of this is that intrinsic parameters cannot affect visiblity -- occluded objects cannot be revealed by simple 2D transformations in image space.

Full decomposition

We can now combine our decomposed intrinsic matrix with the extrinsic matrix decomposition we studied last time.  The result shows the sequence of five affine transformations that make up the complete camera matrix: (1) 3D rotation, (2) 3D translation, (3) 2D scaling, (4) 2D translation, and finally (5) 2D shear.  
    
TODO EQUATION HERE

Demo 

The demo below illustrates both interpretations of the intrinsic matrix.  The left pane represents the "camera-geometry" interpretation.  The yellow plane indicates the "virtual" image plane, but for all intents and purposes, represents the "film" of the pinhole camera.  Notice how the pinhole move relative to the image plane as \\(x_0\\) and \\(y_0\\) are adjusted.

The right pane represents the "2D transformation" interpretation.  Notice how changing focal length results in scaling of the projected image, and principal point results in pure translation.  Also note that since translation occurs *after* scaling, larger focal lengths will result in larger translations as \\(x_0\\) and \\(y_0\\) are adjusted.

    TODO: demo here

