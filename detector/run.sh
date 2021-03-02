#!/usr/bin/env bash
echo "Download all the dependencies"
echo "Download utilities"
apt update
apt-get install -y --no-install-recommends \
	git \
	wget \
        libhdf5-dev \  
	libhdf5-serial-dev \
       	libatlas-base-dev \
       	libjasper-dev \
      	libqtgui4 \
      	libqt4-test \

echo "Download tensorflow"
source prepare_tensorflow.sh
echo "Download OpenALPR"
source prepare_openalpr.sh
echo "Create environment"
python3.7 -m venv .env
source .env/bin/activate
echo "Install dependencies"
pip install -r requirements.lock
echo "Run the detection engine model"
if [$0 == 'tensorflow']
then
    /usr/bin/python3 stc/openALPR_tensorflow.py --modeldir model --graph detect.tflite  --threshold 0.3 --mode 0 --labels model/labelmap.txt
else
    /usr/bin/python3 stc/openALPR.py --mode 0
fi
