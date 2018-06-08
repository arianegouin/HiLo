import csv
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os


class CSVFile:

    def __init__(self):
        self.directory = directory = os.fsencode(directory_in_str)
        self.filename = os.path.basename(root.PathAndFilename)

    def iterateCSVThroughFolder(self):
        # directory = CSVFile.getFilePath()[0]
        # print(directory)
        for file in os.listdir(self.directory):
            filename = os.fsdecode(file)
            if filename.endswith(".csv"):
                print('ok')
                print(os.path.join(self.directory, filename))
                # return os.path.join(directory, filename)
                continue
            else:
                print('no')
                continue

    def read(self):
        with open(self.name) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                yield row

    def getData(self):
        xdata = []
        ydata = []
        for row in self.read():
            try:
                float(row[0])
            except ValueError:
                continue
            else:
                print(row)
            yield xdata, ydata


root = tk.Tk()
root.withdraw()
root.PathAndFilename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select HDF5 file",
                                                  filetypes=(("CSVfiles", "*.csv"), ("all files", "*.*")))
directory = os.path.split(root.PathAndFilename)[0] + '/'
filename = os.path.basename(root.PathAndFilename)

print(filename)

# for i in x.read():
#     print(i)
