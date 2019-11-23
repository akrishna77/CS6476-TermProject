#If positive example is (man, next to, bus)
#The negative example will be like (man, leaning on, bus)
<<<<<<< HEAD
print("test")
=======

>>>>>>> 313733b439d2303e1b4d2709cc53526de352aaa7
import json
import imageio
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

#Just change this based on the file and predicate used
predicate = 'on'
filename = "sg_test_annotations.json"

#From here on you don't need to change anything
if(filename=="sg_test_annotations.json"):
    newFilename = str(predicate+'_test_triplets.json')
else:
    newFilename = str(predicate + '_train_triplets.json')

data = {'predicate': predicate, 'examples': []}
def addToData(filename1, filename2, p_bbox1, p_bbox2, n_bbox1, n_bbox2, p_name1, p_name2, n_name1, n_name2, relationship_p, relationship_n):
    row = {}
    row['filename1'] = filename1
    row['filename2'] = filename2

    row['positive'] = {}
    row['negative'] = {}

    row['positive']['bbox1'] = p_bbox1
    row['positive']['bbox2'] = p_bbox2
    row['positive']['obj1'] = p_name1
    row['positive']['obj2'] = p_name2
    row['positive']['relationship'] = relationship_p

    row['negative']['bbox1'] = n_bbox1
    row['negative']['bbox2'] = n_bbox2
    row['negative']['obj1'] = n_name1
    row['negative']['obj2'] = n_name2
    row['negative']['relationship'] = relationship_n

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

                    for it2 in range(it+1, len(datastore)):
                        nearest2obj1 = -1
                        dist_obj1 = -1
                        nearest2obj2 = -1
                        dist_obj2 = -1
                        for j in range(len(datastore[it2]['relationships'])):
                            row = datastore[it2]['relationships'][j]
                            if(datastore[it2]['objects'][row['objects'][0]]['names'][0]==datastore[it]['objects'][obj1]['names'][0]
                                    and datastore[it2]['objects'][row['objects'][1]]['names'][0]==datastore[it]['objects'][obj2]['names'][0]
                                    and row['relationship']!=predicate):
                                n_bb1 = datastore[it2]['objects'][row['objects'][0]]['bbox']
                                n_bb2 = datastore[it2]['objects'][row['objects'][1]]['bbox']
                                n_objname1 = datastore[it2]['objects'][row['objects'][0]]['names'][0]
                                n_objname2 = datastore[it2]['objects'][row['objects'][1]]['names'][0]
                                addToData(datastore[it]['filename'], datastore[it2]['filename'], p_bb1, p_bb2, n_bb1, n_bb2, p_objname1, p_objname2,n_objname1, n_objname2, predicate, row['relationship'])
                            elif(datastore[it2]['objects'][row['objects'][0]]['names'][0]==datastore[it]['objects'][obj2]['names'][0]
                                    and datastore[it2]['objects'][row['objects'][1]]['names'][0]==datastore[it]['objects'][obj1]['names'][0]
                                    and row['relationship']!=predicate):
                                n_bb1 = datastore[it2]['objects'][row['objects'][1]]['bbox']
                                n_bb2 = datastore[it2]['objects'][row['objects'][0]]['bbox']
                                n_objname1 = datastore[it2]['objects'][row['objects'][1]]['names'][0]
                                n_objname2 = datastore[it2]['objects'][row['objects'][0]]['names'][0]
                                addToData(datastore[it]['filename'], datastore[it2]['filename'], p_bb1, p_bb2, n_bb1, n_bb2, p_objname1, p_objname2,n_objname1, n_objname2, predicate, row['relationship'])

with open(newFilename, 'w') as f:
    json.dump(data, f)
