# HiLo

*Je dédie ce readme à Ludo.*

Python files should be run in this order:

### 1. PlotIntensityAgainstTime.py (optional)  
- input with pop-up window: folder path of the acquired tiff images[1], folder path where to save the pyplot figure  
- input with python console: exposure time in ms, illumination type (*speckles* or *uniform*)  
- output: Sum all pixel values for each image of the stack and divide a stack by its mean. Return the graph against the time. Save the pyplot figure as *{exposure time}ms {illumination type}.png*.  

### 2. NormaliseAndSave.py  
- input with pop-up window: folder path of the acquired tiff images[1]  
- output: Divide each image by its mean. Then divide all images by the z-stack mean. Save each image in a folder named 'normalised' that is created in input folder. Each normalised image has the same name as its original image. 

### 3. StdevAndSave.py  
- input with pop-up window: folder path containing the normalised tiff images[1], folder path where to save the tiff image  
- input with python console: exposure time in ms, illumination type (*speckles* or *uniform*) 
- output: Compute the standard deviation for each pixel through the Z-stack (along Z axis). Save the data as a tiff image with name *{exposure time}ms {illumination type}.tiff*

### 4. PlotHistogram.py (optional)  
- input with pop-up window: folder path of the tiff images containing standard deviations[2]
- output: Return the histogram of standard deviations for each image. Save the pyplot figures in the same folder with the same names as the input tiff images.  

### 5. PlotStdevAgainstExposureTime.py  
- input with pop-up window: folder path of the tiff images containing the standard deviations[2]
- output: Return the graph of standard deviations against the exposure time. Save the pyplot figure in the input folder with name *#ALL*.

### Notes
- hilo.py contains all Classes
- 'optional' means you can skip this py and go run the next py without problems. It usually plots something to help visualise what has happened.
- [1] The tiff images should be named: *0.tiff*, *1.tiff*, *2.tiff*, etc.
- [2] The tiff images should be named: *{exposure time}ms {illumination type}.tiff*
