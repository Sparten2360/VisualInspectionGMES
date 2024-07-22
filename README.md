# VisualInspectionGMES
This projects aims to bring highlevel OCR and inspection Capablites with a lowcost implementation. Runnable on a single board computer and black and white cameras with global shutter. The system uses easyOCR to detect text on the wire. Then Segments the image into digits to run EasyOCR on for better results. 
## Computer Configuration
Nesscary Installs
To Run with CPU:
- Python 3.12
- EasyOCR

To Run With GPU:

- CUDA Toolkit 12.1
- Pytorch Compatiable with CUDA Toolkit 12.1 (if you've already installed EasyOCR uninstall before downloading Compatible Pytorch)

In order to run with the GPU enabled function on for EasyOCR you must have a cuda capibale GPU and the CUDA 12.1 toolkit installed.
## Instalation Procedure

1. DownLoad VisualInspectionRunScript.py
2. Plug in 5 cameras(Use USBC hub instead of USB 3.0 hub for connection so you aren't limited on bandwidth)
3. Run Script
4. Place Wire in view.

## Running and Results
The script will display a list of 4 digit footages it was able to detect while the wire was running. It will then take the mode of this list in order to return footage. 
