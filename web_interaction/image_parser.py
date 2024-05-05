import cv2
import numpy as np
import matplotlib.pyplot as plt
from os import listdir, getcwd, path


def load_characters():
    characters = []
    template_dir = getcwd()
    if "web_interaction" not in template_dir:
        template_dir = path.join(template_dir, "web_interaction")
    template_dir = path.join(template_dir, "templates")

    for f in listdir(template_dir):
        key = "" if f[:5] == "empty" else f[0]
        digit = cv2.imread(path.join(template_dir, f))
        characters.append((key, digit))
    return characters


CHARACTERS = load_characters()


def get_black_white_image(image, backgruond_color):
    lower = backgruond_color * 0.6
    upper = backgruond_color * 1.01
    mask = cv2.inRange(image, lower, upper)
    image[mask == 255] = [255, 255, 255]
    image[mask == 0] = [0, 0, 0]

    return image


def find_digit(image):
    for key, value in CHARACTERS:
        if value is None:
            continue
        if value.shape != image.shape:
            continue
        if (image == value).all():
            return key


def get_float(nums, num_width, num_count):
    value = ""
    for i in range(num_count):
        num = nums[:, num_width * i : num_width * (i + 1)]
        digit = find_digit(num)
        if digit == "k":
            value += "000"
            break
        if digit is None:
            cv2.imwrite(f"web_interaction/templates/unknown.png", num)
            plt.imshow(num)
            plt.show()
            break
        value += str(digit)
    return float(value)


def get_user_story_float(nums):
    num_width = 6
    return get_float(nums, num_width, 5)


def get_backlog_float(nums):
    num_width = 11
    return get_float(nums, num_width, 2)


def get_user_story_loyalty(user_story):
    loyalty_nums = user_story[7:15, 55:]
    loyalty_value = get_user_story_float(loyalty_nums)
    return loyalty_value


def get_user_story_customers(user_story):
    customers_nums = user_story[19:27, 55:]
    customers_value = get_user_story_float(customers_nums)
    return customers_value / 1000


def get_user_story_description(user_story):
    color = np.array(user_story[0, 0])
    user_story_bw = get_black_white_image(user_story, color)

    loyalty_value = get_user_story_loyalty(user_story_bw)
    customers_value = get_user_story_customers(user_story_bw)

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

        color = row[0, 0]
        if (color == [255, 255, 255]).all():
            break

        rows.append(row)

    return rows


def get_user_stories(frame):
    user_stories = []
    user_stories_board = get_board(frame)
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


def get_backlog_card_descripton(card_image: cv2.typing.MatLike):
    color = np.array(card_image[0, 0])
    card_image = get_black_white_image(card_image, color)

    hours = card_image[9:24, 3:25]
    hours_value = get_backlog_float(hours)

    return color, hours_value


def get_backlog_card_images(image):
    backlog_board = get_board(image)

    backlog_rows = get_rows(backlog_board)
    cards = []
    for row in backlog_rows:
        row_cards = split_row(row)
        cards.extend(row_cards)

    return cards


def get_backlog(image):
    backlog_cards = []
    cards = get_backlog_card_images(image)

    for card in cards:
        card_descripton = get_backlog_card_descripton(card)
        backlog_cards.append(card_descripton)

    return backlog_cards


def get_sprint_number(meta_info: cv2.typing.MatLike):
    sprint = meta_info[14:30, 487:530]
    # plt.imshow(sprint)
    # plt.grid()
    # plt.show()

    sprint_n = get_float(sprint, 11, 3)

    return sprint_n


def get_game_money(meta_info: cv2.typing.MatLike):
    money = meta_info[33:49:, 421:480]
    # plt.imshow(money)
    # plt.grid()
    # plt.show()
    unique_colors = np.unique(money[:, 0], axis=0)
    while len(unique_colors) == 1:
        money = money[:, 1:]
        unique_colors = np.unique(money[:, 0], axis=0)
    money_value = get_float(money, 11, 5)
    return money_value


def get_customers(meta_info: cv2.typing.MatLike):
    num_width = 9
    num_count = 3
    image_width = num_width * num_count
    customers_nums = meta_info[18:29, 161 : 161 + image_width]
    # plt.imshow(customers_nums)
    # plt.grid()
    # plt.show()

    customers_value = get_float(customers_nums, num_width, num_count)
    return customers_value / 1000


def get_loyalty(meta_info: cv2.typing.MatLike):
    loyalty_nums = meta_info[38:49, 143:206]
    # plt.imshow(loyalty_nums)
    # plt.grid()
    # plt.show()

    loyalty_value = get_float(loyalty_nums, 9, 5)
    return loyalty_value


def get_current_sprint_hours(backlog_image):
    backlog_board = get_board(backlog_image)
    button = backlog_board[334:356, 11:199]
    
    button_action = button[:, :100]
    button_action_digit = find_digit(button_action)
    if button_action_digit == 'd':
        nums = button[7:15, 115:145]
    else:
        nums = button[8:16, 138:168]
    nums = get_black_white_image(nums, nums[0, 0])
    current_hours_nums = nums[:, :12]
    current_hours_value = get_float(current_hours_nums, 6, 2)

    return current_hours_value


def main():
    # image = cv2.imread("tests/test_images/iframe_user_stories.png")
    # user_stories = get_user_stories(image)
    # print(user_stories)

    image = cv2.imread("web_interaction/iframe.png")
    # backlog_cards = get_backlog(image)
    # print(backlog_cards)
    # image = cv2.imread("tests/test_images/iframe_user_stories.png")
    meta_info = image[7:83, 57:932]
    # plt.imshow(meta_info)
    # plt.show()

    sprint_n = get_sprint_number(meta_info)
    print(sprint_n)

    money = get_game_money(meta_info)
    print(money)

    customers_value = get_customers(meta_info)
    print(customers_value)

    loyalty_value = get_loyalty(meta_info)
    print(loyalty_value)

    current_sprint_hours = get_current_sprint_hours(image)
    print(current_sprint_hours)


if __name__ == "__main__":
    main()
