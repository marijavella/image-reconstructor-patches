import click
from patch_reconstructor.recon_from_patches import *
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as pil_image


def get_indices(GT, stride, patch_size):

    plt.imshow(GT.astype(np.uint8))
    for i in range(0, GT.shape[0] - patch_size + 1, stride):
        plt.axhline(y=i, color='r', linestyle='--')
        for j in range(0, GT.shape[1] - patch_size + 1, stride):
            plt.axvline(x=j, color='b', linestyle='--')

    plt.axvline(x=j+stride, color='b', linestyle='--')
    plt.axhline(y=i+stride, color='r', linestyle='--')

    plt.show()


@click.command()
@click.option("--stride", default=18, help='Empty')
@click.option("--patch_size", default=33, help='Empty')
@click.argument('input_image', type=click.Path(exists=True))
def demo(input_image, stride, patch_size):

    GT = np.array(pil_image.open(input_image))  # extract image

    get_indices(GT, stride, patch_size)

    patches, im_h, im_w, n_channels = get_patches(GT, stride, patch_size)  # split image into patches (demo purposes)
    
    reconstructedim = recon_im(patches, im_h, im_w, n_channels, stride)  # reconstruct original image from patches

    # TODO: Plot original, patches, reconstructed here

    if n_channels == 1:  # TODO: Remove gray colormap
        plt.imshow(reconstructedim, cmap='gray')
        plt.show()
    else:
        plt.imshow(reconstructedim.astype(np.uint8))
        plt.show()


if __name__ == '__main__':
    demo()
