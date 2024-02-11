from textblob import TextBlob
import time
import re
from spellchecker import SpellChecker

spell = SpellChecker()

start_time = time.time()  # 获取当前时间

# 方法来自: https://github.com/GaganSD/ttds-cw3-research-team/blob/main/core_algorithms/adv_query_options.py
def query_spell_check(query):
    s = re.sub(r'[^\w\s]', '', query)
    wordlist = s.split()
    spell = SpellChecker()
    # find those words that may be misspelled
    misspelled_list = list(spell.unknown(wordlist))
    # To keep the query order
    misspelled = [word for word in wordlist if word in misspelled_list]
    new_query = []
    for word in wordlist:
        if word not in misspelled:
            new_query.append(word)
        else:
            curr = spell.correction(word)
            new_query.append(curr)
    return new_query



def preprocess_query(query):
    query = query.lower()
    # 将查询语句分割成单词列表
    tokens = query.split()
    message = []

    # 检查单词数量是否超过20个
    if len(tokens) > 20:
        # 如果超过20个，警告用户并只使用前20个单词
        warning_message = "Your query contains more than 20 words. Only the first 20 words will be considered."
        message.append(warning_message)
        processed_query = ' '.join(tokens[:20])
        return processed_query, message
    else:
        # 如果没有超过，返回原始查询
        return query, message


def correct_spelling(preprocessed_query):
    query, message = preprocessed_query  # 预处理模块的输出

    # 进行拼写修正，不论是否有警告信息
    blob = TextBlob(query)
    corrected_text = str(blob.correct())

    # 比较原始查询和更正后的查询，查找更正的单词
    original_words = query.split()
    corrected_words = corrected_text.split()

    corrections = []
    for original, corrected in zip(original_words, corrected_words):
        if original != corrected:  # 如果发现更正
            corrections.append((original, corrected))

    if corrections:  # 如果有拼写更正
        corrections_message = "Some words were corrected, do you mean: " + ", ".join([f"{o}->{c}" for o, c in corrections]) + "?"
        message.append(corrections_message)

    return corrected_text, " ".join(message)


def correct_spelling2(preprocessed_query):
    query, message = preprocessed_query
    words = query.split()

    corrected_words = [spell.correction(word) if spell.unknown([word]) else word for word in words]
    corrections = [(original, corrected) for original, corrected in zip(words, corrected_words) if
                   original != corrected]

    if corrections:
        corrections_message = "Some words were corrected, do you mean: " + ", ".join(
            [f"{c}->{o}" for o, c in corrections]) + "?"
        if isinstance(message, list):
            message.append(corrections_message)
        else:
            message = [message, corrections_message]

    corrected_text = " ".join(corrected_words)
    return corrected_text, " ".join(message)

def query_expansion(query,max_cap = 2):
    stemmer = SnowballStemmer("english")
    tokens = nltk.word_tokenize(query)
    original_words = set(tokens)
    filtered_words = [word for word in tokens if word not in STOPWORDS]
    pos = nltk.pos_tag(filtered_words)

    synonyms_set = set()
    synset_cache = {}

    for item, (word, tag) in zip(filtered_words, pos):
        currentPOS = _get_wordnet_pos(tag)
        if item in synset_cache:  # 检查是否已缓存同义词集
            synsets = synset_cache[item]
        else:
            synsets = wordnet.synsets(item, pos=currentPOS) or wordnet.synsets(stemmer.stem(item), pos=currentPOS)
            synset_cache[item] = synsets  # 缓存同义词集

        counter = 0  # 初始化同义词计数器
        for synset in synsets:
            if counter >= max_cap:  # 检查是否达到同义词添加上限
                break
            for lemma in synset.lemmas():
                synonym = lemma.name().replace("_", " ")
                if synonym not in original_words and synonym not in synonyms_set:
                    synonyms_set.add(synonym)
                    counter += 1  # 更新同义词计数器
                    if counter >= max_cap:  # 再次检查以便提前退出
                        break

        # 移除原查询中已有的词汇
    extensions = list(synonyms_set - original_words)

    return extensions


# 测试预处理模块
# query = "This is a test query to check how the gril module wirks when the input has more than twenty words"
query = "Hallo My name is Yuan Liu"
preprocessed_query = preprocess_query(query)
corrected_query, message = correct_spelling2(preprocessed_query)
print("Processed query:", corrected_query)
print(message)


# 测试预处理模块
# query = "This is a test query to check how the preprocessing module works when the input has more than twenty words"
# corrected_query, message = preprocess_query(query)
# print("Processed query:", corrected_query)
# print(message)

# print("Message:", message)

end_time = time.time()  # 获取当前时间
print(f"Execution time: {end_time - start_time} seconds")
