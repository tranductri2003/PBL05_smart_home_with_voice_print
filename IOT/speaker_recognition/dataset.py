import glob
import os
import random

"""
example of flac file: r"'D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\LibriSpeech\train-clean-100\19\198\19-198-0000.flac"
"""

# This function creates a dictionary where the key is the speaker ID and the value is a list of their utterances
def get_librispeech_speaker_to_utterance(data_dir):
    speaker_to_utterance = dict()
    flac_files = glob.glob(os.path.join(data_dir, "*", "*", "*.flac"))

    # Iterate through all flac files in the data directory
    for file in flac_files:
        # Extract the speaker ID from the file path
        speaker_id = file.split("\\")[-3]
        # Extract the utterance ID from the file name
        utterance_id = file.split("\\")[-1].split(".")[0]

        # Add the file path to the corresponding speaker's list in the dictionary
        if speaker_id not in speaker_to_utterance:
            speaker_to_utterance[speaker_id] = []
        speaker_to_utterance[speaker_id].append(file)
    return speaker_to_utterance


# This function generates a triplet data consisting of anchor, positive, and negative samples
def get_triplet(spk_to_utts):
    """Get a triplet of anchor/pos/neg samples."""
    # Randomly choose two different speakers as positive and negative
    pos_spk, neg_spk = random.sample(list(spk_to_utts.keys()), 2)

    # Check if the positive speaker has at least two utterances, if not, choose again
    while len(spk_to_utts[pos_spk]) < 2:
        pos_spk, neg_spk = random.sample(list(spk_to_utts.keys()), 2)

    # Randomly select two utterances from the positive speaker as anchor and positive
    anchor_utt, pos_utt = random.sample(spk_to_utts[pos_spk], 2)
    # Randomly select one utterance from the negative speaker as the negative sample
    neg_utt = random.sample(spk_to_utts[neg_spk], 1)[0]

    return (anchor_utt, pos_utt, neg_utt)
