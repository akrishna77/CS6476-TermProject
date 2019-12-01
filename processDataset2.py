#If positive example is (man, next to, bus)
#The negative example will have the pair which is at the least distance from either man or bus
#So, if a car is near to a man. Then, the negative example will be (man, next to, car)
#It's not the ideal thing probably. So, check processDataset as it's more similar to the negative example that we had discussed about.

import json
import imageio
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

#Just change this based on the file and predicate used
predicate = 'next to'
filename = "sg_test_annotations.json"

#From here on you don't need to change anything
if(filename=="sg_test_annotations.json"):
    newFilename = str(predicate+'_test_triplets.json')
else:
    newFilename = str(predicate + '_train_triplets.json')

data = {'predicate': predicate, 'examples': []}
def addToData(filename, p_bbox1, p_bbox2, n_bbox1, n_bbox2, p_name1, p_name2, n_name1, n_name2):
    row = {}
    row['filename'] = filename
    row['positive'] = {}
    row['negative'] = {}

    row['positive']['bbox1'] = p_bbox1
    row['positive']['bbox2'] = p_bbox2
    row['positive']['obj1'] = p_name1
    row['positive']['obj2'] = p_name2

    row['negative']['bbox1'] = n_bbox1
    row['negative']['bbox2'] = n_bbox2
    row['negative']['obj1'] = n_name1
    row['negative']['obj2'] = n_name2

    # print(row)
    data['examples'].append(row)


def getDistance(bb1, bb2):
    bb1_x1 = bb1['x']
    bb1_y1 = bb1['y']
    bb1_w = bb1['w']
    bb1_h = bb1['h']
    bb1_x2 = bb1_x1+bb1_w
    bb1_y2 = bb1_y1+bb1_h

    bb2_x1 = bb2['x']
    bb2_y1 = bb2['y']
    bb2_w = bb2['w']
    bb2_h = bb2['h']
    bb2_x2 = bb2_x1 + bb2_w
    bb2_y2 = bb2_y1 + bb2_h

    dx = min(bb1_x1-bb2_x1, bb1_x1-bb2_x2, bb1_x2-bb2_x1, bb1_x2-bb2_x2)
    dy = min(bb1_y1 - bb2_y1, bb1_y1 - bb2_y2, bb1_y2 - bb2_y1, bb1_y2 - bb2_y2)
    return dx**2 + dy**2

filter = "JSON file (*.json)|*.json|All Files (*.*)|*.*||"
filename = "sg_test_annotations.json"

#Read JSON data into the datastore variable
if filename:
    with open(filename, 'r') as f:
        datastore = json.load(f)
        for it in range(len(datastore)):
            for i in range(len(datastore[it]['relationships'])):
                row = datastore[it]['relationships'][i]
                if(row['relationship']=='next to'):
                    obj1 = row['objects'][0]
                    obj2 = row['objects'][1]
                    p_bb1 = datastore[it]['objects'][obj1]['bbox']
                    p_bb2 = datastore[it]['objects'][obj2]['bbox']
                    p_objname1 = datastore[it]['objects'][obj1]['names'][0]
                    p_objname2 = datastore[it]['objects'][obj2]['names'][0]

                    nearest2obj1 = -1
                    dist_obj1 = -1
                    nearest2obj2 = -1
                    dist_obj2 = -1
                    for j in range(i+1,len(datastore[it]['relationships'])):
                        row = datastore[it]['relationships'][j]

                        if(row['objects'][0]==obj1):
                            if(row['objects'][1]==obj2):
                                continue
                            # if(datastore[it]['objects'][row['objects'][1]]['names'][0]!=datastore[it]['objects'][obj2]['names'][0]):
                            #     continue
                            # print(datastore[it]['objects'][row['objects'][1]]['names'], " ",datastore[it]['objects'][obj2]['names'])
                            if(dist_obj1==-1):
                                dist_obj1 = getDistance(datastore[it]['objects'][obj1]['bbox'], datastore[it]['objects'][row['objects'][1]]['bbox'])
                                nearest2obj1 = row['objects'][1]
                            elif(dist_obj1>(getDistance(datastore[it]['objects'][obj1]['bbox'], datastore[it]['objects'][row['objects'][1]]['bbox']))):
                                dist_obj1 = getDistance(datastore[it]['objects'][obj1]['bbox'],datastore[it]['objects'][row['objects'][1]]['bbox'])
                                nearest2obj1 = row['objects'][1]

                        elif(row['objects'][1]==obj1):
                            if (row['objects'][0] == obj2):
                                continue
                            # if (datastore[it]['objects'][row['objects'][0]]['names'][0] != datastore[it]['objects'][obj2]['names'][0]):
                            #     continue
                            # print(datastore[it]['objects'][row['objects'][0]]['names'], " ",datastore[it]['objects'][obj2]['names'])
                            if (dist_obj1 == -1):
                                dist_obj1 = getDistance(datastore[it]['objects'][obj1]['bbox'],datastore[it]['objects'][row['objects'][0]]['bbox'])
                                nearest2obj1 = row['objects'][0]
                            elif (dist_obj1 > (getDistance(datastore[it]['objects'][obj1]['bbox'],datastore[it]['objects'][row['objects'][0]]['bbox']))):
                                dist_obj1 = getDistance(datastore[it]['objects'][obj1]['bbox'],datastore[it]['objects'][row['objects'][0]]['bbox'])
                                nearest2obj1 = row['objects'][0]


                        if (row['objects'][0] == obj2):
                            if (row['objects'][1] == obj1):
                                continue
                            # if (datastore[it]['objects'][row['objects'][1]]['names'][0] != datastore[it]['objects'][obj1]['names'][0]):
                            #     continue
                            # print(datastore[it]['objects'][row['objects'][1]]['names'], " ",datastore[it]['objects'][obj1]['names'])
                            if (dist_obj2 == -1):
                                dist_obj2 = getDistance(datastore[it]['objects'][obj2]['bbox'],datastore[it]['objects'][row['objects'][1]]['bbox'])
                                nearest2obj2 = row['objects'][1]
                            elif (dist_obj2 > (getDistance(datastore[it]['objects'][obj2]['bbox'],datastore[it]['objects'][row['objects'][1]]['bbox']))):
                                dist_obj2 = getDistance(datastore[it]['objects'][obj2]['bbox'],datastore[it]['objects'][row['objects'][1]]['bbox'])
                                nearest2obj2 = row['objects'][1]

                        elif (row['objects'][1] == obj2):
                            if (row['objects'][0] == obj1):
                                continue
                            # if (datastore[it]['objects'][row['objects'][0]]['names'][0] != datastore[it]['objects'][obj1]['names'][0]):
                            #     continue
                            # print(datastore[it]['objects'][row['objects'][0]]['names'], " ",datastore[it]['objects'][obj1]['names'])
                            if (dist_obj2 == -1):
                                dist_obj2 = getDistance(datastore[it]['objects'][obj2]['bbox'],datastore[it]['objects'][row['objects'][0]]['bbox'])
                                nearest2obj2 = row['objects'][0]
                            elif (dist_obj2 > (getDistance(datastore[it]['objects'][obj2]['bbox'],datastore[it]['objects'][row['objects'][0]]['bbox']))):
                                dist_obj2 = getDistance(datastore[it]['objects'][obj2]['bbox'],datastore[it]['objects'][row['objects'][0]]['bbox'])
                                nearest2obj2 = row['objects'][0]

                    if(dist_obj1==-1 and dist_obj2==-1):
                        continue
                    if(dist_obj1<dist_obj2):
                        n_bb1 = datastore[it]['objects'][obj1]['bbox']
                        n_bb2 = datastore[it]['objects'][nearest2obj1]['bbox']
                        n_objname1 = datastore[it]['objects'][obj1]['names'][0]
                        n_objname2 = datastore[it]['objects'][nearest2obj1]['names'][0]
                    else:
                        n_bb1 = datastore[it]['objects'][obj2]['bbox']
                        n_bb2 = datastore[it]['objects'][nearest2obj2]['bbox']
                        n_objname1 = datastore[it]['objects'][obj2]['names'][0]
                        n_objname2 = datastore[it]['objects'][nearest2obj2]['names'][0]

                    addToData(datastore[it]['filename'], p_bb1, p_bb2, n_bb1, n_bb2, p_objname1, p_objname2, n_objname1, n_objname2)


with open(newFilename, 'w') as f:
    json.dump(data, f)
