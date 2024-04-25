import torch  # Importing the PyTorch library
import numpy as np  # Importing the NumPy library
import math

from . import feature_extraction, myconfig  # Importing the feature_extraction module


#---get embedding of a single utterance
def get_embedding(file_name, encoder):
    try:
        features = feature_extraction.extract_features(file_name)
        if features is None:
            print(f"Failed to extract features from file: {file_name}")
            return None

        embedding = my_inference(features, encoder)
        if embedding is None:
            print(f"Failed to predict embedding from file: {file_name}")
            return None
        return embedding
    except Exception as e:
        print(f"Error processing file {file_name}: {e}")
        return None

def compute_distance(embedding1, embedding2):
    if len(embedding1) != len(embedding2):
        print("Different lengths of embeddings")
    else:
        result = 0
        for i in range(len(embedding1)):
            result += abs(embedding1[i] - embedding2[i]) ** 2
        return math.sqrt(result)
    
    
def my_inference(features, encoder, is_full_sequence_inference = myconfig.USE_FULL_SEQUENCE_INFERENCE):
    """
    Extracts the embedding of a single utterance or a sequence of utterances using the provided encoder model.
    
    Parameters:
        features (numpy.ndarray): The features of the audio segment.
        encoder: The trained encoder model.
        is_full_sequence_inference (bool): Determines whether the prediction will be made for the entire audio sequence or not.

    Returns:
        numpy.ndarray: The embedding of the audio segment or sequence of audio segments.
    """
    if is_full_sequence_inference:  # Checking if full sequence inference is enabled
        batch_input = torch.unsqueeze(torch.from_numpy(features), dim=0).float().to(myconfig.DEVICE)  # Converting features to a PyTorch tensor and unsqueezing it to add a batch dimension
        batch_output = encoder(batch_input)  # Passing the input through the encoder model
        return batch_output[0, :].cpu().data.numpy()  # Extracting the output embedding and converting it to a NumPy array
    
    else:  # If full sequence inference is not enabled
        windows = feature_extraction.extract_sliding_windows(features)  # Extracting sliding windows of features
        if not windows:  # Checking if there are no sliding windows
            return None
        batch_input = torch.from_numpy(
            np.stack(windows)).float().to(myconfig.DEVICE)  # Converting sliding windows to a PyTorch tensor and moving it to the appropriate device
        batch_output = encoder(batch_input)  # Passing the input through the encoder model

        #------Aggregate the inference outputs from sliding windows
        aggregated_output = torch.mean(batch_output, dim=0, keepdim=False).cpu()  # Calculating the mean of the output embeddings
        return aggregated_output.data.numpy()  # Converting the aggregated output to a NumPy array


# if __name__ == '__main__':
    # x = torch.tensor([1,2,3,4])
    # print(torch.unsqueeze(x,dim=0))
