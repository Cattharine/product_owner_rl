import cv2
from numpy import array

from web_interaction import image_parser as ip


def test_get_backlog_description():
    frame = cv2.imread("tests/test_images/iframe_backlog.png")
    backlog = ip.get_backlog(frame)
    assert len(backlog) == 4
    assert len(backlog[0]) == 2
    expected_backlog = [
        (array([255, 255, 255]), 8.0),
        (array([255, 255, 255]), 8.0),
        (array([255, 255, 255]), 13.0),
        (array([255, 255, 255]), 9.0),
    ]

    for expected, actual in zip(expected_backlog, backlog):
        expected_color, expected_hours = expected
        color, hours = actual
        assert (color == expected_color).all()
        assert hours == expected_hours
