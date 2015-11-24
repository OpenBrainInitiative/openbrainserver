import json
import sys, copy
import base64
import io
import jsonpatch
import numpy as np
import os
import scipy
import scipy.misc
from mnist_loader import MNIST

sys.path.insert(1, os.path.dirname(os.getcwd()))



res_dict = {
    'bucket': {
        'name': 'mnist'
    },
    'create': [],
    'modify': [],
    'delete': []
}

def generate_mnist_changeset():
    m = MNIST('/home/wolfv/Downloads/')
    m.load_training()

    f = open('./static/mnist.png', 'rb')

    encoded = base64.b64encode(f.read())

    create_with_file = {
        'data': {
            'file': {
                'contents': '',
                'mime': 'image/png'
            }
        },
        'annotations': {
            'label': ''
        }
    }


    import pprint  # print(m.train_labels)
    for idx, img_arr in enumerate(m.train_images):
        # if idx > 5:
        #     break

        img  = scipy.misc.toimage(np.array(img_arr).reshape(28, 28), cmin=0, cmax=255)
        fp = io.BytesIO()
        img.save(fp, format='PNG')
        create_with_file['data']['file']['contents'] = base64.b64encode(fp.getvalue())
        create_with_file['annotations']['label'] = m.train_labels[idx]
        patch = jsonpatch.make_patch({}, create_with_file).patch

        res_dict['create'].append(
            copy.deepcopy(patch)
        )

    pprint.pprint(res_dict)
    with open('static/patchfile_mnistfake.json', 'w') as wout:
        json.dump(res_dict, wout, indent=True)


if __name__ == '__main__':
    generate_mnist_changeset()