#!/usr/bin/env bash
git clone https://github.com/tensorflow/tensorflow.git &&
cd tensorflow
./tensorflow/lite/tools/make/download_dependencies.sh\n
./tensorflow/lite/tools/make/build_rpi_lib.sh
