from transformers import AutoModel, AutoTokenizer

# 下载模型和分词器
model = AutoModel.from_pretrained("distilbert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# 保存模型和分词器到本地
# 使用原始字符串
model.save_pretrained(r"D:\VSCode\MyAiAgent\local_models\distilbert-base-uncased")
tokenizer.save_pretrained(r"D:\VSCode\MyAiAgent\local_models\distilbert-base-uncased")

# 或者使用双反斜杠
# model.save_pretrained("D:\\VSCode\\MyAiAgent\\local_models\\distilbert-base-uncased")
# tokenizer.save_pretrained("D:\\VSCode\\MyAiAgent\\local_models\\distilbert-base-uncased")
