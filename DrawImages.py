from PIL import Image, ImageDraw
from CreateConfig import ConfigClass
from DrawFunction import DrawFunction
import os

# dest_folder is where images will be created
# source_folder is where you put texts
configfile_name = "config.ini"
dest_folder = 'images'
source_folder = 'texts'

# create and get config
Config = ConfigClass(configfile_name)
if not os.path.isfile(configfile_name):
    Config.create_config()
Config.get_whole_config()

if not os.path.isdir(dest_folder):
    os.mkdir(dest_folder)
if not os.path.isdir(source_folder):
    os.mkdir(source_folder)
    # if you create new folder, make some test files
    test_file = open(os.path.join(source_folder, 'test.txt'), 'w')
    test_file.write('This is test message\n')
    test_file.write('%\n')
    test_file.write('To *show you* how to use this program')
    test_file.close()

    test_file2 = open(os.path.join(source_folder, 'test2.txt'), 'w')
    test_file2.write('Next one')
    test_file2.close()


def create_image(folder_name, text):
    print('Creating image no.: '+str(x))
    # make one color image
    img = Image.new('RGB', (Config.width, Config.height), color=Config.background_color)
    draw = ImageDraw.Draw(img)

    # draw
    # get first_font_color variable from outside of function, to know whether first image ended up with
    # first or second color
    global first_font_color
    draw_function = DrawFunction(draw, Config, text, first_font_color)
    draw_function.start_drawing()
    # get last font color used for image
    first_font_color = draw_function.first_font_color

    # save image
    img.save(os.path.join(folder_name, 'img'+str(x)+'.jpg'))

    # return lines that didnt fit in image
    return draw_function.lines_left


# define default font color
first_font_color = True
# for every txt file in source_folder
for file in os.listdir(source_folder):
    if file.endswith(".txt"):
        print('Converting:', file)
        # create text_path, and dest_path (dest without extension cause it will be just a folder)
        text_path = os.path.join(source_folder, file)
        dest_path = os.path.join(dest_folder, file[:-4])
        # if dest_path exist, remove every file inside
        if os.path.isdir(dest_path):
            for i in os.listdir(dest_path):
                os.remove(os.path.join(dest_path, i))
        else:
            os.mkdir(dest_path)

        # open file
        all_lines = open(text_path, mode='r', encoding='utf-8-sig')
        lines = []
        # to count images
        x = 1

        for line in all_lines:
            # if in line is only %, then create image
            if line.strip('\n') == "%":
                # create_image returns lines that didnt fit into image
                lines = create_image(dest_path, lines)
                x += 1
            # else add line to array for next image
            else:
                lines.append(line)

        # while there are still lines
        while lines:
            # create_image returns lines that didnt fit into image
            lines = create_image(dest_path, lines)
            x += 1

        # close file
        all_lines.close()

