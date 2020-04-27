import os
import pickle
import numpy as np  # (pip install numpy)
from tkinter import Tk, filedialog


# basePath = "/home/mbraun/NewIS"
colabBasePath = "/content/drive/My Drive/NewIS"
root = Tk()
root.withdraw()
annotationDictFileName = filedialog.askopenfilename(filetypes=[("Text Dict","*.txt")])

if not annotationDictFileName:
    quit()

# loading a saved dict back in
with open(annotationDictFileName, 'rb') as handle:
   readDictList = pickle.loads(handle.read())

quit()
for segDict in readDictList:
    originalNamePath, _ = os.path.split(segDict['file_name'])
    originalNameParentFolderPath, _ = os.path.split(originalNamePath)
    originalNameBasePath, _ = os.path.split(originalNameParentFolderPath)

    originalImageIDPath, _ = os.path.split(segDict['image_id'])
    originalImageIDParentFolderPath, _ = os.path.split(originalImageIDPath)
    originalImageIDBasePath, _ = os.path.split(originalImageIDParentFolderPath)

    segDict['file_name'] = segDict['file_name'].replace(originalNameBasePath, colabBasePath)
    segDict['image_id'] = segDict['image_id'].replace(originalImageIDBasePath, colabBasePath)

# newAnnotationDictFileName = 'annotations_dict_bitmask_Train_colab.txt'
newAnnotationDictFileName = 'annotations_dict_bitmask_Validation_colab.txt'

with open(newAnnotationDictFileName, 'wb') as handle:
    pickle.dump(readDictList, handle)