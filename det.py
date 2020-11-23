import cv2
import numpy as np

whT = 320
confTreshold = 0.5
nmsTreshold = 0.3
# cap = cv2.VideoCapture(0)

classesFile = 'coco.names'
classNames = []
with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
# print(classNames)

modelConfiguration = 'yolov3.cfg'  # 'yolov3-tiny.cfg'
modelWeights = 'yolov3.weights'  # 'yolov3-tiny.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def findObjects(img):
##############
    whT = 320
    confTreshold = 0.5
    nmsTreshold = 0.3

    classesFile = 'coco.names'
    classNames = []
    with open(classesFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')
    # print(classNames)

    modelConfiguration = 'yolov3.cfg'  # 'yolov3-tiny.cfg'
    modelWeights = 'yolov3.weights'  # 'yolov3-tiny.weights'

    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

##############

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
    # for i in indices:
    #     i = i[0]
    #     box = bbox[i]
    #     x, y, w, h = box[0], box[1], box[2], box[3]
    #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
    #     cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)} %', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)


# while True:
#     # success, img = cap.read()

#     blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0, 0, 0], 1, crop=False)
#     net.setInput(blob)

#     layerNames = net.getLayerNames()

#     outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]

#     outputs = net.forward(outputNames)

#     findObjects(outputs, img)

#     cv2.imshow('Image', img)
#     cv2.waitKey(1)
imga = 'q.jpg'
img = cv2.imread('imga')

print(findObjects(img))
