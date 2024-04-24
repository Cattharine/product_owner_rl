import cv2
import matplotlib.pyplot as plt
import numpy as np

def load_characters():
    digits = {}
    for i in range(10):
        digit = cv2.imread(f"user_stories_nums/digit_{i}.png")
        digits[i] = digit
    dot = cv2.imread(f"user_stories_nums/dot.png")
    digits["."] = dot
    empty = cv2.imread(f"user_stories_nums/empty.png")
    digits[""] = empty
    k_char = cv2.imread(f"user_stories_nums/k.png")
    digits["k"] = k_char
    return digits

CHARACTERS = load_characters()

def get_black_white_image(image, backgruond_color):
    lower = backgruond_color * 0.6
    upper = backgruond_color * 1.01
    mask = cv2.inRange(image, lower, upper)
    image[mask == 255] = [255, 255, 255]
    image[mask == 0] = [0, 0, 0]

    return image

def find_digit(image):
    for key, value in CHARACTERS.items():
        if (image == value).all():
            return key

def get_user_story_float(nums):
    num_width = 6
    value = ""
    for i in range(1, 6):
        num = nums[:, num_width * (i - 1) : num_width * i]
        digit = find_digit(num)
        if digit == 'k':
            break
        if digit is None:
            cv2.imwrite(f"user_stories_nums/unknown.png", num)
            plt.imshow(num)
            plt.show()
            break
        value += str(digit)
    return float(value)

def get_user_story_loyalty(user_story):
    loyalty_nums = user_story[7:15, 55:]
    # plt.imshow(loyalty_nums)
    # plt.show()
    loyalty_value = get_user_story_float(loyalty_nums)
    return loyalty_value

def get_user_story_customers(user_story):
    customers_nums = user_story[19:27, 55:]
    # plt.imshow(customers_nums)
    # plt.show()
    customers_value = get_user_story_float(customers_nums)
    return customers_value

def get_user_story_description(user_story):
    color = user_story[0, 0]
    lower = color * 0.6
    upper = color * 1.01
    mask = cv2.inRange(user_story, lower, upper)
    user_story[mask == 255] = [255, 255, 255]
    user_story[mask == 0] = [0, 0, 0]

    # plt.imshow(user_story)
    # plt.show()

    loyalty_value = get_user_story_loyalty(user_story)
    customers_value = get_user_story_customers(user_story)

    return color, loyalty_value, customers_value

def get_board(image: cv2.typing.MatLike):
    board = image[135:495, 715:925]
    return board

def get_rows(board_image: cv2.typing.MatLike):
    rows = []
    w, h = 88, 37
    for i in range(10):
        x_0 = 10
        y_0 = 48 + 46 * i
        row = board_image[y_0 : y_0 + h, x_0 : x_0 + w]
        # plt.imshow(row)
        # plt.show()

        color = row[0, 0]
        if (color == [255, 255, 255]).all():
            break

        rows.append(row)
    
    return rows

def get_user_stories(frame):
    user_stories = []
    user_stories_board = get_board(frame)
    # plt.imshow(user_stories_board)
    # plt.show()
    user_stories_cards = get_rows(user_stories_board)
    for user_story in user_stories_cards:
        description = get_user_story_description(user_story)
        user_stories.append(description)
    
    return user_stories


def split_row(row: cv2.typing.MatLike):
    left = row[:, :42]
    right = row[:, 46:]
    if (right[0, 0] == [255, 255, 255]).all():
        return [left]
    return [left, right]

def main():
    # image = cv2.imread("iframe_user_stories.png")

    # user_stories = get_user_stories(image)
    # print(user_stories)

    image = cv2.imread("iframe_backlog.png")

    backlog_board = get_board(image)
    plt.imshow(backlog_board)
    plt.show()

    backlog_rows = get_rows(backlog_board)
    cards = []
    for row in backlog_rows:
        row_cards = split_row(row)
        cards.extend(row_cards)
    
    for card in cards:
        plt.imshow(card)
        plt.show()
        color = card[0, 0]
        lower = color * 0.6
        upper = color * 1.01
        mask = cv2.inRange(card, lower, upper)
        card[mask == 255] = [255, 255, 255]
        card[mask == 0] = [0, 0, 0]

        plt.imshow(card)
        plt.show()
        break


if __name__ == "__main__":
    main()
