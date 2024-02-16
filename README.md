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

## 后续方向

- 可以使用机器学习进行查询预测(给出一个单词预测后面的单词是什么)。训练时候只需要本数据集的所有题目进行划分设为 input 并进行验证即可
- 优化代码结构
- 将代码与FastAPI结合



## 往届信息

|                                                              | 拼写纠正 | 同义词检索 | 单词预测 |
| ------------------------------------------------------------ | -------- | ---------- | -------- |
| **Re-Search**<br /> https://github.com/GaganSD/ttds-cw3-research-team | ⭕        | ⭕          | ❌        |
| **TTDS Movie Search IR Project 2020** <br />https://github.com/marinapts/ttds_movie_search | ❌        | ❌          | ⭕        |
| **TTDS Paper Search**<br />https://github.com/jerryzhao173985/TTDS_Paper_Search | ❌        | ❌          | (simple) |
| **Recipe Search and Recommendation Engine** <br />https://github.com/Ethan-Yang0101/Text-Technology-For-Data-Science |          |            |          |
| TTDS Paper Search<br />https://github.com/jiaqingxie/AI-paper-search-engine |          |            |          |

