import imageio
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np

#Just enter filename
filename = "on_test_triplets.json"

#No need to make changes from here
def getCoordinates(bbox):
    x = bbox['x']
    y = bbox['y']
    w = bbox['w']
    h = bbox['h']

    x2 = x+w
    y2 = y+h

    x_coordinates = np.array([x,x,x2,x2,x])
    y_coordinates = np.array([y,y2,y2,y,y])
    return x_coordinates, y_coordinates

import json
filter = "JSON file (*.json)|*.json|All Files (*.*)|*.*||"

#Read JSON data into the datastore variable
if filename:
    with open(filename, 'r') as f:
        datastore = json.load(f)
        print(len(datastore['examples']))
        for it in range(len(datastore['examples'])):
            filename1 = datastore['examples'][it]['filename1']
            filename2 = datastore['examples'][it]['filename2']

            p_bb1 = datastore['examples'][it]['positive']['bbox1']
            p_bb2 = datastore['examples'][it]['positive']['bbox2']
            n_bb1 = datastore['examples'][it]['negative']['bbox1']
            n_bb2 = datastore['examples'][it]['negative']['bbox2']

            p_obj1 = datastore['examples'][it]['positive']['obj1']
            p_obj2 = datastore['examples'][it]['positive']['obj2']
            n_obj1 = datastore['examples'][it]['negative']['obj1']
            n_obj2 = datastore['examples'][it]['negative']['obj2']

            p_pred = datastore['examples'][it]['positive']['relationship']
            n_pred = datastore['examples'][it]['negative']['relationship']

            img1 = imageio.imread("sg_test_images/"+filename1)
            img2 = imageio.imread("sg_test_images/"+filename2)


            plt.subplot(121)
            plt.title("Positive Example: "+p_obj1+", "+p_pred+", "+p_obj2)
            plt.imshow(img1)
            coordinates_x, coordinates_y = getCoordinates(p_bb1)
            plt.plot(coordinates_x, coordinates_y, 'b-')
            coordinates_x, coordinates_y = getCoordinates(p_bb2)
            plt.plot(coordinates_x, coordinates_y, 'b-')

            plt.subplot(122)
            plt.title("Negative Example: " + n_obj1 + ", " + n_pred + ", " + n_obj2)
            plt.imshow(img2)
            coordinates_x, coordinates_y = getCoordinates(n_bb1)
            plt.plot(coordinates_x, coordinates_y, 'r-')
            coordinates_x, coordinates_y = getCoordinates(n_bb2)
            plt.plot(coordinates_x, coordinates_y, 'r-')

            plt.show()





