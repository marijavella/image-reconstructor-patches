Image Reconstructor (from Patches)
============================================================
[![Build Status](https://travis-ci.org/marijavella/image-reconstructor-patches.svg?branch=master)](https://github.com/marijavella/image-reconstructor-patches)

Python code to reconstruct images from patches with a specified patch size/stride combination.  The patches are combined by averaging, making this useful when reconstructing an image from imperfect patches generated from a neural network.  

This code is more flexible than the [`Scikit`](https://scikit-learn.org/stable/) [`reconstruct_from_patches_2d`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.image.reconstruct_from_patches_2d.html) function since it can work with any stride value.

Contents
--------

The `patch_reconstructor` package contains the following functions within `recon_from_patches.py`:

* `recon_im`: Reconstructs an image from an array of patches with a specified stride and patch size.  Overlapping areas are resolved by averaging. 

* `get_patches`: Extracts overlapping patches (square) of a specified size and stride from an input image.  This is a demo function used to prove the functionality of the `recon_im` function.

Installation 
------------
Activate your preferred Python (3.x) environment and run the following command from the repo home directory:

`pip install .`

`Numpy` is the only dependency for this package.

Usage
-----
You can use this function directly in Python after installation by first importing it using the following statement:

`from patch_reconstructor.recon_from_patches import recon_im`

Then, the actual reconstruction function (`recon_im`) can be called with the following parameters:

`recon_im(patches: np.ndarray, im_h: int, im_w: int, n_channels: int, stride: int)`

    patches: 4D ndarray with shape (patch_number,patch_height,patch_width,channels)
        Array containing extracted patches. If the patches contain colour information,
        channels are indexed along the last dimension: RGB patches would
        have `n_channels=3`.
    im_h: int
        original height of image to be reconstructed
    im_w: int
        original width of image to be reconstructed
    n_channels: int
        number of channels the image has. For  RGB image, n_channels = 3
    stride: int
           desired patch stride

Demo
----
To execute a short demo run the following commands from the repo home directory:

1. `pip install -r requirements.txt` (adds [`pillow`](https://pillow.readthedocs.io/en/stable/), [`click`](https://click.palletsprojects.com/en/7.x/) and [`matplotlib`](https://matplotlib.org) for graphing functionalities)
2. `pip install .`
2. `python demo.py samples/baboon.bmp`

The demo will produce an image showing the patching and reconstruction process.  The image, stride and patch size can be adjusted as required.

Further Development
-------------------
Open to suggestions/improvements.






