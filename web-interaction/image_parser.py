import cv2
import matplotlib.pyplot as plt
import numpy as np


def main():
    image = cv2.imread("iframe_user_stories.png")

    x_0 = 725
    y_0 = 229  # 183  # diff = 46
    w = 86
    h = 35
    slice = image[y_0 : y_0 + h, x_0 : x_0 + w]
    plt.imshow(slice)
    plt.show()

    # (247, 150, 23), (241, 147, 23), (239, 145, 22)
    color = slice[0, 0]
    lower = color * 0.6
    upper = color * 1.1
    mask = cv2.inRange(slice, lower, upper)
    slice[mask == 255] = [255, 255, 255]
    slice[mask == 0] = [0, 0, 0]

    plt.imshow(slice)
    plt.show()


if __name__ == "__main__":
    main()
