import random

import librosa
import numpy as np
import torch

import dataset
import soundfile as sf

import myconfig
import specaug


def extract_features(audio_file):
    """Extract MFCC features from an audio file, shape=(TIME, MFCC)."""
    waveform, sample_rate = sf.read(audio_file)

    # Convert stereo audio to mono
    if len(waveform.shape) == 2:
        waveform = librosa.to_mono(waveform.transpose())

    # Resample audio to 16kHz if not already
    if sample_rate != 16000:
        waveform = librosa.resample(waveform, sample_rate, 16000)

    # Compute Mel-frequency cepstral coefficients (MFCCs)
    features = librosa.feature.mfcc(y=waveform, sr=sample_rate, n_mfcc=myconfig.N_MFCC)
    # The shape of features will be (TIME, MFCC), e.g., (40, 441)

    return features.transpose()


def get_triplet_features(spk_to_utts):
    """Get MFCC features for a triplet of anchor/pos/neg samples."""
    anchor_utt, pos_utt, neg_utt = dataset.get_triplet(spk_to_utts)
    return (extract_features(anchor_utt),
            extract_features(pos_utt),
            extract_features(neg_utt))


def trim_features(features, apply_specaug):
    """
    Trim features to SEQ_LEN. If the number of rows exceeds SEQ_LEN, randomly extract SEQ_LEN rows.
    Optionally apply SpecAugment.
    """
    full_length = features.shape[0]
    start = random.randint(0, full_length - myconfig.SEQ_LEN)
    trimmed_features = features[start: start + myconfig.SEQ_LEN, :]
    if apply_specaug:
        trimmed_features = specaug.apply_specaug(trimmed_features)
    return trimmed_features


class TrimmedTripletFeaturesFetcher:
    def __init__(self, speaker_to_utterance):
        self.speaker_to_utterance = speaker_to_utterance

    def __call__(self, _):
        """Get a triplet of trimmed anchor/pos/neg features."""
        anchor, pos, neg = get_triplet_features(self.speaker_to_utterance)
        while anchor.shape[0] < myconfig.SEQ_LEN or pos.shape[0] < myconfig.SEQ_LEN or neg.shape[0] < myconfig.SEQ_LEN:
            anchor, pos, neg = get_triplet_features(self.speaker_to_utterance)
        return np.stack([trim_features(anchor, myconfig.SPECAUG_TRAINING),
                         trim_features(pos, myconfig.SPECAUG_TRAINING),
                         trim_features(neg, myconfig.SPECAUG_TRAINING)])


def get_batched_triplet_input(speaker_to_utterance, batch_size, pool):
    """Get batched triplet input for training."""
    fetcher = TrimmedTripletFeaturesFetcher(speaker_to_utterance)
    if pool is None:
        input_arrays = list(map(fetcher, range(batch_size)))
    else:
        input_arrays = pool.map(fetcher, range(batch_size))
    # Concatenate the input arrays to form the batch input
    batch_input = torch.from_numpy(np.concatenate(input_arrays)).float()
    return batch_input


def extract_sliding_windows(features):
    """Extract sliding windows from features."""
    sliding_windows = []
    start = 0
    
    while start + myconfig.SEQ_LEN <= features.shape[0]:
        sliding_windows.append(features[start: start + myconfig.SEQ_LEN, :])
        start += myconfig.SLIDING_WINDOW_STEP
    return sliding_windows
