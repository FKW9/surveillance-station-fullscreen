import pyautogui, time
import traceback
from configparser import ConfigParser

config = ConfigParser()
config.read('conf.ini')

x_right_offset = 26
y_pos = 81

try:
    x_right_offset = config.getint('config', 'x_right_offset')
    y_pos = config.getint('config', 'y_pos')
except:
    print('Config file not found, creating default...')
    config.add_section('config')
    config.set('config', 'x_right_offset', str(x_right_offset))
    config.set('config', 'y_pos', str(y_pos))
    with open('conf.ini', 'w') as configfile:
        config.write(configfile)

width, height = pyautogui.size()
print('detected screen size:', width, height)
print('click fullscreen at:', width - x_right_offset, y_pos)

for i in range(3):
    pyautogui.click(x = width - x_right_offset, y=y_pos)
    time.sleep(0.7)

pyautogui.moveTo(width-1, height-1)