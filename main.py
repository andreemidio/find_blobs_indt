import glob
import json
import os
from datetime import datetime
from typing import List, Tuple, Union

import cv2
import numpy as np


def read_image(file: str) -> np.ndarray:
    return cv2.imread(file)


def threshold(image: np.ndarray) -> List[Union[float, np.ndarray]]:
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 127, 255, 0)

    return ret, thresh


def find_contours(image: np.array) -> Tuple[np.ndarray]:
    return cv2.findContours(image=image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)


def inverse(image: np.array) -> np.ndarray:
    return cv2.bitwise_not(image)


def draw_contours(image: np.array, contours: Tuple[np.ndarray]) -> np.ndarray:
    return cv2.drawContours(image, contours, -1, (0, 255, 75), 2)


def moments(contours: Tuple[np.ndarray]) -> List[Tuple[int, int]]:
    centroids: list = list()
    for c in contours:
        bbox = cv2.minAreaRect(c)
        M = cv2.moments(c)

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        centroids.append((cX, cY))

    return centroids


def find_min_x_axis(centroids: List[Tuple[int, int]]) -> List[int]:
    min_x_list: list = list()

    for c in centroids:
        min_x_list.append(c[0])

    min_x_list.sort()
    min_value = min(min_x_list)

    resultado = list()
    for m in min_x_list:

        if m == min_value:
            resultado.append(m)

    return resultado


def main(images_list: List[str], view: bool = False) -> None:
    images_list.sort()

    for file_image in images_list:

        r = read_image(file=file_image)
        ret, image_thresh = threshold(image=r)

        i = inverse(image=image_thresh)

        contours, hierarchy = find_contours(image=i)

        m = moments(contours=contours)

        r_copy = r.copy()

        d = draw_contours(image=r_copy, contours=contours)

        f = find_min_x_axis(centroids=m)

        for row in m:
            cv2.circle(d, row, 1, (0, 255, 0), 2)

        resultado_object = dict(
            file_name=file_image,
            first_line=len(contours[0]),
            first_column=len(f),
            total=len(contours)
        )
        image_name = file_image.split("/")[-1].split(".")[-2]
        datetime_value = datetime.now().strftime("%d_%m_%y_%H_%M_%S")
        with open(f"resultados/{image_name}_resultado_leitura_{datetime_value}.json", "w",
                  encoding='utf-8') as f:
            json.dump(resultado_object, f, ensure_ascii=False, indent=4)

        if view:
            cv2.imshow("test", d)
            cv2.imshow("not", i)
            cv2.waitKey(0)


if __name__ == '__main__':
    import argparse

    ext = ['png', 'jpg', 'gif', 'bmp']

    if not os.path.exists("resultados") :
        os.mkdir("resultados")


    parser = argparse.ArgumentParser(description='OMR Images')

    parser.add_argument('--image', type=str)
    parser.add_argument('--folder', type=str)

    parser.add_argument('--view', type=bool, default=False,
                        help='View processing images')

    args = parser.parse_args()

    images_list: list = list()

    if args.folder and args.image:
        print("Você precisa escolher uma forma de acessar os arquivos")
        print("Para imagens --images images.bmp")
        print("Para pasta --folder images")
        exit()

    if args.folder:
        images_list = []
        [images_list.extend(glob.glob(args.folder + '*.' + e)) for e in ext]
        images_list = glob.glob(f"{args.folder}/*.bmp")
        # --folder images

    if args.image:
        images_list.append(args.image)
        # --folder images

    imdir = 'images/'
    # Add image formats here

    print(f"Lista de imagens {images_list}")
    # main(view=args.view)
    main(images_list=images_list)
