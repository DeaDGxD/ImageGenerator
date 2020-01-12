from PIL import ImageDraw, Image, ImageFont


class DrawFunction(object):
    def __init__(self, draw, config, lines, first_font_color):
        self.lines = lines
        self.draw = draw
        self.Config = config
        # default font_size is the max one
        self.font_size = self.Config.max_font_size
        # font change mark
        self.font_state_change = '*'
        self.first_font_color = first_font_color
        self.font = ImageFont.truetype("arial.ttf", self.font_size)
        # test image, to test font sizes on it
        self.test_draw = ImageDraw.Draw(
            Image.new(
                mode='RGB',
                size=(300, 300)
            )
        )
        # blank variables
        self.indent_top = 0
        self.indent_left = 0
        self.attrib_count = 0
        self.line_height = 0
        self.buf_list = []
        self.lines_attrib = []
        self.lines_left = []

    # #### minor functions
    # #### here

    # set font size from self.font_size variable
    def set_font_size(self):
        self.font = ImageFont.truetype("arial.ttf", self.font_size)

    # get string width with current self.font
    def get_line_width(self, string):
        return self.test_draw.textsize(text=string, font=self.font)[0]

    # get max char height from string (excluding \n)
    def get_max_height(self, string):
        max_height = 0
        for char in string.strip('\n'):
            height_buf = self.test_draw.textsize(text=char, font=self.font)[1]
            if height_buf >= max_height:
                max_height = height_buf
        return max_height

    # sum max height from every line
    def get_whole_height(self, lines):
        whole_height = 0
        for line in lines:
            whole_height += self.get_max_height(' '.join(line))
        return whole_height

    # while line is wider than image, decrease font_size by 1, until min_font_size
    def get_font_size(self, lines):
        self.font_size = self.Config.max_font_size
        for line in lines:
            while self.get_line_width(line) > self.Config.width and self.font_size > self.Config.min_font_size:
                self.font_size -= 1
                self.set_font_size()

    # split string by spaces and when there are many spaces next to each other, then they become blank in list
    # so use replace_blank_with_spaces function additionally
    def get_list_from_string(self, string):
        word_list = string.split(" ")
        return self.replace_blank_with_spaces(word_list)

    # add every word in list to string, put spaces between them and return string without last char (space it is)
    def get_string_from_list(self, word_list):
        string = ''
        for word in word_list:
            if not word == ' ':
                string += word
            string += ' '
        return string[:-1]

    # strip \n additionally while replacing blank list items with spaces
    def replace_blank_with_spaces(self, word_list):
        final_words = []
        for word in word_list:
            if word == '\n':
                string = word.replace('\n', ' ')
            else:
                string = word.strip('\n')
            if word == '':
                string = word.replace('', ' ')
            final_words.append(string)
        return final_words

    #
    def adjust_lines_length(self, lines, not_empty=True):
        if not_empty:
            self.buf_list += self.get_list_from_string(lines)

        to_return = []
        text_width = 0
        # while text+first word in buf_list is smaller than image or word is bigger than image (to avoid infinite loop)
        # add that word and try with next one
        while text_width + self.get_line_width(' '+self.buf_list[0]) <= self.Config.width \
                or self.get_line_width(self.buf_list[0]) > self.Config.width:
            # get the first word in buf_list and append it to to_return
            to_return.append(self.buf_list.pop(0))
            # set new text_width
            text_width = self.get_line_width(self.get_string_from_list(to_return))
            # if buf_list is empty, break
            if not self.buf_list:
                break
        # return line that is not wider than image
        return to_return
    # #### end of minor functions
    # #### here

    def start_drawing(self):
        # make lines_attrib list full of 0 and 1 that
        # if first word printed had to be in second font color, then lines_attrib[0] is 1
        # if word is in first color then lines_attrib is 0
        # if you want to change font_color state identifier, change font_state variable
        line_buf = []
        # use first_font_color first
        for line in self.lines:
            for word in self.get_list_from_string(line):
                added = False
                # if word starts with * use the other font color and change first_font_color variable to the other state
                if word[0] == self.font_state_change:
                    if self.first_font_color:
                        self.lines_attrib.append(1)
                    else:
                        self.lines_attrib.append(0)
                    self.first_font_color = not self.first_font_color
                else:
                    if self.first_font_color:
                        self.lines_attrib.append(0)
                    else:
                        self.lines_attrib.append(1)
                # if there is * at the end of the word, change first_font_color state
                if word[-1] == self.font_state_change:
                    self.first_font_color = not self.first_font_color
            # remove every * cause its not needed anymore
            line_buf.append(line.replace(self.font_state_change, ""))
        self.lines = line_buf

        # get optimal (that function still can be changed, but its working fine i guess) font_size 
        self.get_font_size(self.lines)

        # adjust lines width
        lines = []
        # if words are wider than image, strip last words and place them at the beginning of next line
        for line in self.lines:
            lines.append(self.adjust_lines_length(line))
        # while there are still words in buf_list keep adjusting
        while self.buf_list:
            lines.append(self.adjust_lines_length(None, False))

        # align center vertically
        self.indent_top = (self.Config.height - self.get_whole_height(lines))/2
        if self.indent_top < 0:
            self.indent_top = 0

        # preparations over i guess, lets get to drawing
        self.draw_align_center(lines)

    def draw_align_center(self, lines):
        same_page = True
        for line in lines:
            # if line fits to image height and same_page is True
            self.line_height = self.get_max_height(self.get_string_from_list(line))
            if self.indent_top + self.line_height <= self.Config.height and same_page:
                self.indent_left = (self.Config.width - self.get_line_width(self.get_string_from_list(line)))/2
                for word in line:
                    if word == ' ':
                        self.indent_left += self.get_line_width(' ')
                    else:
                        self.draw_word(word)
                        self.attrib_count += 1
                self.indent_top += self.line_height
            # if line at least once didnt fit, set same_page to False
            # so every line afterwards will be saved in lines_left
            # if word has second font_color attrib, then save word as *word*
            else:
                # if line height is smaller that image height
                # just in case, so we acoid infinite loop
                if self.line_height < self.Config.height:
                    same_page = False
                    line_left = []
                    for word in line:
                        word_left = word
                        if self.lines_attrib[self.attrib_count] == 1:
                            word_left = self.font_state_change+word+self.font_state_change
                        line_left.append(word_left)
                        self.attrib_count += 1
                    self.lines_left.append(self.get_string_from_list(line_left))

    def draw_word(self, word):
        # simple draw function, that check font_color and use self.indent_left, self.indent_top and self.font
        if self.lines_attrib[self.attrib_count] == 0:
            color = self.Config.font_color
        else:
            color = self.Config.second_font_color
        self.draw.text((self.indent_left, self.indent_top), word, fill=color, font=self.font)
        self.indent_left += self.get_line_width(word) + self.get_line_width(" ")
