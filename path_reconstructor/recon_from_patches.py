#  Test on image patches
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as pil_image

def recon_im(patches, im_h, im_w, n_channels, stride, patch_size):
    """Reconstruct the image from all patches.
        Patches are assumed to be square and overlapping depending on the stride. The image is constructed
         by filling in the patches from left to right, top to bottom, averaging the overlapping parts.

    Parameters
    -----------
    patches : array
        Array containing extracted patches. If the patches contain colour information,
        channels are indexed along the last dimension: RGB patches would
        have `n_channels=3`.
    im_h: int
        height of image to be reconstructed
    im_w: int
        width of image to be reconstructed
    n_channels: int
        number of channels the image has. For  RGB image, n_channels = 3
    stride : int
           desired patch stride
    patch_size : int
               patch size

    Returns
     -----------
     reconstructedim : ndarray
                     Reconstructed image from the given patches
    """

    rows = ((im_h - patch_size) // stride) * stride + patch_size
    cols = ((im_w - patch_size) // stride) * stride + patch_size

    if n_channels == 1:
        reconim = np.zeros((rows, cols))
        temp = np.zeros((rows, cols))
    else:
        reconim = np.zeros((rows, cols, n_channels))
        temp = np.zeros((rows, cols, n_channels))
    p_r = (rows - patch_size + stride)/stride
    p_c = (cols - patch_size + stride)/stride
    totpatches = patches.shape[0]
    initr, initc, start, num = 0, 0, 0, 0
    templabels = patches

    end = totpatches + start
    templabels = templabels[start:end]

    # extract each patch and place in the zero matrix and sum it with existing pixel values
    k = 1
    reconim[initr:patch_size, initc:patch_size] = templabels[0]
    while k <= len(templabels) - 1:
        initc = initc + stride
        temp[initr:initr + patch_size, initc:patch_size + initc] = templabels[k]
        total = np.add(reconim, temp)
        reconim = total
        if n_channels == 1:
            temp = np.zeros((rows, cols))
        else:
            temp = np.zeros((rows, cols, n_channels))
        temp = np.squeeze(temp)
        elements = len(range(-1, k))


        if np.remainder(elements, p_c) == 0 and k < len(templabels) - 1:
            initr = initr + stride
            initc = 0
            temp[initr:initr + patch_size, initc:patch_size] = templabels[k + 1]
            total = np.add(reconim, temp)
            reconim = total
            k += 1
        k += 1

    # Average overlapping pixels by adding one to overlapping positions

    if n_channels == 1:
        divim = np.zeros((rows, cols))
        tempdiv = np.zeros((rows, cols))
    else:
        divim = np.zeros((rows, cols, n_channels))
        tempdiv = np.zeros((rows, cols, n_channels))

    initr = 0
    initc = 0
    divim[initr:patch_size, initc:patch_size] = np.ones(templabels[0].shape)

    k = 1
    while k <= len(templabels) - 1:
        initc = initc + stride
        tempdiv[initr:initr + patch_size, initc:patch_size + initc] = np.ones(templabels[k].shape)
        totaloverlap = np.add(divim, tempdiv)
        divim = totaloverlap
        tempdiv = np.zeros((rows, cols, n_channels))
        if n_channels == 1:
            tempdiv = np.zeros((rows, cols))
        elements = len(range(-1, k))

        if np.remainder(elements, p_c) == 0 and k < len(templabels) - 1:
            initr = initr + stride
            initc = 0
            tempdiv[initr:initr + patch_size, initc:patch_size] = np.ones(templabels[k].shape)
            totaloverlap = np.add(divim, tempdiv)
            divim = totaloverlap
            k += 1
        k += 1

    # Average out pixel values
    reconstructedim = reconim / divim
    return reconstructedim


def get_patches(GT, stride, patch_size):
    """Extracts square patches from an image of any size.
    Parameters
    -----------
    GT : ndarray
        n-dimensional array containing the image from which patches are to be extracted
    stride : int
           desired patch stride
    patch_size : int
               patch size
    Returns
    -----------
    patches: ndarray
            array containing all patches
    im_h: int
        height of image to be reconstructed
    im_w: int
        width of image to be reconstructed
    n_channels: int
        number of channels the image has. For  RGB image, n_channels = 3
    """

    hr_patches = []

    for i in range(0, GT.shape[0] - patch_size + 1, stride):
        for j in range(0, GT.shape[1] - patch_size + 1, stride):
            hr_patches.append(GT[i:i + patch_size, j:j + patch_size])

    im_h, im_w  = GT.shape[0], GT.shape[1]

    if len(GT.shape) == 2:
        n_channels = 1
    else:
        n_channels = GT.shape[2]

    patches = np.asarray(hr_patches)

    return patches, im_h, im_w, n_channels
