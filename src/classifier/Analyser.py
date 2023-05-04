import os

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from starlette.responses import FileResponse

from src.api.utils.Exceptions import no_model
from src.api.utils.TextPreProcessor import TextPreProcessor


class Analyser:
    lda_model = None
    dictionary = None

    def __init__(self, model_id):
        self.pre_processor = TextPreProcessor()
        self.model_id = model_id
        self.ld_avis_data_filepath = os.path.join('warehouse/ldavis_prepared_' + str(self.model_id))

        self.__check_model()
        self.load_model()

    def __get_visualization_path(self):
        return 'warehouse/ldavis_prepared_' + str(self.model_id) + '.html'

    def __check_model(self):
        if not os.path.exists(self.ld_avis_data_filepath+'.html'):
            raise no_model

    def load_model(self):
        self.lda_model = LdaModel.load(self.ld_avis_data_filepath + '_model')
        self.dictionary = Dictionary.load(self.ld_avis_data_filepath + '_dictionary')

    def get_model(self):
        file_path = self.__get_visualization_path()
        return FileResponse(file_path, filename="index.html", media_type="text/html")

    def define_text(self, text: str):
        processed_text = self.pre_processor.process(text)[0]
        bow_vector = self.dictionary.doc2bow(processed_text)
        topic_probabilities = self.lda_model.get_document_topics(bow_vector)
        return topic_probabilities
