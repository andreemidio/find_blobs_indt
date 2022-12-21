import glob
import json
import os
from typing import List, Tuple, Union

import cv2
import numpy as np


class ExtractOMR:

    def read_image(self, file: str) -> np.ndarray:
        return cv2.imread(file)

    def threshold(self, image: np.ndarray) -> List[Union[float, np.ndarray]]:
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 127, 255, 0)

        return ret, thresh

    def find_contours(self, image: np.array) -> Tuple[np.ndarray]:
        contours = list()
        cnts, h = cv2.findContours(image=image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

        for cnt in cnts:
            contours.append(cv2.minAreaRect(cnt))
        return cnts

    def inverse(self, image: np.array) -> np.ndarray:
        return cv2.bitwise_not(image)

    def draw_contours(self, image: np.array, contours: Tuple[np.ndarray]) -> np.ndarray:
        return cv2.drawContours(image=image, contours=contours, contourIdx=-1, color=(0, 255, 75), thickness=2,
                                lineType=cv2.LINE_AA)

    def moments(self, contours: Tuple[np.ndarray]) -> List[Tuple[int, int]]:
        centroids: list = list()
        area_list = list()
        for c in contours:

            area = cv2.contourArea(c)

            area_list.append(area)

            bbox = cv2.minAreaRect(c)

            # if bbox[1][0] == 10.0 and bbox[1][1] == 21:
            if area == 210.0 :
                M = cv2.moments(c)

                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                centroids.append((cX, cY))

        area_list.sort()

        print(area_list)

        return centroids

    def find_min_x_axis(self, centroids: List[Tuple[int, int]]) -> List[int]:
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

    def external(self, image: np.ndarray):
        return cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def run(self, images_list: List[str], view: bool = False) -> None:
        images_list.sort()

        for file_image in images_list:

            r = self.read_image(file=file_image)
            ret, image_thresh = self.threshold(image=r)

            # ccccc, _ = self.external(image=r)

            i = self.inverse(image=image_thresh)

            contours = self.find_contours(image=i)

            m = self.moments(contours=contours)

            r_copy = i.copy()

            d = self.draw_contours(image=r_copy, contours=contours)

            f = self.find_min_x_axis(centroids=m)

            for row in m:
                cv2.circle(d, row, 1, (0, 255, 0), 2)

            resultado_object = dict(
                file_name=file_image,
                first_line=len(contours[0]),
                first_column=len(f),
                total=len(contours)
            )
            image_name = file_image.split("/")[-1].split(".")[-2]

            with open(f"resultados/{image_name}_resultado_leitura.json", "w",
                      encoding='utf-8') as f:
                json.dump(resultado_object, f, ensure_ascii=False, indent=4)

            if view:
                cv2.imshow("test", d)
                cv2.imshow("not", i)
                cv2.waitKey(0)


if __name__ == '__main__':
    import argparse

    ext = ['png', 'jpg', 'gif', 'bmp']

    if not os.path.exists("resultados"):
        os.mkdir("resultados")

    parser = argparse.ArgumentParser(description='OMR Images')

    parser.add_argument('--image', type=str)
    parser.add_argument('--folder', type=str)
    parser.add_argument('--view', type=str, default='false')
    args = parser.parse_args()

    _view = eval(args.view.title())

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
        # --image images/4x14x187.bmp

    print(f"Lista de imagens {images_list}")

    extract = ExtractOMR()
    extract.run(images_list=images_list, view=_view)
