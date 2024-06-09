import multiprocessing
import os
import time
import matplotlib.pyplot as plt
import torch
from torch import nn
import dataset
import feature_extraction
import myconfig


class BaseSpeakerEncoder(nn.Module):
    def _load_from(self, saved_model):
        var_dict=torch.load(saved_model, map_location=myconfig.DEVICE)
        self.load_state_dict(var_dict["encoder_state_dict"])

class TransformerSpeakerEncoder(BaseSpeakerEncoder):

    def __init__(self, saved_model=""):
        super(TransformerSpeakerEncoder, self).__init__()
        # Define the Transformer network.
        self.linear_layer = nn.Linear(myconfig.N_MFCC, myconfig.TRANSFORMER_DIM)
        self.encoder = nn.TransformerEncoder(nn.TransformerEncoderLayer(
            d_model=myconfig.TRANSFORMER_DIM, nhead=myconfig.TRANSFORMER_HEADS,
            batch_first=True),
            num_layers=myconfig.TRANSFORMER_ENCODER_LAYERS)
        self.decoder = nn.TransformerDecoder(nn.TransformerDecoderLayer(
            d_model=myconfig.TRANSFORMER_DIM, nhead=myconfig.TRANSFORMER_HEADS,
            batch_first=True),
            num_layers=1)

        # Load from a saved model if provided.
        if saved_model:
            self._load_from(saved_model)

    def forward(self, x):
        encoder_input = torch.sigmoid(self.linear_layer(x))
        encoder_output = self.encoder(encoder_input)
        tgt = torch.zeros(x.shape[0], 1, myconfig.TRANSFORMER_DIM).to(
            myconfig.DEVICE)
        output = self.decoder(tgt, encoder_output)
        return output[:, 0, :]

class LstmSpeakerEncoder(BaseSpeakerEncoder):

    def __init__(self, saved_model=""):
        super(LstmSpeakerEncoder, self).__init__()
        self.lstm = nn.LSTM(
            input_size=myconfig.N_MFCC,
            hidden_size=myconfig.LSTM_HIDDEN_SIZE,
            num_layers=myconfig.LSTM_NUM_LAYERS,
            batch_first=True,
            bidirectional=myconfig.BI_LSTM)
        if saved_model:
            self._load_from(saved_model)

    def _aggregate_frames(self, batch_output):
        if myconfig.FRAME_AGGREGATION_MEAN:
            return torch.mean(batch_output, dim=1, keepdim=False)
        else:
            return batch_output[:, -1, :]

    def forward(self, x):
        D = 2 if myconfig.BI_LSTM else 1
        h0 = torch.zeros(D * myconfig.LSTM_NUM_LAYERS, x.shape[0], myconfig.LSTM_HIDDEN_SIZE).to(myconfig.DEVICE)
        c0 = torch.zeros(D * myconfig.LSTM_NUM_LAYERS, x.shape[0], myconfig.LSTM_HIDDEN_SIZE).to(myconfig.DEVICE)
        y, (hn, cn) = self.lstm(x, (h0, c0))
        return self._aggregate_frames(y)


def get_speaker_encoder(load_from=""):
    """Create speaker encoder model or load it from a saved model."""
    if myconfig.USE_TRANSFORMER:
        return TransformerSpeakerEncoder(load_from).to(myconfig.DEVICE)
    else:
        return LstmSpeakerEncoder(load_from).to(myconfig.DEVICE)


def get_triplet_loss(anchor, pos, neg,):
    """Triplet loss defined in https://arxiv.org/pdf/1705.02304.pdf."""
    cos = nn.CosineSimilarity(dim=-1, eps=1e-6)
    return torch.maximum(
        cos(anchor, neg) - cos(anchor, pos) + myconfig.TRIPLET_ALPHA,
        torch.tensor(0.0))


def get_triplet_loss_from_batch_output(batch_output, batch_size):
    """Triplet loss from N*(a|p|n) batch output."""
    batch_output_reshaped = torch.reshape(batch_output, (batch_size, 3, batch_output.shape[1]))     #batch_output_reshaped.shape=[8,3,128]
    batch_loss = get_triplet_loss(
        batch_output_reshaped[:, 0, :],     #all the 1st row will be anchor
        batch_output_reshaped[:, 1, :],     #all the 2nd row will be positive
        batch_output_reshaped[:, 2, :])     #all the 3rd row will be negative
    loss = torch.mean(batch_loss)
    return loss


def save_model(saved_model_path, encoder, losses, start_time):
    """Save model to disk."""
    training_time = time.time() - start_time
    os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
    if not saved_model_path.endswith(".pt"):
        saved_model_path += ".pt"
    torch.save({"encoder_state_dict": encoder.state_dict(),
                "losses": losses,
                "training_time": training_time},
               saved_model_path)


def train_network(speaker_to_utterance, num_steps, saved_model="", pool=None):
    losses = []
    start_time = time.time()
    encoder = get_speaker_encoder()

    #Train
    optimizer = torch.optim.Adam(encoder.parameters(), lr=myconfig.LEARNING_RATE)
    start_time = time.time()
    print("Start training at:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))  # Thay đổi ở đây

    for step in range(num_steps):
        optimizer.zero_grad()

        #build batch input
        batch_input = feature_extraction.get_batched_triplet_input(speaker_to_utterance, myconfig.BATCH_SIZE, pool)
        batch_input = batch_input.to(myconfig.DEVICE)  # Chuyển đầu vào lên GPU
        batch_output = encoder(batch_input)     #batch_output.shape=[24,64*2]
        loss = get_triplet_loss_from_batch_output(batch_output, myconfig.BATCH_SIZE)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
        print(f"step: {step}/{num_steps} loss: {loss.item()}")

    #     saving model
        if saved_model is not None and (step + 1) % myconfig.SAVE_MODEL_FREQUENCY == 0:
            checkpoint = saved_model
            if checkpoint.endswith(".pt"):
                checkpoint = checkpoint[:-3]
            checkpoint += ".ckpt-" + str(step + 1) + ".pt"
            save_model(checkpoint,encoder, losses, start_time)

    training_time = time.time() - start_time
    print("End training at:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))  # Thay đổi ở đây
    print("Finished training in", training_time, "seconds")
    
    if saved_model is not None:
        save_model(saved_model, encoder, losses, start_time)
    return losses


def run_training():
    print("Training data:", myconfig.TRAIN_DATA_DIR)
    speaker_to_utterance = dataset.get_librispeech_speaker_to_utterance(myconfig.TRAIN_DATA_DIR)

    with multiprocessing.Pool(myconfig.NUM_PROCESSES) as pool:
        losses = train_network(speaker_to_utterance,
                               myconfig.TRAINING_STEPS,
                               myconfig.SAVED_MODEL_PATH,
                               pool)
    plt.plot(losses)
    plt.xlabel("step")
    plt.ylabel("loss")
    plt.show()



if __name__ == '__main__':
    run_training()

