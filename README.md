# On-Device ML for ECE475

This repo contains code for going through the process of collecting data, training an ML model, and deploying it on an embedded system.

## Setup

Make sure to install Python dependencies according to `requirements.txt`.

## Record Data

Determine your device's serial port by running `ls /dev/tty*` or looking at the Arduino IDE.
Update `SERIAL_PORT_NAME` variable in `plot_and_record.py` with it.
Run the script with `python plot_and_record.py`.
This script will read lines of tab-separated values (e.g., `100\t200\300\t\n`) from the serial port and plot it live.
Press the buttons at the bottom to record data to be labeled with the corresponding text.
The data will be saved in `./data/`.
You may need to update `NUM_CHANNELS` if you have a different number of signals to plot.

Troubleshooting:
- If the script says the serial port is busy, make sure nothing else is accessing it (i.e., close the Arduino IDE).
- If nothing appears, try resetting the microcontroller.

## Training

This script reads all files in `./data/` and plots it for a quick overview visualization.
It then extracts 4 statistical features (min, max, mean, std) from each file.
First, the script splits the dataset into 50% for training and 50% for testing, and presents a confusion matrix on that evaluation.
Second, the script trains a model on the entire dataset and exports it as a C header file at `./out/model.h`.
Copy this header file to your Arduino code.

You will likely have to experiment with different features and/or models (i.e., SVM, decision tree, neural network) to achieve the best results on your dataset.
