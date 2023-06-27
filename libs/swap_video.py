import os.path as osp
import os
import cv2
import insightface
from insightface.app import FaceAnalysis
import time
import argparse
import numpy as np

assert insightface.__version__ >= '0.7'


def count_files_in_directory(directory):
    file_count = 0
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            file_count += 1
    return file_count


def load_fit_image(img, resize=False):
    if resize == True:
        w, h, _ = img.shape
        if w > h:
            rate = 512 / w
        else:
            rate = 512 / h

        w = int(w * rate)
        h = int(h * rate)

        img = cv2.resize(img, (h, w), interpolation=cv2.INTER_CUBIC)

    return img


def get_my_image(image_file, resize=True):
    if osp.exists(image_file):
        image_file = image_file
    else:
        assert image_file is not None, '%s not found' % image_file
    img = cv2.imread(image_file)
    if resize is True:
        return load_fit_image(img)
    return img


if __name__ == '__main__':
    # python inswapper_main.py --swap_face=/Users/laozhang/Pictures/aitest/明星/wangbaoqiang.png  --swap_to=/Users/laozhang/Downloads/swapface/gaojin/
    start = time.time()

    # os.environ['CUDA_VISIBLE_DEVICES'] = '2, 3'
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--swap_to',
        type=str,
        default='',
        help="要被替换的图片路径"
    )

    parser.add_argument(
        '--swap_face',
        type=str,
        default='',
        help="脸的路径"
    )

    parser.add_argument(
        '--swap_fps',
        type=str,
        default='25',
        help="帧率"
    )

    parser.add_argument(
        '--swap_check',
        type=str,
        default='',
        help="将此图片的脸替换掉"
    )

    args = parser.parse_args()

    if args.swap_to == "":
        raise "--swap_to参数不能为空"

    src_dir = args.swap_to + os.sep + 'src' + os.sep
    dst_dir = args.swap_to + os.sep + 'dst' + os.sep

    if not osp.exists(src_dir):
        os.system("mkdir " + src_dir)
    if not osp.exists(dst_dir):
        os.system("mkdir " + dst_dir)

    src_mp4 = args.swap_to + os.sep + "src.avi"
    src_mp3 = args.swap_to + os.sep + "audio.mp3"
    output_mp4 = args.swap_to + os.sep + "output.mp4"
    merge_mp4 =  args.swap_to + os.sep + "merge.mp4"
    if not os.path.exists(src_mp4):
        src_mp4 = args.swap_to + os.sep + "src.mp4"

    dst_mp4 = args.swap_to + os.sep + "dst.mp4"

    if args.swap_check == "":
        check_image = args.swap_to + os.sep + "check.jpg"
        if not os.path.exists(check_image):
            check_image = args.swap_to + os.sep + "check.png"
        if not os.path.exists(check_image):
            check_image = args.swap_to + os.sep + "check.jpeg"
        #不存在参考图片，默认目标所有视频中的人脸都换成一个人
        if not os.path.exists(check_image):
           check_image = ""
    else:
        check_image = args.swap_check

    if not osp.exists(src_mp4):
        print(src_mp4)
        raise src_mp4 + " not found"

    if count_files_in_directory(src_dir) < 5:
        command_cut = "ffmpeg -i " + src_mp4 + " -r " + args.swap_fps + " " + src_dir + "%08d.png"
        print(command_cut)
        os.system(command_cut)

    app = FaceAnalysis(name='buffalo_l',root="./")
    app.prepare(ctx_id=0, det_size=(640, 640))

    swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=True, download_zip=True)

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_extension = os.path.splitext(file)
            if file_extension.lower() in ['.jpeg', '.jpg', '.png']:
                # print(src_dir + file)
                print(dst_dir + file)

                if not osp.exists(dst_dir + file):
                    #old face
                    img_src = get_my_image(src_dir + file)
                    face_src = app.get(img_src)

                    #new face
                    img_dst = get_my_image(args.swap_face)
                    face_dst = app.get(img_dst)

                    res = img_src.copy()
                    faces = []

                    if check_image != "":
                        img_check = get_my_image(check_image)
                        faces_check = app.get(img_check)

                        for face in face_src:
                            feat1 = face.embedding
                            feat2 = faces_check[0].embedding
                            sim = np.linalg.norm(feat1 - feat2)
                            faces.append(sim)

                        if len(faces) > 0:
                            min_index = faces.index(min(faces))
                            if face_src[min_index].sex == 'F':
                                res = swapper.get(res, face_src[min_index], face_dst[0], paste_back=True)

                    else:
                        for face in face_src:
                            res = swapper.get(res, face, face_dst[0], paste_back=True)

                    cv2.imwrite(dst_dir + file, res)


    if count_files_in_directory(dst_dir) > 100:
        command_merge = "ffmpeg -r " + args.swap_fps + " -i " + dst_dir + "%06d.png " + dst_mp4 + " -y"
        print(command_merge)
        os.system(command_merge)

        command_audio = "ffmpeg -i "+ src_mp4 +" -vn -f mp3 -ar 16000 -ac 1 " + src_mp3 + " -y"
        print(command_audio)
        os.system(command_audio)

        command_output = "ffmpeg -i " + dst_mp4 + " -i " + src_mp3 + " -c:v copy -c:a copy " + output_mp4 + " -y"
        print(command_output)
        os.system(command_output)

    if osp.exists(src_mp4) and osp.exists(output_mp4):
        command_merge = 'ffmpeg -i '+ src_mp4 +' -i '+ output_mp4 +' -filter_complex "[0:v]pad=iw*2:ih[a];[a][' \
                                                             '1:v]overlay=w*1" '+ merge_mp4 +' -y '
        print(command_merge)
        os.system(command_merge)


    end = time.time()
    print('CPU执行时间: ', end - start)
