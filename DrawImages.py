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

if not os.path.isdir('images'):
    os.mkdir('images')
if not os.path.isdir('teksty'):
    os.mkdir('teksty')
    test_file = open('teksty/test.txt', 'w')
    test_file.write('To jest wiadomość testowa\n')
    test_file.write('%\n')
    test_file.write('Aby *pokazać jak działa* program')
    test_file.close()

    test_file2 = open('teksty/test2.txt', 'w')
    test_file2.write('tutaj kolejny tekst')
    test_file2.close()


def create_image():
    print('Tworzenie obrazu numer: '+str(x))

    img = Image.new('RGB', (Config.width, Config.height), color=Config.background_color)
    draw = ImageDraw.Draw(img)

    draw_function = DrawFunction(draw, Config, lines)
    draw_function.start_drawing()

    img.save(folder_name+'/img'+str(x)+'.jpg')

    return draw_function.lines_left


for file in os.listdir("teksty"):
    if file.endswith(".txt"):
        print('Konwertowanie pliku: '+file)
        text_name = os.path.join("teksty", file)
        folder_name = os.path.join('images/', file[:-4])

        if os.path.isdir(folder_name):
            for i in os.listdir(folder_name):
                os.remove(os.path.join(folder_name, i))
        else:
            os.mkdir(folder_name)

        all_lines = open(text_name, mode='r', encoding='utf-8-sig')
        lines = []
        x = 1

        for line in all_lines:
            if line.strip('\n') == "%":
                lines = create_image()
                x += 1
            else:
                lines.append(line)

        while lines:
            lines = create_image()
            x += 1

        all_lines.close()

