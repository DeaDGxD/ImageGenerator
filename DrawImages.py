from PIL import Image, ImageDraw
from CreateConfig import ConfigClass
from DrawFunction import DrawFunction
import os

# create and get config
configfile_name = "config.ini"
Config = ConfigClass(configfile_name)

if not os.path.isfile(configfile_name):
    Config.create_config()
Config.get_whole_config()

if not os.path.isfile('lista_tekstow.txt'):
    f = open('lista_tekstow.txt', 'w+')
    f.close()
if not os.path.isdir('images'):
    os.mkdir('images')
if not os.path.isdir('teksty'):
    os.mkdir('teksty')


def create_image():
    img = Image.new('RGB', (Config.width, Config.height), color=Config.background_color)
    draw = ImageDraw.Draw(img)

    draw_function = DrawFunction(draw, Config, lines)
    draw_function.start_drawing()

    img.save('images/'+str(text_name)+'/img'+str(x)+'.jpg')


text_list = open('lista_tekstow.txt', mode='r', encoding='utf-8-sig')
for text in text_list:
    text_name = text.strip('\n')
    os.mkdir('images/'+str(text_name))

    all_lines = open('teksty/'+str(text_name)+'.txt', mode='r', encoding='utf-8-sig')
    lines = []
    x = 1

    for line in all_lines:
        if line.strip('\n') == "%":
            create_image()
            x += 1
            lines = []
        else:
            lines.append(line.strip('\n'))
    create_image()
    all_lines.close()
text_list.close()


