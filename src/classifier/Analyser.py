from fastapi.responses import FileResponse


class Analyser:

    def __init__(self, model_id):
        self.model_id = model_id

    def get_visualization_path(self):
        return 'warehouse/ldavis_prepared_' + str(self.model_id) + '.html'
