import re
import json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam
import numpy as np
import os
from pickle import dump, load
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


file_path = 'preprocessed_titles.txt'

titles = []
with open(file_path, 'r', encoding='utf-8') as file:
    for i, line in enumerate(file):
        if i < 5000:  # 仅读取前5000行
            title = line.strip().lower()
            titles.append(title)
        else:
            break  # 当读取到5000行时，退出循环


tokenizer = Tokenizer()
tokenizer.fit_on_texts(titles)
total_words = len(tokenizer.word_index) + 1

input_sequences = []
for line in titles:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# 填充序列以保持统一长度
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

# 分割为特征和标签
predictors, label = input_sequences[:,:-1], input_sequences[:,-1]
label = to_categorical(label, num_classes=total_words)

# 定义模型
def create_model(total_words, max_sequence_len):
    model = Sequential()
    model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
    model.add(LSTM(150, return_sequences=True))
    model.add(LSTM(100))
    model.add(Dense(total_words, activation='softmax'))
    # 编译模型
    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.01), metrics=['accuracy'])
    return model

# 创建模型
model = create_model(total_words, max_sequence_len)
model.summary()

# 设置checkpoint
checkpoint_path = 'model_checkpoint2.h5'
checkpoint = ModelCheckpoint(checkpoint_path, monitor='loss', verbose=1, save_best_only=True, mode='min')

# 训练模型
model.fit(predictors, label, epochs=100, verbose=1, callbacks=[checkpoint],batch_size=64)

# 保存tokenizer
dump(tokenizer, open('tokenizer2.pkl', 'wb'))

