import cv2
import matplotlib.pyplot as plt
import numpy as np


def get_user_story_description(user_story):
    color = user_story[0, 0]
    lower = color * 0.6
    upper = color * 1.01
    mask = cv2.inRange(user_story, lower, upper)
    user_story[mask == 255] = [255, 255, 255]
    user_story[mask == 0] = [0, 0, 0]

    plt.imshow(user_story)
    plt.show()

    loyalty_nums = user_story[7:15, 55:]
    plt.imshow(loyalty_nums)
    plt.show()

    num_width = 6
    for i in range(1, 6):
        num = loyalty_nums[:, num_width * (i - 1) : num_width * i]
        plt.imshow(num)
        plt.show()
    
    # customers_nums = user_story[7:15, :]


def get_user_stories(frame):
    user_stories_board = frame[135:495, 715:925]
    plt.imshow(user_stories_board)
    plt.show()
    w = 86
    h = 35
    for i in range(10):
        x_0 = 10
        y_0 = 48 + 46 * i
        user_story = user_stories_board[y_0 : y_0 + h, x_0 : x_0 + w]
        plt.imshow(user_story)
        plt.show()

        color = user_story[0, 0]
        if (color == [255, 255, 255]).all():
            break

        description = get_user_story_description(user_story)


def main():
    image = cv2.imread("iframe_user_stories.png")

    user_stories = get_user_stories(image)


if __name__ == "__main__":
    main()
