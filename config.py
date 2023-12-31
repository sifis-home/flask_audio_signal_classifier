
# Flask settings
DEBUG = True

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False

# Application settings

# API metadata
API_TITLE = 'MAX Audio Classifier'
API_DESC = 'Identify sounds in short audio clips'
API_VERSION = '1.2.0'

# default model
MODEL_NAME = 'audio_embeddings'
MODEL_LICENSE = 'Apache 2.0'

MODEL_META_DATA = {
    'id': '{}-tf-imagenet'.format(MODEL_NAME.lower()),
    'name': '{} TensorFlow Model'.format(MODEL_NAME),
    'description': '{} TensorFlow model trained on Audio Set'.format(MODEL_NAME),
    'type': 'image_classification',
    'license': '{}'.format(MODEL_LICENSE)
}

DEFAULT_EMBEDDING_CHECKPOINT = "assets/vggish_model.ckpt"
DEFAULT_PCA_PARAMS = "assets/vggish_pca_params.npz"
DEFAULT_CLASSIFIER_MODEL = "assets/classifier_model.h5"
