import numpy as np
import matplotlib.pyplot as plt

def get_indices(GT, stride, patch_size ):
    hr_patches = []

    plt.imshow(GT.astype(np.uint8))
    for i in range(0, GT.shape[0] - patch_size + 1, stride):
        plt.axhline(y=i, color='r', linestyle='--')
        for j in range(0, GT.shape[1] - patch_size + 1, stride):
            hr_patches.append(GT[i:i + patch_size, j:j + patch_size])
            plt.axvline(x=j, color='b', linestyle='--')
    plt.axvline(x=j+patch_size, color='b', linestyle='--')
    plt.axhline(y=i+patch_size, color='r', linestyle='--')
    plt.savefig("PatchedImage.png")
    plt.show()


