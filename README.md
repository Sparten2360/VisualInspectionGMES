# VisualInspectionGMES
This projects aims to bring highlevel OCR and inspection Capablites with a lowcost implementation. Runnable on a single board computer and black and white cameras with global shutter. The system uses easyOCR to detect text on the wire. Then Segments the image into digits to run EasyOCR on for better results. 
## Computer Configuration
Nesscary Installs:
To Run with CPU
-Python 3.12
-EasyOCR

-CUDA Toolkit 12.1
-Pytorch Compatiable with CUDA Toolkit 12.1
-
In order to run with the GPU enabled function on for EasyOCR you must have a cuda capibale GPU and the CUDA 12.1 toolkit installed.
