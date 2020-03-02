import numpy as np


def recon_im(patches: np.ndarray, im_h: int, im_w: int, n_channels: int, stride: int):
    """Reconstruct the image from all patches.
        Patches are assumed to be square and overlapping depending on the stride. The image is constructed
         by filling in the patches from left to right, top to bottom, averaging the overlapping parts.

    Parameters
    -----------
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

    Returns
    -----------
    reconstructedim: ndarray with shape (height, width, channels)
                      or ndarray with shape (height, width) if output image only has one channel
                    Reconstructed image from the given patches
    """

    patch_size = patches.shape[1]  # patches assumed to be square

    # Assign output image shape based on patch sizes
    rows = ((im_h - patch_size) // stride) * stride + patch_size
    cols = ((im_w - patch_size) // stride) * stride + patch_size

    if n_channels == 1:
        reconim = np.zeros((rows, cols))
        divim = np.zeros((rows, cols))
    else:
        reconim = np.zeros((rows, cols, n_channels))
        divim = np.zeros((rows, cols, n_channels))

    p_c = (cols - patch_size + stride) / stride  # number of patches needed to fill out a row

    totpatches = patches.shape[0]
    initr, initc = 0, 0

    # extract each patch and place in the zero matrix and sum it with existing pixel values

    reconim[initr:patch_size, initc:patch_size] = patches[0]# fill out top left corner using first patch
    divim[initr:patch_size, initc:patch_size] = np.ones(patches[0].shape)

    patch_num = 1

    while patch_num <= totpatches - 1:
        initc = initc + stride
        reconim[initr:initr + patch_size, initc:patch_size + initc] += patches[patch_num]
        divim[initr:initr + patch_size, initc:patch_size + initc] += np.ones(patches[patch_num].shape)

        if np.remainder(patch_num + 1, p_c) == 0 and patch_num < totpatches - 1:
            initr = initr + stride
            initc = 0
            reconim[initr:initr + patch_size, initc:patch_size] += patches[patch_num + 1]
            divim[initr:initr + patch_size, initc:patch_size] += np.ones(patches[patch_num].shape)
            patch_num += 1
        patch_num += 1
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

    im_h, im_w = GT.shape[0], GT.shape[1]

    if len(GT.shape) == 2:
        n_channels = 1
    else:
        n_channels = GT.shape[2]

    patches = np.asarray(hr_patches)

    return patches, im_h, im_w, n_channels
