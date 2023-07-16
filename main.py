import os
import time
from configparser import ConfigParser

import cv2 as cv
import numpy as np
import pyautogui
from PIL import ImageGrab


class TemplateMatcher:
    method = cv.TM_CCOEFF_NORMED
    position = (0, 0)
    template_path = os.path.join(os.getcwd(), 'template')
    screen_path = os.path.join(os.path.expanduser('~'), 'Pictures', 'screen.png')

    @classmethod
    def match(cls, _template_file: str, certainty: float):
        template_file = os.path.join(cls.template_path, _template_file)
        if not os.path.isfile(template_file):
            raise FileNotFoundError(f'{matcher} not found!')

        # save screenshot of monitor
        ImageGrab.grab(all_screens=True).save(cls.screen_path)
        input_image_rgb = cv.imread(cls.screen_path)
        os.remove(cls.screen_path)

        # convert screenshot to greyscale
        input_image_gry = cv.cvtColor(input_image_rgb.copy(), cv.COLOR_BGR2GRAY)

        # loop over each template image
        _curr_certainty = 0
        _position  = (0, 0)

        # read image
        template_image = cv.imread(template_file, 0)
        w, h = template_image.shape[::-1]

        # apply template Matching
        result = cv.matchTemplate(input_image_gry, template_image, cv.TM_CCOEFF_NORMED)

        # check if certainty is higher then the last one
        _c = np.amax(result)
        if _c > _curr_certainty:
            _curr_certainty = _c
            max_loc = cv.minMaxLoc(result)[3]

            # update mouse position
            _position = (
                (2 * max_loc[0] + w)//2,
                (2 * max_loc[1] + h)//2
            )

        if _curr_certainty < certainty:
            raise ValueError(f'Did not find a match for: \"{_template_file}\"! {_curr_certainty:.3f} < {certainty}')

        print(f'Found match for \"{_template_file}\" at: {_position}, certainty: {_curr_certainty}')
        return _position

    @classmethod
    def find(cls, template: str, certainty: float):
        cls.position = cls.match(template, certainty)
        return cls.position


if __name__ == '__main__':

    config = ConfigParser()
    config.read('conf.ini')

    x_pos_offset = 2
    y_pos_offset = 34
    retries      = 30
    retry_delay  = 2
    debug        = False

    try:
        x_pos_offset = config.getint('config', 'x_pos_offset')
        y_pos_offset = config.getint('config', 'y_pos_offset')
        retry_delay  = config.getint('config', 'retry_delay')
        retries      = config.getint('config', 'retries')
        debug        = config.getboolean('config', 'debug')
    except:
        print('Config file not found, creating default...')
        config.add_section('config')
        config.set('config', 'x_pos_offset', str(x_pos_offset))
        config.set('config', 'y_pos_offset', str(y_pos_offset))
        config.set('config', 'retry_delay', str(retry_delay))
        config.set('config', 'retries', str(retries))
        config.set('config', 'debug', str(debug))
        with open('conf.ini', 'w') as configfile:
            config.write(configfile)

    width, height = pyautogui.size()
    print('Detected screen size:', width, height)

    matcher = TemplateMatcher()
    for _ in range(retries):
        try:
            matcher.find('header.png', 0.96)
            matcher.find('player.png', 0.96)
        except ValueError as err:
            print(err)
            time.sleep(retry_delay)
        else:
            break

    pos = matcher.find('button.png', 0.96)

    if not debug:
        pyautogui.click(x=pos[0]+x_pos_offset, y=pos[1]+y_pos_offset)
        pyautogui.moveTo(width-1, height-1)
    else:
        pyautogui.moveTo(x=pos[0]+x_pos_offset, y=pos[1]+y_pos_offset)
