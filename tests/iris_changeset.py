import sys, os
sys.path.insert(1, os.path.dirname(os.getcwd()))

import csv
import json
import jsonpatch

res_dict = {
    'bucket': {
        'name': 'iris'
    }
}

def generate_iris_changeset():
    res_dict['create'] = []
    res_dict['modify'] = []
    res_dict['delete'] = []
    with open('static/iris.data', 'r') as fp:
        csv_file = csv.reader(fp)
        for row in csv_file:
            print(row)
            if not len(row):
                continue
            new_data_item = {
                'data': {
                    'sepal_length': float(row[0]),
                    'sepal_width': float(row[1]),
                    'petal_length': float(row[2]),
                    'petal_width': float(row[3]),
                },
                'annotations': {
                    'label': row[4]
                }
            }
            print(jsonpatch.make_patch({}, new_data_item).patch)
            res_dict['create'].append(
                jsonpatch.make_patch({}, new_data_item).patch
            )
    print(res_dict)
    with open('static/patchfile_iris.json', 'w') as wout:
        json.dump(res_dict, wout, indent=True)

if __name__ == '__main__':
    generate_iris_changeset()