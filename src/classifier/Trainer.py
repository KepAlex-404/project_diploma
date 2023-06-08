import os

import gensim
import gensim.corpora as corpora
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from gensim.models import CoherenceModel

from src.api.utils.TextPreProcessor import TextPreProcessor


class Trainer:
    """
    Gives functionality to train new LDA models
    """
    corpus = None
    id2word = None
    num_topics = None
    lda_model = None

    def __init__(self, stop_words=None, tags=None, num_topics=10):
        self.pre_processor = TextPreProcessor(stop_words, tags)
        self.num_topics = num_topics

    @staticmethod
    def make_trigrams(data_words):
        # Build the bigram and trigram models
        bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)  # higher threshold fewer phrases.
        trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
        # Faster way to get a sentence clubbed as a trigram/bigram
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)

        def trigrams(texts):
            return [trigram_mod[bigram_mod[doc]] for doc in texts]

        # Form Bigrams
        data_words_trigrams = trigrams(data_words)
        return data_words_trigrams

    def save_model(self, model_id):
        ld_avis_data_filepath = os.path.join('warehouse/ldavis_prepared_' + str(model_id))
        # save LdaModel
        self.lda_model.save(ld_avis_data_filepath+'_model')
        # save Dictionary
        self.id2word.save(ld_avis_data_filepath+'_dictionary')

        lda_prepared = gensimvis.prepare(self.lda_model, self.corpus, self.id2word)
        pyLDAvis.save_html(lda_prepared, ld_avis_data_filepath+'.html')

    def build_model(self, model_id: str):
        # Build LDA model
        self.lda_model = gensim.models.LdaModel(corpus=self.corpus,
                                                id2word=self.id2word,
                                                num_topics=self.num_topics,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True
                                                )

        self.save_model(model_id)

    def process(self, data, model_id):
        data_words = self.pre_processor.process(data)
        data_words_trigrams = self.make_trigrams(data_words)
        self.id2word = corpora.Dictionary(data_words_trigrams)
        # Term Document Frequency
        self.corpus = [self.id2word.doc2bow(text) for text in data_words_trigrams]

        self.build_model(model_id)



