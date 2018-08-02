import cv2
import os
import json
import sys


module_dir = os.path.dirname(__file__)


def open_json_file(file):
    file_path = os.path.join(module_dir, file)
    with open(file_path) as f:
        schema = json.load(f)
    return schema


def test(file):
    lsbbox = open_json_file(file+'.json')
    lsbbox = lsbbox['bboxes']

    img = cv2.imread(file+'.png', cv2.IMREAD_COLOR)

    for bb in lsbbox:
        cv2.rectangle(img, (int(bb['x0']), int(bb['y0'])), (int(
            bb['x1']), int(bb['y1'])), (0, 0, 255), 1)

    cv2.imshow('bounding boxes', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():

    if len(sys.argv) < 2:
        print("missing a map for path file")
        print("example: testbboxes data_gen/task0/map_eqdc_0")
        sys.exit()

    path = str(sys.argv[1])

    test(path)


main()