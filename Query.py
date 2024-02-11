import nltk
from nltk import SnowballStemmer
from nltk.corpus import stopwords, wordnet
from textblob import TextBlob
import time
from spellchecker import SpellChecker
import re

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

spell = SpellChecker()
start_time = time.time()  # 获取当前时间
STOPWORDS = set(stopwords.words('english'))


def preprocess_query(query):
    query = query.lower()
    query = re.sub(r'[^\w\s]', '', query)
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

def _get_wordnet_pos(tag: str) -> str:
    if tag[1].startswith('J'):
        return wordnet.ADJ
    elif tag[1].startswith('N'):
        return wordnet.NOUN
    elif tag[1].startswith('R'):
        return wordnet.ADV
    elif tag[1].startswith('V'):
        return wordnet.VERB
    else:
        return ''

def query_expansion(query,max_cap = 2):
    stemmer = SnowballStemmer("english")
    tokens = nltk.word_tokenize(query)
    original_words = set(tokens)
    filtered_words = [word for word in tokens if word not in STOPWORDS]
    pos = nltk.pos_tag(filtered_words)

    synonyms_set = set()
    synset_cache = {}

    def add_synonyms(item, synsets):
        counter = 0
        for synset in synsets:
            for lemma in synset.lemmas():
                synonym = lemma.name().replace("_", " ")
                if synonym not in original_words and synonym not in synonyms_set:
                    synonyms_set.add(synonym)
                    counter += 1
                    if counter >= max_cap:
                        return  # 提前返回以跳出函数

    for item, (word, tag) in zip(filtered_words, pos):
        currentPOS = _get_wordnet_pos(tag)
        if item in synset_cache:
            synsets = synset_cache[item]
        else:
            synsets = wordnet.synsets(item, pos=currentPOS) or wordnet.synsets(stemmer.stem(item), pos=currentPOS)
            synset_cache[item] = synsets

        add_synonyms(item, synsets)  # 封装的添加同义词逻辑

    extensions = list(synonyms_set - original_words)

    return extensions



# 测试全部模块
query = "Machine learning computer science Machine Machine Machine Machine Machine Machine Machine Machine Machine Machine"
# query = "Hallo My name is Yuan Liu"
preprocessed_query = preprocess_query(query)
corrected_query, message = correct_spelling(preprocessed_query)
print("Processed query:", corrected_query)
print(message)
print(query_expansion(corrected_query))

#  测试预处理模块
# query = "This is a test query to check how the preprocessing module works when the input has more than twenty words"
# corrected_query, message = preprocess_query(query)
# print("Processed query:", corrected_query)
# print(message)

# print("Message:", message)


end_time = time.time()  # 获取当前时间
print(f"Execution time: {end_time - start_time} seconds")
