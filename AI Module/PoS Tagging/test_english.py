import spacy
import time


# Load mô hình tiếng Anh, thay thế bằng mô hình tiếng Việt nếu có
start_time_load = time.time()

nlp = spacy.load("en_core_web_sm")

end_time_load = time.time()

print(end_time_load - start_time_load)


# Câu ví dụ
sentence = "The quick brown fox jumps over the lazy dog."

start_time_inference = time.time()
# Thực hiện POS tagging
doc = nlp(sentence)

# In ra từ và nhãn POS tương ứng
for token in doc:
    print(token.text, token.pos_)

# Lọc và in ra động từ và danh từ
verbs = [token.text for token in doc if token.pos_ == "VERB"]
nouns = [token.text for token in doc if token.pos_ == "NOUN"]
end_time_inference = time.time()


print("Verbs:", verbs)
print("Nouns:", nouns)
print(end_time_inference - start_time_inference)
