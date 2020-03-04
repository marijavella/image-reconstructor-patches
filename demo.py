import click
from patch_reconstructor.recon_from_patches import *
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as pil_image


def plot_patches(ax, GT, stride, patch_size):

    ax.imshow(GT.astype(np.uint8), cmap='gray')
    for i in range(0, GT.shape[0] - patch_size + 1, stride):
        ax.axhline(y=i, color='r', linestyle='--')
        for j in range(0, GT.shape[1] - patch_size + 1, stride):
            ax.axvline(x=j, color='b', linestyle='--')

    ax.axvline(x=j+stride, color='b', linestyle='--')
    ax.axhline(y=i+stride, color='r', linestyle='--')
    ax.set_title('Patches Selected', size=40)
    ax.axis('off')

@click.command()
@click.option("--stride", default=18, help='Empty')
@click.option("--patch_size", default=33, help='Empty')
@click.argument('input_image', type=click.Path(exists=True))
def demo(input_image, stride, patch_size):

    GT = np.array(pil_image.open(input_image))  # extract image

    patches, im_h, im_w, n_channels = get_patches(GT, stride, patch_size)  # split image into patches (demo purposes)
    
    reconstructedim = recon_im(patches, im_h, im_w, n_channels, stride)  # reconstruct original image from patches

    # Plotting demo images and patches
    fig = plt.figure(figsize=(28, 10))

    ax = fig.add_subplot(1, 3, 1)
    ax.imshow(GT, cmap='gray')
    ax.set_title('Original Image', size=40)
    ax.axis('off')

    ax2 = fig.add_subplot(1, 3, 2)
    plot_patches(ax2, GT, stride, patch_size)

    ax3 = fig.add_subplot(1, 3, 3)
    ax3.imshow(reconstructedim.astype(np.uint8), cmap='gray')
    ax3.set_title('Reconstructed Image', size=40)
    ax3.axis('off')

    plt.show()


if __name__ == '__main__':
    demo()

