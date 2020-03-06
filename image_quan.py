import json

# def create_vars():


def run(filename):
    print(filename)
    print("OMNI")
    if filename=="":
        return None
    import cv2
    import argparse
    import numpy as np

    # ap = argparse.ArgumentParser()
    # ap.add_argument('-i', '--image', required=True,
    #                 help = 'path to input image')
    # ap.add_argument('-c', '--config', required=True,
    #                 help = 'path to yolo config file')
    # ap.add_argument('-w', '--weights', required=True,
    #                 help = 'path to yolo pre-trained weights')
    # ap.add_argument('-cl', '--classes', required=True,
    #                 help = 'path to text file containing class names')
    # args = ap.parse_args()
    # print(args)

    args = {"image": "horse.jpg",
            "config": "yolov3.cfg",
            "weights": "yolov3.weights",
            "classes": "yolov3.txt"
    }
    #   args = {
    #         "image": "horse.jpg",
    #         "config": "yolov3.cfg",
    #         "weights": "yolov3.weights",
    #         "classes": "yolov3.txt"
    # }
    print(filename)
    args["image"] = filename

    number_items=0
    number_animals=0
    number_person=0

    counter = {
        "person": 0,
        "items": 0,
        "animals" :0 
    }

    animal = [
        "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"
    ]

    items = [
        "bicycle", "motorcycle", "car", "airplane","bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter"
        "bench", "bagpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat" 
        "baseball glove", "spaceboard", "spool", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
        "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote"
        "keyboard", "cell phone", "microwave", "oven", "tosater", "sink", "refrigerator", "book", "clock", "vase", "scissors","teddy bear",
        "hair dryer", "toothbrush", "surfboard", "tennisracket", "bottle", "wine glass", "cup", "fork", "knife"
    ]

    def get_output_layers(net):
        
        layer_names = net.getLayerNames()
        
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers


    # def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h,number_items,number_animals,number_person,counter):

        # global number_items, number_animals,number_person, counter
        label = str(classes[class_id])
        # print(label)
        if label in items:
            number_items+=1
            counter["items"] = number_items
        elif label in animal:
            number_animals+=1
            counter["animals"] = number_animals
        elif label=="person":
            number_person+=1
            counter["person"] = number_person
            # print(number_person)
        else:
            label="unknown"
        color = COLORS[class_id]

        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
        cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        
    image = cv2.imread(args["image"])

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None

    with open(args["classes"], 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet(args["weights"], args["config"])

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4


    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])


    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h),number_items,number_animals,number_person,counter)
        # def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h,number_items,number_animals,number_person,counter):
    # cv2.imshow("object detection", image)
    cv2.waitKey()
    print(counter)
    # my edit
    y1 = json.dumps(counter)
    print(y1)

    cv2.imwrite("object-detection.jpg", image)
    cv2.destroyAllWindows()
    return y1

# if __name__ == "__main__":
#     run("H:\AI\image.jpg")