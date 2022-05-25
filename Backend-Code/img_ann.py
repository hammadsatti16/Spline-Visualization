import PIL
import json
import cv2

def data(annotation):
    f = open(annotation)
    annotation = json.load(f)
    return annotation
def ann_file(annotation):
    annotation1 = annotation["annotations"][0]["shape"]
    return annotation1