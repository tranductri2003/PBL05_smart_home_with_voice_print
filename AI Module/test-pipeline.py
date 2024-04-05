import os
import torch
import time
import csv
from collections import defaultdict, Counter
from Speaker_Recognition.LSTM import *
from PoS_Tagging import *
from transformers import pipeline

# Kiểm tra xem CUDA có sẵn không, nếu không, sử dụng CPU
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def speech2text(wav_file):
    # Sử dụng pipeline của transformers để chuyển đổi âm thanh thành văn bản
    model = pipeline('automatic-speech-recognition', model='vinai/PhoWhisper-base', device=DEVICE)
    return model(wav_file)['text']


