import os
import json
import jsonpickle
import tkinter
from tkinter import Tk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from Utility.Utilities import *
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def strToFloat(numberString):
    charFreeStr = ''.join(ch for ch in numberString if ch.isdigit() or ch == '.' or ch == ',')
    return float(locale.atof(charFreeStr))


def validStringNumberRange(numberString, minimumValue, maximumValue):
    if minimumValue <= strToFloat(numberString) <= maximumValue:
        return True
    return False


def hide_AdvancedOptions(win):
    if 'showPlots_Label' in win.children:
        win.children['showPlots_Label'].destroy()
        win.children['showPlots_YesButton'].destroy()
        win.children['showPlots_NoButton'].destroy()
        win.children['showBoundingBoxPlots_Label'].destroy()
        win.children['showBoundingBoxPlots_YesButton'].destroy()
        win.children['showBoundingBoxPlots_NoButton'].destroy()
        win.children['plotPolylidar_Label'].destroy()
        win.children['plotPolylidar_YesButton'].destroy()
        win.children['plotPolylidar_NoButton'].destroy()
        win.children['parallelProcessing_Label'].destroy()
        win.children['parallelProcessing_YesButton'].destroy()
        win.children['parallelProcessing_NoButton'].destroy()


def show_AdvancedOptions(win, showPlotsVar, showBoundingBoxPlotsVar, plotPolylidarVar, parallelProcessingVar):
    if 'showPlots_Label' not in win.children:
        initialRow = 11
        tkinter.Label(win, text="Show Intermediate Plots?", name='showPlots_Label').grid(row=initialRow, column=0)
        r1showPlots = tkinter.Radiobutton(win, text="Yes", variable=showPlotsVar, value=1, name='showPlots_YesButton')
        r2showPlots = tkinter.Radiobutton(win, text="No", variable=showPlotsVar, value=0, name='showPlots_NoButton')
        r1showPlots.grid(row=initialRow, column=1)
        r2showPlots.grid(row=initialRow, column=2)
        tkinter.Label(win, text="Show BoundingBox Plots?", name='showBoundingBoxPlots_Label').grid(row=initialRow+1, column=0)
        r1showBoundingBoxPlots = tkinter.Radiobutton(win, text="Yes", variable=showBoundingBoxPlotsVar, value=1, name='showBoundingBoxPlots_YesButton')
        r2showBoundingBoxPlots = tkinter.Radiobutton(win, text="No", variable=showBoundingBoxPlotsVar, value=0, name='showBoundingBoxPlots_NoButton')
        r1showBoundingBoxPlots.grid(row=initialRow+1, column=1)
        r2showBoundingBoxPlots.grid(row=initialRow+1, column=2)
        tkinter.Label(win, text="Show Polylidar Point Plot?", name='plotPolylidar_Label').grid(row=initialRow+2, column=0)
        r1plotPolylidar = tkinter.Radiobutton(win, text="Yes", variable=plotPolylidarVar, value=1, name='plotPolylidar_YesButton')
        r2plotPolylidar = tkinter.Radiobutton(win, text="No", variable=plotPolylidarVar, value=0, name='plotPolylidar_NoButton')
        r1plotPolylidar.grid(row=initialRow+2, column=1)
        r2plotPolylidar.grid(row=initialRow+2, column=2)
        tkinter.Label(win, text="Use parallelization?", name='parallelProcessing_Label').grid(row=initialRow+3, column=0)
        r1parallelProcessing = tkinter.Radiobutton(win, text="Yes", variable=parallelProcessingVar, value=1, name='parallelProcessing_YesButton')
        r2parallelProcessing = tkinter.Radiobutton(win, text="No", variable=parallelProcessingVar, value=0, name='parallelProcessing_NoButton')
        r1parallelProcessing.grid(row=initialRow+3, column=1)
        r2parallelProcessing.grid(row=initialRow+3, column=2)
    else:
        hide_AdvancedOptions(win)


def get_file(entryField, entryFieldText, titleMessage, fileFormatsStr):
    listName = getFileOrDir('file', titleMessage, fileFormatsStr, entryFieldText.get().replace('~', os.path.expanduser('~')))
    entryFieldText.set(listName.replace(os.path.expanduser('~'), '~'))
    entryField.config(width=len(listName.replace(os.path.expanduser('~'), '~')))


def preview_image(imageFilePath):
    inputImagePath = imageFilePath.get().replace('~', os.path.expanduser('~'))
    if inputImagePath.endswith(('.tiff', '.tif')):
        print("attempting to convert tiff to png")
        rawImage = Image.open(inputImagePath)
        npImage = ((np.array(rawImage) + 1) / 256) - 1
        visImage = Image.fromarray(np.uint8(npImage), mode='L')
        visImage.show()
    else:
        rawImage = Image.open(inputImagePath)
        rawImage.show()


def get_setupOptions(savedJSONFileName):
    try:
        with open(savedJSONFileName) as infile:
            inputFile = json.load(infile)
        setupOptions = jsonpickle.decode(inputFile)
    except FileNotFoundError:
        setupOptions = SetupOptions()
    return setupOptions


def on_closing(win, setupOptions, savedJSONFileName, ImageEntryText, scaleDictEntryText, modelEntryText, isVerticalSubSectionVar, centerFractionToMeasureVar, tiltAngleVar, showPlotsVar, showBoundingBoxPlotsVar, plotPolylidarVar, parallelProcessingVar, scaleBarWidthMicronsVar):
    setupOptions.imageFilePath = ImageEntryText.get().replace('~', os.path.expanduser('~'))
    setupOptions.scaleDictPath = scaleDictEntryText.get().replace('~', os.path.expanduser('~'))
    setupOptions.modelPath = modelEntryText.get().replace('~', os.path.expanduser('~'))
    setupOptions.isVerticalSubSection = isVerticalSubSectionVar.get()
    setupOptions.centerFractionToMeasure = strToFloat(centerFractionToMeasureVar.get())
    setupOptions.tiltAngle = strToFloat(tiltAngleVar.get())
    setupOptions.showPlots = showPlotsVar.get()
    setupOptions.showBoundingBoxPlots = showBoundingBoxPlotsVar.get()
    setupOptions.plotPolylidar = plotPolylidarVar.get()
    setupOptions.parallelProcessing = parallelProcessingVar.get()
    setupOptions.scaleBarWidthMicrons = strToFloat(scaleBarWidthMicronsVar.get())

    with open(savedJSONFileName, 'w') as outfile:
        json.dump(jsonpickle.encode(setupOptions), outfile)
    win.destroy()


def uiInput(win, setupOptions, savedJSONFileName):
    win.title("Spectrum Data Processing Setup UI")
    ImageEntryText = tkinter.StringVar(value=setupOptions.imageFilePath.replace(os.path.expanduser('~'), '~'))
    scaleDictEntryText = tkinter.StringVar(value=setupOptions.scaleDictPath.replace(os.path.expanduser('~'), '~'))
    modelEntryText = tkinter.StringVar(value=setupOptions.modelPath.replace(os.path.expanduser('~'), '~'))
    isVerticalSubSectionVar = tkinter.BooleanVar(value=setupOptions.isVerticalSubSection)
    scaleBarWidthMicronsVar = tkinter.StringVar(value=setupOptions.scaleBarWidthMicrons)
    centerFractionToMeasureVar = tkinter.StringVar(value=setupOptions.centerFractionToMeasure)
    tiltAngleVar = tkinter.StringVar(value=setupOptions.tiltAngle)

    showPlotsVar = tkinter.BooleanVar(value=setupOptions.showPlots)
    showBoundingBoxPlotsVar = tkinter.BooleanVar(value=setupOptions.showBoundingBoxPlots)
    plotPolylidarVar = tkinter.BooleanVar(value=setupOptions.plotPolylidar)
    parallelProcessingVar = tkinter.BooleanVar(value=setupOptions.parallelProcessing)

    tkinter.Label(win, text="Image File:").grid(row=0, column=0)
    ImageFileEntry = tkinter.Entry(win, textvariable=ImageEntryText)
    ImageFileEntry.grid(row=1, column=0)
    ImageFileEntry.config(width=len(setupOptions.imageFilePath.replace(os.path.expanduser('~'), '~')))
    ImageFileButton = tkinter.Button(win, text='Choose File', command=lambda: get_file(ImageFileEntry, ImageEntryText, 'Choose Image File', '.jpg .jpeg .png .tiff .tif'))
    ImageFileButton.grid(row=1, column=1)
    ImageFilePreviewButton = tkinter.Button(win, text='Preview', command=lambda: preview_image(ImageEntryText))
    ImageFilePreviewButton.grid(row=1, column=2)

    tkinter.Label(win, text="Scale Dict File:").grid(row=2, column=0)
    scaleDictEntry = tkinter.Entry(win, textvariable=scaleDictEntryText)
    scaleDictEntry.grid(row=3, column=0)
    scaleDictEntry.config(width=len(setupOptions.scaleDictPath.replace(os.path.expanduser('~'), '~')))
    scaleDictButton = tkinter.Button(win, text='Choose File', command=lambda: get_file(scaleDictEntry, scaleDictEntryText, 'Choose Scale Dict File', '.txt'))
    scaleDictButton.grid(row=3, column=1)

    tkinter.Label(win, text="Machine Learning Model:").grid(row=4, column=0)
    modelEntry = tkinter.Entry(win, textvariable=modelEntryText)
    modelEntry.grid(row=5, column=0)
    modelEntry.config(width=len(setupOptions.modelPath.replace(os.path.expanduser('~'), '~')))
    modelButton = tkinter.Button(win, text='Choose File', command=lambda: get_file(modelEntry, modelEntryText, 'Choose Machine Learning Model', '.pth'))
    modelButton.grid(row=5, column=1)

    tkinter.Label(win, text="Measure Widths or Lengths").grid(row=6, column=0)
    r1isXRD = tkinter.Radiobutton(win, text="Widths", variable=isVerticalSubSectionVar, value=1)
    r2isXRD = tkinter.Radiobutton(win, text="Lengths", variable=isVerticalSubSectionVar, value=0)
    r1isXRD.grid(row=6, column=1)
    r2isXRD.grid(row=6, column=2)

    tkinter.Label(win, text="Scale Bar Size (Microns)").grid(row=7, column=0)
    tiltAngleEntry = tkinter.Entry(win, textvariable=scaleBarWidthMicronsVar, validate='all', validatecommand=lambda: validStringNumberRange(scaleBarWidthMicronsVar.get(), 0, 1000))
    tiltAngleEntry.grid(row=7, column=1)

    tkinter.Label(win, text="Tilt Angle").grid(row=8, column=0)
    tiltAngleEntry = tkinter.Entry(win, textvariable=tiltAngleVar, validate='all', validatecommand=lambda: validStringNumberRange(tiltAngleVar.get(), -10, 90))
    tiltAngleEntry.grid(row=8, column=1)

    tkinter.Label(win, text="Center Fraction to Measure").grid(row=9, column=0)
    centerFractionToMeasureEntry = tkinter.Entry(win, textvariable=centerFractionToMeasureVar, validate='all', validatecommand=lambda: validStringNumberRange(centerFractionToMeasureVar.get(), 0, 1))
    centerFractionToMeasureEntry.grid(row=9, column=1)

    tkinter.Button(win, text='Show/Hide Advanced Options', command=lambda: show_AdvancedOptions(win, showPlotsVar, showBoundingBoxPlotsVar, plotPolylidarVar, parallelProcessingVar)).grid(row=10, column=1)

    hide_AdvancedOptions(win)
    win.protocol("WM_DELETE_WINDOW", lambda: on_closing(win, setupOptions, savedJSONFileName, ImageEntryText, scaleDictEntryText, modelEntryText, isVerticalSubSectionVar, centerFractionToMeasureVar, tiltAngleVar, showPlotsVar, showBoundingBoxPlotsVar, plotPolylidarVar, parallelProcessingVar, scaleBarWidthMicronsVar))
    win.mainloop()


def setupOptionsUI():
    savedJSONFileName = 'AnalyzeOutputSetupOptions.json'
    setupOptions = get_setupOptions(savedJSONFileName)  # Read previously used setupOptions
    uiInput(Tk(), setupOptions, savedJSONFileName)
    return setupOptions


# setupOptionsUI()