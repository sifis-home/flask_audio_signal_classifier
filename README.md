# WP4 Analytic: Privacy-Aware Audio Signal Classifier

[![Actions Status][actions badge]][actions]
[![CodeCov][codecov badge]][codecov]
[![LICENSE][license badge]][license]

<!-- Links -->
[actions]: https://github.com/sifis-home/flask_audio_signal_classifier/actions
[codecov]: https://codecov.io/gh/sifis-home/flask_audio_signal_classifier
[license]: LICENSES/MIT.txt

<!-- Badges -->
[actions badge]: https://github.com/sifis-home/flask_audio_signal_classifier/workflows/flask_audio_signal_classifier/badge.svg
[codecov badge]: https://codecov.io/gh/sifis-home/flask_audio_signal_classifier/branch/master/graph/badge.svg
[license badge]: https://img.shields.io/badge/license-MIT-blue.svg

One valuable source of information for detecting anomalies is the audio signals captured within the smart home. Audio anomaly detection in smart homes adds an extra layer of protection, enabling early detection and response to potential threats, improving safety, and enhancing the overall quality of life for the occupants. Performing audio anomaly detection in smart homes enhances the overall safety and security of the occupants by identifying unusual or potentially dangerous events that may occur within the home environment. This includes detecting anomalies such as breaking glass, loud and sudden noises, unusual patterns of speech or conversation, or other signs of potential threats or emergencies. By continuously monitoring audio signals in the smart home, the system can quickly identify and raise an alert for any abnormal activities. 

The input data for audio anomaly detection in smart homes is the audio signals captured within the smart home environment. These audio signals can be obtained from various sources such as microphones or audio sensors deployed throughout the home. This analytic is designed to process WAV or FLAC audio samples with specific requirements, including a sampling rate of 16 kHz, a single channel (mono) audio represented in 16 bit. There is no specific duration requirement for the input audio files, but longer audio files may take more time to process, and extremely short audio snippets might not provide sufficient information for accurate classification. If the audio sample is in a different format, a preprocessing step may be necessary to adjust it to meet the input requirements of the analytic. 

We employ the [IBM MAX audio classification model](https://github.com/IBM/MAX-Framework) developed and maintained by IBM. This model is a multi-attention classifier designed to analyze and categorize audio data into various predefined classes or labels. The classifier leverages the power of deep neural networks to learn patterns and features from large-labeled audio datasets, allowing it to make predictions on new, unseen audio inputs. The core component of the IBM Audio Classifier is a deep neural network model. The architecture consists of multiple layers, such as convolutional layers, pooling, and fully connected layers. These layers are designed to learn hierarchical representations and capture relevant audio features for classification. The model output includes the top 5 class predictions along with their corresponding probabilities. The model is designed to support 527 classes, defined within the Audioset Ontology. 

The analytic generates the top 5 predictions or classifications, providing insights into the most probable classes or categories present in the input audio. For the purpose of audio anomaly detection, we have curated a specific set of classes that are indicative of abnormal behavior, including events like glass breaking, screaming, and fire. By leveraging these classifications, we can identify potential anomalies and assess whether the audio exhibits any concerning patterns or events. 

## Deploying

### Privacy-Aware Audio Signal Classifier
The DHT and the Analytics-API containers should be running before starting to build and run the image and container of the Privacy-Aware Audio Signal Classifier.

Privacy-Aware Audio Signal Classifier is intended to run in a docker container on port 5000. The Dockerfile at the root of this repo describes the container. To build and run it execute the following commands:

`docker build -t max-model .`

`docker-compose up`


## REST API of Privacy-Aware Audio Signal Classifier

Description of the REST endpoint available while Privacy-Aware Audio Signal Classifier is running.

---

#### GET /model/predict

Description: Returns the classification of sounds in an audio signal.

Command: 

`curl -F "file=@file_location;type=audio/wav" -XPOST http://localhost:5000/model/predict/anonymized_audio/<privacy_method>/<requestor_id>/<requestor_type>/<request_id>`

Sample: 

`curl -F "audio=@file_location;type=audio/wav" -XPOST http://localhost:5000/model/predict/anonymized_audio/scrample/33466553786f48cb72faad7b2fb9d0952c97/NSSD/2023061906001633466553786f48cb72faad7b2fb9d0952c97`

Sample: 

`curl -F "audio=@file_location;type=audio/wav" -XPOST http://localhost:5000/model/predict/anonymized_audio/dp_noise/33466553786f48cb72faad7b2fb9d0952c97/NSSD/2023061906001633466553786f48cb72faad7b2fb9d0952c97`

---
## License

Released under the [MIT License](LICENSE).

## Acknowledgements

This software has been developed in the scope of the H2020 project SIFIS-Home with GA n. 952652.