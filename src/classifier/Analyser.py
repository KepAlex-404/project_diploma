import os

from gensim.corpora import Dictionary
from gensim.models import LdaModel

from src.api.utils.TextPreProcessor import TextPreProcessor


class Analyser:
    lda_model = None
    dictionary = None

    def __init__(self, model_id):
        self.pre_processor = TextPreProcessor()
        self.model_id = model_id
        self.load_model()

    def get_visualization_path(self):
        return 'warehouse/ldavis_prepared_' + str(self.model_id) + '.html'

    def load_model(self):
        ld_avis_data_filepath = os.path.join('warehouse/ldavis_prepared_' + str(self.model_id))
        self.lda_model = LdaModel.load(ld_avis_data_filepath + '_model')
        self.dictionary = Dictionary.load(ld_avis_data_filepath + '_dictionary')

    def define_text(self, text: str):
        processed_text = self.pre_processor.process(text)[0]
        bow_vector = self.dictionary.doc2bow(processed_text)
        topic_probabilities = self.lda_model.get_document_topics(bow_vector)
        return topic_probabilities
