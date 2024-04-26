import cv2

from web_interaction import image_parser as ip

def test_get_board():
    frame = cv2.imread('tests/test_images/board.png')
    board = ip.get_board(frame)
    assert len(board) == 1080
    assert len(board[0]) == 1920