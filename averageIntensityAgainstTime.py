import csv
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os


class CSVFile:

    def __init__(self, name):
        self.name = name

    @staticmethod
    def getFilePath():
        root = tk.Tk()
        root.withdraw()
        root.PathAndFilename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select HDF5 file",
                                                          filetypes=(("CSVfiles", "*.csv"), ("all files", "*.*")))
        directory = os.path.split(root.PathAndFilename)[0] + '/'
        fileName = os.path.basename(root.PathAndFilename)
        return directory + fileName

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
                pass
            else:
                print(row)
            yield xdata, ydata

x = CSVFile('Results.csv')
for i in x.read():
    print(i)
