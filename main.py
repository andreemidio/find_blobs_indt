import glob
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


def main():
    file_image: str = "images/4x14x187.bmp"
    # file_image: str = "images/6x20x198.bmp"
    list_images: list = glob.glob("images/*.bmp")

    list_images.sort()

    for file_image in list_images:

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

        print(f"Imagem {file_image}")

        print(f"Primeira linha há {len(contours[0])} contornos hachurados ")

        print(f"Primeira coluna  há {len(f)} contornos hachurados ")

        print(f"Há um total de  {len(contours)} área hachuradas")

        cv2.imshow("test", d)
        cv2.imshow("not", i)
        cv2.waitKey(0)


if __name__ == '__main__':
    main()
