from maxfw.core import MAX_API, METADATA_SCHEMA, MetadataAPI

from core.model import ModelWrapper


class ModelMetadataAPI(MetadataAPI):
    @MAX_API.marshal_with(METADATA_SCHEMA)
    def get(self):
        """Return the metadata associated with the model"""
        return ModelWrapper.MODEL_META_DATA
