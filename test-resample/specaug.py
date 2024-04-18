import numpy as np
import random

import myconfig


def apply_specaug(features):
    """Apply SpecAugment to features."""
    # Get the shape of the input features
    seq_len, n_mfcc = features.shape
    # Copy the input features to the outputs
    outputs = features
    # Compute the mean feature value
    mean_feature = np.mean(features)

    # Apply frequency masking with probability SPECAUG_FREQ_MASK_PROB
    if random.random() < myconfig.SPECAUG_FREQ_MASK_PROB:
        # Randomly select the width of the mask
        width = random.randint(1, myconfig.SPECAUG_FREQ_MASK_MAX_WIDTH)
        # Randomly select the starting index for the mask
        start = random.randint(0, n_mfcc - width)
        # Apply the mask to the frequency dimension by setting masked values to the mean feature value
        outputs[:, start: start + width] = mean_feature

    # Apply time masking with probability SPECAUG_TIME_MASK_PROB
    if random.random() < myconfig.SPECAUG_TIME_MASK_PROB:
        # Randomly select the width of the mask
        width = random.randint(1, myconfig.SPECAUG_TIME_MASK_MAX_WIDTH)
        # Randomly select the starting index for the mask
        start = random.randint(0, seq_len - width)
        # Apply the mask to the time dimension by setting masked values to the mean feature value
        outputs[start: start + width, :] = mean_feature

    return outputs
