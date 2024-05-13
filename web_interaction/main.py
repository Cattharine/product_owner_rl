from game.game import ProductOwnerGame
from game.userstory_card.userstory_card_info import UserStoryCardInfo
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from single_color_storage import SingleColorStorage
from typing import List

import cv2
import time
import image_parser


def open_game():
    driver = webdriver.Chrome()

    driver.get("https://npg-team.itch.io/product-owner-simulator")

    load_iframe_btn = driver.find_element(by=By.CLASS_NAME, value="load_iframe_btn")
    load_iframe_btn.click()

    return driver


def wait_loading(iframe: WebElement):
    while True:
        time.sleep(1)
        iframe.screenshot("loading.png")
        loading_image = cv2.imread("loading.png")
        is_loading = image_parser.is_loading(loading_image)
        if not is_loading:
            break


def start_game(driver, iframe: WebElement):
    # skip intro
    iframe.click()
    iframe.click()

    height = iframe.rect["height"]  # 540
    width = iframe.rect["width"]  # 960

    # type name
    ActionChains(driver).move_to_element_with_offset(
        iframe, 0, int(0.1 * height)
    ).click().send_keys("selenium").perform()

    # start game
    ActionChains(driver).move_to_element_with_offset(
        iframe, 0, int(0.2 * height)
    ).click().perform()

    # skip tutorial
    ActionChains(driver).move_to_element_with_offset(
        iframe, -int(0.35 * width), int(0.4 * height)
    ).click().perform()

    time.sleep(1)

    # turn off sprint animation
    ActionChains(driver).move_to_element_with_offset(
        iframe, -int(0.45 * width), -int(0.42 * height)  # move to settings icon
    ).click().move_to_element_with_offset(
        iframe, int(0.1 * width), int(0.07 * height)  # move to animation checkbox
    ).click().move_to_element_with_offset(
        iframe, -int(0.45 * width), -int(0.42 * height)  # move to settings icon
    ).click().perform()


def buy_research(driver, iframe: WebElement, width: int, height: int):
    ActionChains(driver).move_to_element_with_offset(
        iframe, 950 - width // 2, 396 - height // 2
    ).click().move_to_element_with_offset(
        iframe, int(0.3 * width), -int(0.3 * height)
    ).click().perform()


def get_game_user_stories_from_image(image: cv2.typing.MatLike, current_sprint: int):
    game_user_stories: List[UserStoryCardInfo] = []
    user_stories, positions = image_parser.get_user_stories(image)

    for user_story, position in zip(user_stories, positions):
        color, loyalty, customers = user_story
        color_storage = SingleColorStorage(color)
        game_user_story = UserStoryCardInfo("S", current_sprint, color_storage)
        game_user_story.loyalty = loyalty
        game_user_story.customers_to_bring = customers
        game_user_story.position = position
        game_user_stories.append(game_user_story)

    return game_user_stories


def insert_user_stories_from_image(game: ProductOwnerGame, image: cv2.typing.MatLike):
    user_stories = get_game_user_stories_from_image(image, game.context.current_sprint)
    game.userstories.stories_list.clear()
    game.context.available_stories.clear()
    for user_story in user_stories:
        game.userstories.add_us(user_story)


def fill_main_info_from_image(game: ProductOwnerGame, image: cv2.typing.MatLike):
    pass


def main():
    driver = open_game()

    iframe = driver.find_element(by=By.ID, value="game_drop")

    wait_loading(iframe)

    start_game(driver, iframe)

    time.sleep(10)

    driver.quit()


if __name__ == "__main__":
    main()
