import insightface
import numpy as np
import cv2
import time
from insightface.app import FaceAnalysis
from utils import get_my_image
assert insightface.__version__>='0.7'

class SwapFace:

    def picture(self, swap_from, swap_to, swap_check, output ,gender = None):
        start = time.time()
        app = FaceAnalysis(name='buffalo_l')
        app.prepare(ctx_id=0, det_size=(353, 512))

        swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=True, download_zip=True)

        img_to = get_my_image(swap_to)
        faces_to = app.get(img_to)


        img_from = get_my_image(swap_from)
        faces_from = app.get(img_from)

        img_check = get_my_image(swap_check)
        faces_dst = app.get(img_check)

        res = img_to.copy()

        faces = []

        for face in faces_to:
            feat1 = face.embedding
            feat2 = faces_dst[0].embedding
            sim = np.linalg.norm(feat1 - feat2)
            faces.append(sim)

        if len(faces) >0 :
            min_index = faces.index(min(faces))
            if gender != None :
                if faces[min_index].sex == gender:
                    res = swapper.get(res, face[min_index], faces_from[0], paste_back=True)
            else:
                res = swapper.get(res, face[min_index], faces_from[0], paste_back=True)



        cv2.imwrite(output, res)
        end = time.time()
        print('CPU执行时间: ', end - start)