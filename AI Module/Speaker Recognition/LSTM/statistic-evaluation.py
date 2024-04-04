import numpy as np
import torch
import torch.nn as nn
import time
import os
import matplotlib.pyplot as plt
import torch.optim as optim
import csv
from collections import defaultdict

from inference import my_inference
import multiprocessing
import multiprocessing.pool 
import myconfig
import dataset
from evaluation import TripletScoreFetcher
from neural_net import get_speaker_encoder

def FRR(labels, scores, thres):
    fn = 0
    tp = 0
    for i in range(len(labels)):
        if scores[i] >= thres:
            if labels[i] == 0:
                fn += 1
            else:
                tp += 1
    if (tp+fn) == 0:
        return 0
    return fn / (tp+fn)

def FAR(labels, scores, thres):
    tn = 0
    fp = 0
    for i in range(len(labels)):
        if scores[i] < thres:
            if labels[i] == 0:
                tn += 1
            else:
                fp += 1
    if (tn+fp) == 0:
        return 0
    return fp / (fp+tn)

def compute_equal_error_rate2(labels, scores):
    min_delta = 1
    eer = 1
    thres = 0
    while thres < 1:
        FAR(labels, scores, thres)
        far_ = FAR(labels, scores, thres)
        frr_ = FRR(labels, scores, thres)
        delta_ = abs(far_ - frr_)
        if delta_ < min_delta:
            min_delta = delta_
            eer = (far_ + frr_) / 2
            thres += myconfig.EVAL_THRESHOLD_STEP
    return eer, thres

def compute_equal_error_rate(labels, scores):
    if len(labels) != len(scores):
        raise ValueError("Length of labels and scored must match")
    eer_threshold = None
    eer = None
    min_delta = 1
    threshold = 0.0
    while threshold < 1.0:
        accept = [score >= threshold for score in scores]
        fa = [a and (1-l) for a, l in zip(accept, labels)]
        fr = [(1-a) and l for a, l in zip(accept, labels)]
        far = sum(fa) / (len(labels) - sum(labels))
        frr = sum(fr) / sum(labels)
        delta = abs(far - frr)
        if delta < min_delta:
            min_delta = delta
            eer = (far + frr) / 2
            eer_threshold = threshold
        threshold += myconfig.EVAL_THRESHOLD_STEP

    return eer, eer_threshold

def compute_scores(encoder, dict_speaker, num_eval_triplets=myconfig.NUM_EVAL_TRIPLETS):
    labels = []
    scores = []
    fetcher = TripletScoreFetcher(dict_speaker, encoder, num_eval_triplets)
    with multiprocessing.pool.ThreadPool(myconfig.NUM_PROCESSES) as pool:
        while num_eval_triplets > len(labels)//2: 
            label_score_pairs = pool.map(fetcher, range(len(labels)//2, num_eval_triplets))
            for triplet_labels, triplet_scores in label_score_pairs:
                labels.extend(triplet_labels)
                scores.extend(triplet_scores)
        pool.close()
                
    print("Evaluated", len(labels)//2, "triplets in total")
    return (labels, scores)

def run_eval(model_path):
    start_time = time.time()
    spk_to_utts = dataset.get_librispeech_speaker_to_utterance(myconfig.TEST_DATA_DIR)
    print("Evaluation data:", myconfig.TEST_DATA_DIR)
    
    encoder = get_speaker_encoder(model_path)
    labels, scores = compute_scores(encoder, spk_to_utts, myconfig.NUM_EVAL_TRIPLETS)
    eer, eer_threshold = compute_equal_error_rate(labels, scores)
    eval_time = time.time() - start_time
    print("Finished evaluation in", eval_time, "seconds")
    print("eer_threshold =", eer_threshold, "eer =", eer)
    return eer, eer_threshold

MODEL_PATHS = [
    # r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\nhi's model\mfcc_2lstm_model_100k_specaug_batch_8_saved_model.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\nhi's model\mfcc_lstm_model_100k_specaug_batch_8_saved_model.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-100-hours-100-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_100h_100epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-100-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_360h_100epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-20000-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_360h_20000epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-gpu\mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_gpu.pt",
    # r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-4-stacks-cpu\mfcc_lstm_model_360h_50000epochs_specaug_8batch_4stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-other-500-hours-50000-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_500h_10000epochs_specaug_8batch_3stacks_cpu.pt",
]

MODEL_NAMES = [
    # "mfcc_2lstm_model_100k_specaug_batch_8_saved_model.pt",
    "mfcc_lstm_model_100k_specaug_batch_8_saved_model.pt",
    "mfcc_lstm_model_100h_100epochs_specaug_8batch_3stacks_cpu.pt",
    "mfcc_lstm_model_360h_100epochs_specaug_8batch_3stacks_cpu.pt",
    "mfcc_lstm_model_360h_20000epochs_specaug_8batch_3stacks_cpu.pt",
    "mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt",
    "mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_gpu.pt",
    #"mfcc_lstm_model_360h_50000epochs_specaug_8batch_4stacks_cpu.pt",
    "mfcc_lstm_model_500h_10000epochs_specaug_8batch_3stacks_cpu.pt",

]

start_time = time.time()

# Chạy thống kê cho từng model
eer_results = defaultdict(list)
eer_threshold_results = defaultdict(list)

for i, model_path in enumerate(MODEL_PATHS):
    for j in range(10):  # Chạy 10 lần để lấy giá trị trung bình
        print(f"Running evaluation for model {model_path}, run {j+1}/10")
        eer, eer_threshold = run_eval(model_path)
        eer_results[MODEL_NAMES[i]].append(eer)
        eer_threshold_results[MODEL_NAMES[i]].append(eer_threshold)


end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")


# Khai báo đường dẫn của file CSV
csv_file_path = "statistic-train-models.csv"

# Khởi tạo dữ liệu kết quả
data = [("Model", "Num Eval Triplets", "Average EER", "Best EER", "Average EER-Threshold", "Best EER-Threshold")]

# Thêm dữ liệu từ kết quả thống kê vào danh sách data
for model in MODEL_NAMES:
    num_eval_triplets = myconfig.NUM_EVAL_TRIPLETS
    avg_eer = sum(eer_results[model]) / len(eer_results[model])
    best_eer = min(eer_results[model])
    avg_eer_threshold = sum(eer_threshold_results[model]) / len(eer_threshold_results[model])
    best_eer_threshold = min(eer_threshold_results[model])
    
    data.append((model, num_eval_triplets, avg_eer, best_eer, avg_eer_threshold, best_eer_threshold))
    

# Ghi dữ liệu vào file CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV file 'statistic-train-models.csv' has been created successfully.")