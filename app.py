
from maxfw.core import MAXApp
from api import ModelMetadataAPI, ModelPredictAPI
from config import API_TITLE, API_DESC, API_VERSION

max_app = MAXApp(API_TITLE, API_DESC, API_VERSION)
max_app.add_api(ModelMetadataAPI, '/metadata')
# max_app.add_api(ModelPredictAPI, '/predict')
max_app.add_api(ModelPredictAPI, '/predict/<audio_file>/<method>/<requestor_id>/<requestor_type>/<request_id>')
max_app.run()
