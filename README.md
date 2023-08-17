# Neurapi

![Flowcharts](https://github.com/vitor-martinsb/BCI_OB-RP3/assets/59899402/dad3c8e3-5c4d-4bc6-91e7-1b31e0d65ac0)

Thank you for visiting the Neurapi repository. This Python code is designed for use with the OpenBCI interface on Raspberry Pi 3.

## Table of Contents

- [Python Libraries and OpenBCI](#python-libraries-and-openbci)
- [Setting Up Raspberry Pi](#setting-up-raspberry-pi)
- [Code](#code)
- [Datasets](#datasets)

## Python Libraries and OpenBCI

This repository contains the necessary code and instructions for setting up a Brain-Computer Interface (BCI) system using Python and OpenBCI. The required Python libraries can be installed via PyPi. To install these libraries, you can use the following terminal commands:

```bash
pip3 install matplotlib
pip3 install numpy
pip3 install pylsl
pip3 install python-osc
pip3 install pyserial
pip3 install requests
pip3 install socketIO-client
pip3 install websocket-client
pip3 install wheel
pip3 install Yapsy
pip3 install xmltodict
pip3 install scipy
pip3 install openbci-python
```

## Setting Up Raspberry Pi

The ARM architecture does not compile the file `liblsl32.so` which is present in the pylsl library, responsible for data transmission. Follow these steps to replace the file:

1. [Download the replacement file (liblsl-bcm2708.so)](link_to_download).

2. Unpack the downloaded file.

3. Use the following terminal command to replace the file:
   ```bash
   mv <path_to>/liblsl-bcm2708.so <pylsl_path>/liblsl32.so
   ```

 Please replace `link_to_download` with the actual URL to download the replacement file.

 # BCI System README

## Code

Download the necessary code from this [link](link_to_code). This folder contains all the required files for the BCI system. The "offline" folder does not include the code for the 16-electrode online system. To set up and run the complete system, use the "stream_online.py" code located in the "online/scripts" directory. This code orchestrates other functions. If you need to change essential information (acquisition count, electrode count, etc.), make changes in the "main.py" and "stream_time.py" programs.

- `stream_online.py`: Responsible for online data acquisition and classification, executing "main.py" and "stream_time.py".
- `main.py`: Manages offline data windowing, filtering, and classification.
- `stream_time.py`: Handles data acquisition and prepares the training dataset.

Control variables for the BCI in the "stream_online.py" program have values of 1 or 0:

- `treino`: Enables system acquisition to generate training data (used in "stream_time.py").
- `aplica_filtro`: Applies filtering and performs offline BCI with or without attribute selection (used in "main.py").
- `classifica_online`: Conducts online BCI acquisitions based on the specified number.

Adjust the `runfiles` paths in the "stream_time.py" code if necessary, indicating the locations of "main.py" and "stream_time.py". Configuration changes (frequency count, electrode count, acquisition count, etc.) should primarily be made in these three programs using variables at the beginning of each.

## Datasets

The system offers 8 datasets (four with 8 electrodes and four with 16 electrodes), both with original and filtered signals. Directories for each acquisition are as follows:

- `/online/scripts/Data_record/V_1_16`
- `/online/scripts/Data_record/V_2_16`
- `/online/scripts/Data_record/V_3_16`
- `/online/scripts/Data_record/V_4_16`
- `/online/scripts/Data_record/V_1_8`
- `/online/scripts/Data_record/V_2_8`
- `/online/scripts/Data_record/V_3_8`
- `/online/scripts/Data_record/C_1_8`
