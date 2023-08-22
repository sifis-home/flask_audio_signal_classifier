FROM quay.io/codait/max-base:v1.4.0

ARG model_bucket=https://codait-cos-max.s3.us.cloud-object-storage.appdomain.cloud/max-audio-classifier/1.0.0
ARG model_file=assets.tar.gz

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=assets/${model_file} && \
  tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# check file integrity
RUN sha512sum -c sha512sums.txt

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]