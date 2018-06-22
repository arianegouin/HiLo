# HiLo

hilo.py contains class

Python files should be run in this order.
1. PlotIntensityAgainstTime.py
  input with pop-up window: folder path containing the acquired tiff images
  input with python console: exposure time in seconds, folder path where to save the pyplot figure, name for the pyplot figure
  output: Sums all the pixel values for each image of the stack. Returns the graph of the sum of intensity against the time. Saves the pyplot figure.
2. NormaliseAndSave.py
  input with pop-up window: folder path containing the acquired tiff images
  output: for each stack, divideos each pixel by the sum of intensity for this stack. Saves each stack in a folder named 'normalised' and that is created in the folder chosen as input earlier.
3. StdevAndSave.py
  input with pop-up window: folder path containing the *normalised* tiff images
  input with python console: folder path where to save the tiff images of standard deviations, name for the tiff image *(nb. My code assumes it contains the illumination type ('speckles' or 'uniform') and the exposure time (in ms). Good e.g.: '200ms speckles.tiff' 'uniform 400.tiff'. This is important for the PlotStdevAgainstTime.py to run correctly.)*
  output: Computes the standard deviation for each pixel through the Z-stack. Saves the data as a tiff image.
4. PlotHistogram.py
  input with pop-up window: file path of the tiff image contaning the standard deviations
  output: Returns the *histogram* of all standard deviations. Saves the pyplot figure in the same folder as the input file.
5. PlotStdevAgainstTime.py
  input with pop-up window: folder path containing the tiff images of the standard deviations
  output: Returns the graph of standard deviations against the *exposure time*.
