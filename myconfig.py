import multiprocessing
import datetime
import os
import torch

# Define the paths to training and testing data
TRAIN_DATA_DIR = os.path.join(os.path.expanduser('~'), r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\LibriSpeech\train-clean-360")
TEST_DATA_DIR = os.path.join(os.path.expanduser('~'), r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\LibriSpeech\test-clean")

# Create a timestamp for model saving
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
filename = f"saved_model_{timestamp}.pt"
SAVED_MODEL_PATH = os.path.join(os.path.expanduser('~'), r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model", filename)

# Number of samples in each training batch
BATCH_SIZE = 8
# Number of processes to use for multiprocessing, maximum is the number of available CPUs or equal to BATCH_SIZE
NUM_PROCESSES = min(multiprocessing.cpu_count(), BATCH_SIZE)

# Number of training steps
TRAINING_STEPS = 50000

# Use transformer instead of LSTM
USE_TRANSFORMER = False
# Set the device to be used (cuda if available, otherwise cpu)
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# DEVICE = "cpu"

# Number of MFCC dimensions
N_MFCC = 80
# Size of LSTM hidden layers
LSTM_HIDDEN_SIZE = 64
# Number of LSTM layers stacked on top of each other
LSTM_NUM_LAYERS = 3
# Whether to use bidirectional LSTM or not
BI_LSTM = True
# Method of aggregating frames, whether it's mean or not
FRAME_AGGREGATION_MEAN = True
# Learning rate
LEARNING_RATE = 0.0001
# Length of input sequence
SEQ_LEN = 100
# Whether to use SpecAugment during training or not
SPECAUG_TRAINING = True
# Frequency of saving the model
SAVE_MODEL_FREQUENCY = 5000

# Parameters for SpecAugment
SPECAUG_FREQ_MASK_PROB = 0.3
SPECAUG_TIME_MASK_PROB = 0.3
SPECAUG_FREQ_MASK_MAX_WIDTH = N_MFCC // 5
SPECAUG_TIME_MASK_MAX_WIDTH = SEQ_LEN // 5
# Alpha parameter for the triplet loss function
TRIPLET_ALPHA = 0.1

# If true, use transformer instead of LSTM
USE_TRANSFORMER = False
# Size of layers in the transformer
TRANSFORMER_DIM = 32
# Number of encoder layers for the transformer
TRANSFORMER_ENCODER_LAYERS = 2
# Number of heads in the transformer
TRANSFORMER_HEADS = 8

# Number of triplets used to evaluate Equal Error Rate (EER)
NUM_EVAL_TRIPLETS = 10000

# Whether to use the full sequence for prediction
USE_FULL_SEQUENCE_INFERENCE = True
# Sliding window step size
SLIDING_WINDOW_STEP = 50
# Evaluation threshold step size
EVAL_THRESHOLD_STEP = 0.001
