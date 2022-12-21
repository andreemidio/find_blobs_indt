import glob
import json
import os
from typing import List, Tuple

import cv2
import numpy as np


class ExtractOMR:

    def _read_image(self, file: str) -> np.ndarray:

        gray = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
        return gray

    def _find_contours(self, image: np.array) -> Tuple[np.ndarray]:

        cnts, h = cv2.findContours(image=image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

        return cnts

    def _inverse_image(self, image: np.array) -> np.ndarray:
        return cv2.bitwise_not(image)

    def _draw_contours(self, image: np.array, contours: Tuple[np.ndarray]) -> np.ndarray:
        return cv2.drawContours(image=image, contours=contours, contourIdx=-1, color=(0, 255, 75), thickness=2,
                                lineType=cv2.LINE_AA)

    def _find_moments(self, contours: Tuple[np.ndarray]) -> List[Tuple[int, int]]:
        centroids: list = list()

        for c in contours:

            area = cv2.contourArea(c)

            x, y, w, h = cv2.boundingRect(c)

            if h == 11 and w == 22 and area == 210.0:
                M = cv2.moments(c)

                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                centroids.append((cX, cY))

        return centroids

    def _find_min_x_axis(self, centroids: List[Tuple[int, int]]) -> List[int]:
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

    def _find_min_y_axis(self, centroids: List[Tuple[int, int]]) -> List[int]:
        min_x_list: list = list()

        for c in centroids:
            min_x_list.append(c[1])

        min_x_list.sort()
        min_value = min(min_x_list)

        resultado = list()
        for m in min_x_list:

            if m == min_value:
                resultado.append(m)

        return resultado

    def run(self, images_list: List[str], view: bool = False) -> None:
        images_list.sort()

        for file_image in images_list:

            read_image = self._read_image(file=file_image)

            inversed_image = self._inverse_image(image=read_image)

            contours = self._find_contours(image=inversed_image)

            moments_image = self._find_moments(contours=contours)

            inversed_image_copy = inversed_image.copy()

            draw_contours_image = self._draw_contours(image=inversed_image_copy, contours=contours)

            value_find_min_x_axis = self._find_min_x_axis(centroids=moments_image)
            value_find_min_y_axis = self._find_min_y_axis(centroids=moments_image)

            for row in moments_image:
                cv2.circle(draw_contours_image, row, 1, (0, 255, 0), 2)

            resultado_object = dict(
                file_name=file_image,
                first_line=len(value_find_min_y_axis),
                first_column=len(value_find_min_x_axis),
                total=len(moments_image)
            )
            image_name = file_image.split("/")[-1].split(".")[-2]

            with open(f"resultados/{image_name}_resultado_leitura.json", "w",
                      encoding='utf-8') as value_find_min_x_axis:
                json.dump(resultado_object, value_find_min_x_axis, ensure_ascii=False, indent=4)

            if view:
                cv2.imshow("Contornos", draw_contours_image)
                cv2.imshow("not", inversed_image)
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
