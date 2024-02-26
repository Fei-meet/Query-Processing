# Query-Processing

一个简单的查询语句处理模块模块，包含预处理，拼写纠正，

同义词检索的功能。

## 预处理

包含转小写，去除标点符号，tokens以及字数限制(20单词以内)

返回值为 处理后的查询语句 和 可能的警告信息列表

## 拼写纠正

使用 `spellchecker` 库进行快速的拼写修正。与 `TextBlob` 库相比该库在正确率相似的前提下运行时间更短。

同时该库基于一种“最小编辑距离”（Levenshtein距离）算法来查找和建议最接近错误拼写单词的正确单词。对于不在词典中的单词选取在最小编辑距离意义上与错误单词接近的单词进行替换。

返回值为 处理后的查询语句 和 可能的警告信息列表

## 同义词检索

该函数可为查询添加语义上相关的同义词。实现是对每个过滤后的单词(消去停止词)，根据其词性查找同义词集（WordNet的`synsets`）。为了提高效率，使用了一个缓存(`synset_cache`)来存储已查询过的单词的同义词集。

## 问题

- 预处理阶段只截取了**20**个字符以内的查询语句，在项目要求中没有找到关于查询语句大小的规定。该部分代码可以调整以适应不同长度的查询
- 预处理和拼写修正的时间约为 **0.1 / 0.2 s** , 添加同义词检索后运行时间增至 **1.3s** 左右，可以考虑将同义词检索设置为附加功能而不是基本功能，以减少搜索处理时间。

## 单词预测

该部分代码分为完整代码`Predict.ipynb`(包含题目的预处理阶段)和模型训练代码`pre.py`使用TensorFlow和Keras库来处理文本数据，并训练了一个文本生成模型。用于预测用户之后的输入。accuracy能达到70左右(暂时没搞懂这个“准确率”的含义)，但是还需要继续改进模型。

在预处理阶段中，只读取了`dataset`中所有文章的题目，并将其中 Not found title的文件以及长度小于2的文件排除。同时去除了题目中的标点符号与数字，只保留了英文字符。对于标题中的每个词，生成n-gram序列，并将这些序列作为输入数据。

使用循环神经网络模型，包含嵌入层(`Embedding`)、两个长短期记忆层(`LSTM`)和一个全连接层(`Dense`)。

在文档`Model Version`中有之前三次训练的结果，**各有缺点**。因此需要后续的训练。

## 语义消歧

语义消歧原本是想使用和单词预测一样的思路选择数据库进行训练。后来发现已有预训练好的`pywsd`库，便使用该库。代码文件为`Word_Sense_Disambiguation.py` 

- 函数使用`find_polysemous_words`函数找到句子中的所有多义词。
- 然后，对于每个多义词，使用`simple_lesk`算法尝试确定其在给定上下文中的最可能意义。

然而，对于title的消歧功能并不是很完美，有时候会出现不能正确判定的情况。

## 往届信息

|                                                              | 拼写纠正 | 同义词检索 | 单词预测 |
| ------------------------------------------------------------ | -------- | ---------- | -------- |
| **Re-Search**<br /> https://github.com/GaganSD/ttds-cw3-research-team | ⭕        | ⭕          | ❌        |
| **TTDS Movie Search IR Project 2020** <br />https://github.com/marinapts/ttds_movie_search | ❌        | ❌          | ⭕        |
| **TTDS Paper Search**<br />https://github.com/jerryzhao173985/TTDS_Paper_Search | ❌        | ❌          | (simple) |
| **Recipe Search and Recommendation Engine** <br />https://github.com/Ethan-Yang0101/Text-Technology-For-Data-Science |          |            |          |
| TTDS Paper Search<br />https://github.com/jiaqingxie/AI-paper-search-engine |          |            |          |
