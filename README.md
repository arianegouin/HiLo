# HiLo

*Je dédie ce readme à Ludo.*

Python files should be run in this order:

### 1. PlotIntensityAgainstTime.py (optional)  
- input with pop-up window: folder path of the acquired tiff images[1]  
- input with python console: exposure time in ms, folder path for the pyplot figure, name for the pyplot figure  
- output: Sum all the pixel values for each image of the stack and divide them with their mean. Return the graph against the time. Save the pyplot figure.  

### 2. NormaliseAndSave.py  
- input with pop-up window: folder path of the acquired tiff images[1]  
- output: Divide each image by its mean. Then divide all images by the z-stack mean. Save each image in a folder named 'normalised' that is created in the folder chosen as input earlier. Each normalised image has the same name as its original image. 

### 3. StdevAndSave.py  
- input with pop-up window: folder path containing the normalised tiff images[1]
- input with python console: folder path for the tiff image, name for the tiff image[2]  
- output: Compute the standard deviation for each pixel through the Z-stack (along Z axis). Save the data as a tiff image.  

### 4. PlotHistogram.py (optional)  
- input with pop-up window: folder path of the tiff images containing their standard deviations  
- output: Return the histogram of standard deviations for each image. Save the pyplot figures in the same folder with the same names as the input tiff images.  

### 5. PlotStdevAgainstTime.py  
- input with pop-up window: folder path of the tiff images containing the standard deviations[2]  
- output: Return the graph of standard deviations against the exposure time.  

### Notes
- hilo.py contains all Classes
- 'optional' means subsequent py can be run without. It usually plots something to help visualise what has happened.
- [1] The tiff images should be named: *0.tiff*, *1.tiff*, *2.tiff*, etc.
- [2] The name should contain the illumination type (*speckles* or *uniform*) and the exposure time (in ms). It could have other words but no other numbers. E.g.: *200ms speckles.tiff*, *uniform 400 blabla.tiff*. This is important for the PlotStdevAgainstTime.py to run correctly.
