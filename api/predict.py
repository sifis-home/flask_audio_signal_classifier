import re
from core.model import ModelWrapper
from flask_restplus import fields
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest
from maxfw.core import MAX_API, PredictAPI

import os
import datetime
import hashlib
import platform

import random
from pydub import AudioSegment
import io

import numpy as np
from scipy import signal
import soundfile as sf
import io

# set up parser for audio input data
input_parser = MAX_API.parser()
input_parser.add_argument('audio', type=FileStorage, location='files', required=True,
                          help="signed 16-bit PCM WAV audio file")
input_parser.add_argument('start_time', type=float, default=0,
                          help='The number of seconds into the audio file the prediction should start at.')
input_parser.add_argument('filter', required=False, action='split', help='List of labels to filter (optional)')

label_prediction = MAX_API.model('LabelPrediction', {
    'label_id': fields.String(required=False, description='Label identifier'),
    'label': fields.String(required=True, description='Audio class label'),
    'probability': fields.Float(required=True)
})

predict_response = MAX_API.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message'),
    'predictions': fields.List(fields.Nested(label_prediction), description='Predicted audio classes and probabilities'),
    'audio_file': fields.String(required=True, description='The passed audio file.'),
    'method': fields.String(required=True, description='The passed privacy method.'),
    'requestor_id': fields.String(required=True, description='The passed requestor_id.'),
    'requestor_type': fields.String(required=True, description='The passed requestor_type.'),
    'request_id': fields.String(required=True, description='The passed request_id.'),
    'analyzer_id': fields.String(required=True, description='The analyzer_id.'),
    'analysis_id': fields.String(required=True, description='The analysis_id.')
})


def scrample(audio_file_data):

    audio_data = AudioSegment.from_wav(audio_file_data)

    # Shuffle the audio segments
    segment_duration = 1000  # Duration of each segment in milliseconds
    segments = [audio_data[i:i+segment_duration] for i in range(0, len(audio_data), segment_duration)]
    random.shuffle(segments)
    scrambled_audio = AudioSegment.empty()
    for segment in segments:
        scrambled_audio += segment

    # Convert audio to raw data
    audio_buffer = io.BytesIO()
    scrambled_audio.export(audio_buffer, format='wav')
    audio_buffer.seek(0)
    audio_raw = audio_buffer.read()
    
    return audio_raw

def dp_noise(audio_file_data):

    # define the privacy budget and sensitivity
    epsilon = 0.8
    sensitivity = 0.05

    # read the original audio signal from file
    audio_data, sample_rate = sf.read(audio_file_data)

    # generate noise with Laplace distribution
    scale = sensitivity / epsilon
    noise = np.random.laplace(loc=0, scale=scale, size=len(audio_data))

    # add the noise to the audio signal
    noisy_audio = audio_data + noise
    # noisy_audio = audio_data + noise[:, np.newaxis]

    # apply a low-pass filter to smooth the noise
    b, a = signal.butter(4, 4000/(sample_rate/2), 'lowpass')
    smoothed_audio = signal.filtfilt(b, a, noisy_audio)

    # convert audio to raw data
    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, noisy_audio, sample_rate, format='WAV', subtype='PCM_16')
    audio_buffer.seek(0)
    audio_raw = audio_buffer.read()

    return audio_raw


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    @MAX_API.marshal_with(predict_response)
    def post(self, audio_file, method, requestor_id, requestor_type, request_id):
        analyzer_id = platform.node()

        # Get current date and time
        now = datetime.datetime.now()

        # Generate a random hash using SHA-256 algorithm
        hash_object = hashlib.sha256()
        hash_object.update(bytes(str(now), 'utf-8'))
        hash_value = hash_object.hexdigest()

        # Concatenate the time and the hash
        analysis_id = str(analyzer_id) + str(now) + hash_value

        # def post(self):
        """Predict audio classes from input data"""
        result = {'status': 'error'}

        args = input_parser.parse_args()

        if not re.match("audio/.*wav", str(args['audio'].mimetype)):
            e = BadRequest()
            e.data = {'status': 'error', 'message': 'Invalid file type/extension: ' + str(args['audio'].mimetype)}
            raise e

        # audio_data = args['audio'].read()

        
        audio_file = args['audio']

        if method == "scrample":
            audio_data = scrample(audio_file)
        elif method == "dp_noise":
            audio_data = dp_noise(audio_file)
        else:
            audio_data = args['audio'].read()



        # Getting the predictions
        try:
            preds = self.model_wrapper._predict(audio_data, args['start_time'])
        except ValueError:
            e = BadRequest()
            e.data = {'status': 'error', 'message': 'Invalid start time: value outside audio clip'}
            raise e

        # Aligning the predictions to the required API format
        label_preds = [{'label_id': p[0], 'label': p[1], 'probability': p[2]} for p in preds]

        # Filter list
        if args['filter'] is not None and any(x.strip() != '' for x in args['filter']):
            label_preds = [x for x in label_preds if x['label'] in args['filter']]

        result['predictions'] = label_preds
        result['status'] = 'ok'
        result['audio_file'] = audio_file
        result['method'] = method
        result['requestor_id'] = requestor_id
        result['requestor_type'] = requestor_type
        result['request_id'] = request_id
        result['analyzer_id'] = analyzer_id
        result['analysis_id'] = analysis_id

        ws_req_final = {
                        "RequestPostTopicUUID": {
                        "topic_name": "SIFIS:Privacy_Aware_Audio_Anomaly_Detection_Results",
                        "topic_uuid": "Audio_Anomaly_Detection_Results",
                        "value": {
                            "description": "Speech Recognition Results",
                            "requestor_id": str(requestor_id),
                            "requestor_type": str(requestor_type),
                            "request_id": str(request_id),
                            "analyzer_id": str(analyzer_id),
                            "analysis_id": str(analysis_id),
                            "audio_file": str(audio_file),
                            "method": str(method),
                            "predictions": label_preds
                        }
                    }
                }


        return result
