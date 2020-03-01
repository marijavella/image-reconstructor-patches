import click
from path_reconstructor.recon_from_patches import *

import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as pil_image


@click.command()
@click.option("--stride", default=18, help='Empty')
@click.option("--patch_size", default=33, help='Empty')
@click.argument('input_image', type=click.Path(exists=True))
def demo(input_image, stride, patch_size):
    GT = np.array(pil_image.open(input_image))
    patches, im_h, im_w, n_channels = get_patches(GT, stride, patch_size)
    #TODO: Add functionality to show a patches image or save it 

    reconstructedim = recon_im(patches, im_h, im_w, n_channels, stride, patch_size)

    if n_channels == 1:
        plt.imshow(reconstructedim, cmap='gray')
        plt.show()
    else:
        plt.imshow(reconstructedim.astype(np.uint8))
        plt.show()

if __name__ == '__main__':
    demo()

