from pyvi import ViTokenizer
from gensim.models import FastText
import numpy as np

# Load pre-trained FastText model for Vietnamese
model = FastText.load_fasttext_format('D:/Code/BachKhoa/PBL 5/PBL05_smart_home_with_voice_print_and_antifraud_ai/AI Module/PoS Tagging/cc.vi.300.bin')

# Define the sentences
sentence1 = "Tôi muốn bật đèn ở phòng khách."
sentence2 = "Tôi muốn bật đèn ở phòng ngủ."
sentence3 = "Tôi muốn bật đèn ở phòng khách. À không, tôi muốn bật đèn phòng ngủ"

# Tokenize and embed sentences
def embed_sentence(sentence):
    tokens = ViTokenizer.tokenize(sentence).split()
    valid_tokens = [word for word in tokens if word in model.wv.vocab]
    if valid_tokens:
        embedding = np.mean([model[word] for word in valid_tokens], axis=0)
        return embedding
    else:
        # Handle case when no valid tokens are found in the model's vocabulary
        return np.zeros(model.vector_size)  # Return zero vector

embedding1 = embed_sentence(sentence1)
embedding2 = embed_sentence(sentence2)
embedding3 = embed_sentence(sentence3)

# Calculate Euclidean distance
euclidean_distance13 = np.linalg.norm(embedding1 - embedding3)
euclidean_distance23 = np.linalg.norm(embedding2 - embedding3)

print("Euclidean Distance between sentence 1 and sentence 3:", euclidean_distance13)
print("Euclidean Distance between sentence 2 and sentence 3:", euclidean_distance23)
