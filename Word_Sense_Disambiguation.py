import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.tag import pos_tag
from pywsd.lesk import simple_lesk


# 确保已经下载了必要的nltk资源
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

def get_wordnet_pos(treebank_tag):
    """Converts treebank tags to WordNet tags."""
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return None


def find_polysemous_words(sentence):
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    polysemous_words = []

    for word, tag in tagged_words:
        wn_tag = get_wordnet_pos(tag)
        if wn_tag:
            synsets = wn.synsets(word, pos=wn_tag)
            if len(synsets) > 1:  # 判断是否为多义词
                polysemous_words.append((word, tag, len(synsets)))

    return polysemous_words


def disambiguate_sentence(sentence):
    polysemous_words = find_polysemous_words(sentence)
    disambiguated_words = []

    for word, tag, _ in polysemous_words:
        wn_tag = get_wordnet_pos(tag)
        meaning = simple_lesk(sentence, word, pos=wn_tag)
        if meaning:
            disambiguated_words.append((word, meaning.definition()))

    return disambiguated_words


# 示例句子
sentence = "I went to the bank to deposit my money"
disambiguated_words = disambiguate_sentence(sentence)
for word, meaning in disambiguated_words:
    print(f"'{word}': {meaning}")

print(disambiguated_words)
