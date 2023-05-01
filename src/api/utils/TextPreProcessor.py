from typing import List

from nltk import word_tokenize, SnowballStemmer, pos_tag
from nltk.corpus import stopwords


class TextPreProcessor:
    stop_words = stopwords.words('english')
    tags = []

    def __init__(self, stop_words=None, tags=None):
        if tags is None:
            self.tags = ['NN', 'JJ']
        else:
            self.tags = tags

        if stop_words is not None:
            self.stop_words.extend(stop_words)

    def process(self, texts) -> List[str]:
        stemmer = SnowballStemmer('english')
        result = []
        for doc in texts:
            # Токенизация
            try:
                words = word_tokenize(doc.lower())
            except AttributeError:
                continue
            # Определение частей речи
            tagged_words = pos_tag(words)
            # Оставляем только существительные и прилагательные
            filtered_words = [word for word, tag in tagged_words if tag in self.tags]
            # Удаление стоп-слов
            filtered_words = [word for word in filtered_words if
                              word not in self.stop_words and word.isalpha and len(word) > 3]
            # Применение стеммера
            filtered_words = [stemmer.stem(word) for word in filtered_words]
            result.append(filtered_words)
        return result