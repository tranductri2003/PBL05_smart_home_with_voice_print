from pyvi import ViTokenizer, ViPosTagger

# Tiến hành tách từ
text = "Tôi muốn tắt đèn phòng ngủ"
tokenized_text = ViTokenizer.tokenize(text)

# Thực hiện POS tagging
pos_tags = ViPosTagger.postagging(tokenized_text)

# Xuất ra kết quả
tokens, tags = pos_tags
for token, tag in zip(tokens, tags):
    print(f"{token}: {tag}")
