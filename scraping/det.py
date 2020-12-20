import cv2
import numpy as np
import requests
import os.path


def findObjects(img):

    if not os.path.isfile('coco.names'):
        r = requests.get('https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names', allow_redirects=True)
        open('coco.names', 'wb').write(r.content)

    if not os.path.isfile('yolov3.cfg'):
        r = requests.get('https://opencv-tutorial.readthedocs.io/en/latest/_downloads/10e685aad953495a95c17bfecd1649e5/yolov3.cfg', allow_redirects=True)
        open('yolov3.cfg', 'wb').write(r.content)

    if not os.path.isfile('yolov3.weights'):
        r = requests.get('https://pjreddie.com/media/files/yolov3.weights', allow_redirects=True)
        open('yolov3.weights', 'wb').write(r.content)

    whT = 320
    confTreshold = 0.5
    nmsTreshold = 0.3

    classesFile = 'coco.names'
    classNames = []
    with open(classesFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    modelConfiguration = 'yolov3.cfg'  # 'yolov3-tiny.cfg'
    modelWeights = 'yolov3.weights'  # 'yolov3-tiny.weights'

    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)

    layerNames = net.getLayerNames()

    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]

    outputs = net.forward(outputNames)

    hT, wT, cT = img.shape
    bbox = []

    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confTreshold:
                w, h = int(det[2]*wT), int(det[3]*hT)
                x, y = int((det[0]*wT) - w/2), int((det[1]*hT) - h/2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(bbox, confs, confTreshold, nmsTreshold)

    cls = []
    for i in indices:
        i = i[0]
        cls.append(classNames[classIds[i]])
    return cls


imga = 'q.jpg'
img = cv2.imread(imga)

print(findObjects(img))
