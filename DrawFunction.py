from PIL import ImageDraw, Image, ImageFont
import os

class DrawFunction(object):

    def __init__(self, draw, config, lines):
        self.draw = draw
        self.Config = config
        self.indent_top = 0
        self.indent_left = 0
        self.font_size = self.Config.max_font_size
        self.font = ImageFont.truetype("arial.ttf", self.Config.max_font_size)
        self.test_draw = ImageDraw.Draw(
            Image.new(
                mode='RGB',
                size=(300, 300)
            )
        )
        self.space_width = self.test_draw.textsize(
            text=' ',
            font=self.font
        )[0]
        self.buf_list = []
        self.lines_attrib = []
        self.attrib_count = 0
        self.lines = lines
        self.line_height = 0

    # #### minor functions
    # #### here
    def set_font_size(self):
        self.font = ImageFont.truetype("arial.ttf", self.font_size)

    def get_line_width(self, text):
        return self.test_draw.textsize(text=text, font=self.font)[0]

    def get_max_height(self, text):
        max_height = 0
        for char in text.strip('\n'):
            height_buf = self.test_draw.textsize(text=char, font=self.font)[1]
            if height_buf >= max_height:
                max_height = height_buf
        return max_height

    def get_whole_height(self, lines):
        whole_height = 0
        for line in lines:
            whole_height += self.get_max_height(' '.join(line))
        return whole_height

    def get_font_size(self, lines):
        self.font_size = self.Config.max_font_size
        for line in lines:
            while self.get_line_width(line) > self.Config.width and self.font_size > self.Config.min_font_size:
                self.font_size -= 1
                self.set_font_size()

    def adjust_lines_length(self, lines, empty = False):
        if empty:
            words = self.buf_list
        else:
            words = self.buf_list + lines.split(" ")
        self.buf_list = []
        text_width = self.get_line_width(' '.join(words))
        while text_width > self.Config.width:
            self.buf_list.insert(0, words.pop())
            text_width = self.get_line_width(' '.join(words))
        return words
    # #### end of minor functions
    # #### here

    def start_drawing(self):
        # make list where every word have 0 for first fon color and 1 for second font color
        first_font_color = True
        for line in self.lines:
            for word in line.split(" "):
                added = False
                if word[0] == "*":
                    if first_font_color:
                        self.lines_attrib.append(1)
                    else:
                        self.lines_attrib.append(0)
                    first_font_color = not first_font_color
                    added = True
                if not added:
                    if first_font_color:
                        self.lines_attrib.append(0)
                    else:
                        self.lines_attrib.append(1)
                if word[len(word)-1] == "*":
                    first_font_color = not first_font_color
        # delete '*' from words
        for x in range(0, len(self.lines)):
            self.lines[x] = self.lines[x].replace("*", "")
        # get optimal font size
        self.get_font_size(self.lines)

        # adjust lines width
        lines = []
        for line in self.lines:
            lines.append(self.adjust_lines_length(line))
        if self.buf_list:
            lines.append(self.adjust_lines_length("", True))

        # align center vertically
        self.indent_top = (self.Config.height - self.get_whole_height(lines))/2
        if self.indent_top < 0:
            self.indent_top = 0

        self.draw_align_center(lines)

    def draw_align_center(self, lines):
        for line in lines:
            self.indent_left = (self.Config.width - self.get_line_width(' '.join(line)))/2
            self.line_height = self.get_max_height(' '.join(line))
            for word in line:
                self.draw_word(word)
                self.attrib_count += 1
            self.indent_top += self.line_height

        # if text_width <= self.Config.width:
        #     indent_left = (self.Config.width-text_width)/2
        #     self.draw.text((indent_left, self.indent_top), text, fill=self.Config.font_color, font=self.font)
        #     self.indent_top += self.get_max_height(text)

    def draw_word(self, word):
        if self.lines_attrib[self.attrib_count] == 0:
            color = self.Config.font_color
        else:
            color = self.Config.second_font_color
        self.draw.text((self.indent_left, self.indent_top), word, fill=color, font=self.font)
        self.indent_left += self.get_line_width(word) + self.get_line_width(" ")
