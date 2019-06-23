from fpdf import FPDF
import datetime
import re
import os
import logging
import xai.graphs.format_contants as graph_constants

LOGGER = logging.getLogger(__name__)


class TrainingReportFPDF(FPDF):
    def __init__(self):
        FPDF.__init__(self)
        font_path = os.path.dirname(__file__)
        # Font sample: https://www.dafont.com/linux-biolinum.font
        try:
            self.add_font('acm_title', '', os.path.join(font_path, 'fonts/LinBiolinum_R.ttf'),
                          uni=True)
            self.add_font('acm_title', 'B', os.path.join(font_path, 'fonts/LinBiolinum_RB.ttf'),
                          uni=True)
            self.add_font('acm_title', 'I', os.path.join(font_path, 'fonts/LinBiolinum_RI.ttf'),
                          uni=True)
            self.add_font('acm_title', 'IB', os.path.join(font_path, 'fonts/LinBiolinum_aBL.ttf'),
                          uni=True)

            self.add_font('acm_text', '', os.path.join(font_path, 'fonts/LinLibertine_R.ttf'),
                          uni=True)
            self.add_font('acm_text', 'B', os.path.join(font_path, 'fonts/LinLibertine_RB.ttf'),
                          uni=True)
            self.add_font('acm_text', 'I', os.path.join(font_path, 'fonts/LinLibertine_RI.ttf'),
                          uni=True)
            self.add_font('acm_text', 'IB', os.path.join(font_path, 'fonts/LinLibertine_RBI.ttf'),
                          uni=True)
            self.title_font = 'acm_title'
            self.content_font = 'acm_text'
        except Exception as e:
            LOGGER.info("Fail to find font file, load Times and Arial as default fonts.")
            self.title_font = 'Times'
            self.content_font = 'Arial'

        self.usecase_name = 'ML_App_Name'
        self.version = ''
        self.create_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.set_title("%s %s: Training Report" % (self.usecase_name, self.version))

        # Initialization
        self.b = 0
        self.i = 0
        self.u = 0
        self.href = ''
        self.page_links = {}

        self.cur_sec = 0
        self.cur_subsec = 0
        self.cur_subsubsec = 0
        self.itemize_level = 0
        self.itemize_symbol = ''
        self.foot_size = 15

    def set_report_info(self, usecase_name=None, version=None, create_date=None):
        if usecase_name is not None:
            self.usecase_name = usecase_name
        if version is not None:
            self.version = version
        if create_date is not None:
            self.create_date = create_date
        self.set_title("%s %s: Training Report" % (self.usecase_name, self.version))

    def header(self):
        # Calculate width of title and position

        self.set_font(self.title_font, 'B', 20)
        w = self.get_string_width(self.title) + 6

        self.set_x((210 - w) / 2)
        # Colors of frame, background and text

        # self.set_draw_color(0, 80, 180)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(58, 81, 110)
        # Thickness of frame (1 mm)
        self.set_line_width(0)
        # Title
        self.cell(w, 9, self.title, 0, 0, 'C', 1)
        # Line break
        self.ln(10)

        author_date = '%s created on %s' % (self.author, self.create_date)
        w = self.get_string_width(author_date) + 6
        self.set_x((210 - w) / 2)

        self.set_font('', '', 10)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(58, 81, 110)
        self.set_line_width(0)
        # Title
        self.cell(w, 5, author_date, 0, 0, 'C', 1)
        # Line break
        self.ln(10)

        # reset back the font
        self.set_font(self.content_font, '', 12)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-self.foot_size)
        # Arial italic 8
        self.set_font(self.content_font, 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, label, num=None):
        # Arial 12
        self.set_font(self.title_font, 'B', 15)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        if num is None:
            self.cell(0, 6, '%s' % label, 0, 1, 'L', 1)
        else:
            self.cell(0, 6, '%s   %s' % (num, label), 0, 1, 'L', 1)

        # Line break
        self.ln(4)

        # reset back the font
        self.set_font(self.content_font, '', 12)

    def add_section(self, title):
        self.cur_sec += 1
        self.cur_subsec = 0
        self.cur_subsubsec = 0
        self.chapter_title(title, self.cur_sec)

    def add_subsection(self, title):
        self.cur_subsec += 1
        self.cur_subsubsec = 0
        self.my_write_line("%s.%s  %s" % (self.cur_sec, self.cur_subsec, title), 'B')

    def add_subsubsection(self, title):
        self.cur_subsubsec += 1
        self.my_write_line("%s.%s.%s  %s" % (self.cur_sec, self.cur_subsec, self.cur_subsubsec, title), 'BI')

    def start_itemize(self, symbol=' - '):
        self.itemize_symbol = symbol
        self.itemize_level += 1

    def end_itemize(self):
        self.itemize_symbol = ''
        self.itemize_level -= 1

    def write_html(self, html):
        # HTML parser
        html = html.replace("\n", ' ')
        a = re.split('<(.*?)>', html)
        for i, e in enumerate(a):
            if i % 2 == 0:
                # Text
                if self.href:
                    self.put_link(self.href, e)
                else:
                    self.write(5, e)
            else:
                # Tag
                if e[0] == '/':
                    self.close_tag(e[1:].upper())
                else:
                    # Extract attributes
                    attr = {}
                    a2 = e.split(' ')
                    tag = a2.pop(0).upper()
                    for v in a2:
                        a3 = re.findall('''^([^=]*)=["']?([^"']*)["']?''', v)[0]
                        if a3:
                            attr[a3[0].upper()] = a3[1]
                    self.open_tag(tag, attr)

    def open_tag(self, tag, attr):
        # Opening tag
        if tag in ('B', 'I', 'U'):
            self.set_style(tag, 1)
        if tag == 'A':
            self.href = attr['HREF']
        if tag == 'BR':
            self.ln(5)

    def close_tag(self, tag):
        # Closing tag
        if tag in ('B', 'I', 'U'):
            self.set_style(tag, 0)
        if tag == 'A':
            self.href = ''

    def set_style(self, tag, enable):
        # Modify style and select corresponding font
        t = getattr(self, tag.lower())
        if enable:
            t += 1
        else:
            t += -1
        setattr(self, tag.lower(), t)
        style = ''
        for s in ('B', 'I', 'U'):
            if (getattr(self, s.lower()) > 0):
                style += s
        self.set_font('', style)

    def put_link(self, url, txt):
        # Put a hyperlink
        self.set_text_color(0, 0, 255)
        self.set_style('U', 1)
        self.write(5, txt, url)
        self.set_style('U', 0)
        self.set_text_color(0)

    def draw_table(self, header, data, col_width=None):
        # Colors, line width and bold font
        self.set_fill_color(23, 63, 95)
        self.set_text_color(255)
        self.set_draw_color(23, 63, 95)
        self.set_line_width(0.3)
        self.set_font('', 'B')

        # Header
        if col_width is None:
            w = [55] * len(header)
        else:
            w = col_width

        for i in range(0, len(header)):
            self.cell(w[i], 7, header[i], 1, 0, 'L', 1)
        self.ln()
        # Color and font restoration
        self.set_fill_color(224, 235, 255)
        self.set_text_color(0)
        self.set_font('')
        # Data
        fill = 0
        for row in data:
            for i in range(len(data[0])):
                self.cell(w[i], 6, str(row[i]), 'LR', 0, 'L', fill)
            self.ln()
            fill = not fill
        self.cell(sum(w), 0, '', 'T')
        self.ln()

    def my_write(self, line, style=[]):

        line = "%s%s%s" % ("   " * self.itemize_level, self.itemize_symbol, line)

        html_text = line
        if 'B' in style:
            html_text = "<B>%s</B>" % html_text
        if 'I' in style:
            html_text = "<I>%s</I>" % html_text
        if 'U' in style:
            html_text = "<U>%s</U>" % html_text
        self.write_html(html_text)

    def my_write_line(self, line='', style=[]):
        if type(line) == str:
            self.my_write(line, style)
            self.write_html('<BR>')
        if type(line) == int:
            for i in range(line):
                self.write_html('<BR>')

    def my_write_key_value(self, key, value):
        if value is None or value == '':
            return
        self.write_html("%s%s" % ("   " * self.itemize_level, self.itemize_symbol))
        self.write_html("%s: " % key)
        self.write_html("<B>%s</B>" % str(value))
        self.write_html('<BR>')

    def add_image(self, image_path, width, height):
        # assert remaining space
        if self.y + height > self.h - self.foot_size:
            print('Warning: figure will exceed the page bottom, adding a new page.')
            self.add_page()

        X = self.x
        Y = self.y

        self.image(image_path, X, Y, width, height, '', '')
        self.ln(height)
        return True

    def add_large_image(self, image_path, caption=None, style=None):
        width = graph_constants.LARGE_FIGURE_WIDTH
        height = graph_constants.LARGE_FIGURE_HEIGHT
        # assert remaining space

        if caption is None:
            if self.y + height > self.h - self.foot_size:
                print('Warning: figure will exceed the page bottom, adding a new page.')
                self.add_page()
        else:
            ## TODO: estimate the caption height, 10 is hardcoded
            if self.y + height + 5 > self.h - self.foot_size:
                print('Warning: figure will exceed the page bottom, adding a new page.')
                self.add_page()

        self.my_write_line(caption,style=style)
        X = self.x
        Y = self.y

        self.image(image_path, X, Y, width, height, '', '')
        self.ln(height)
        return True


    def add_grid_images(self, image_set, grid_spec, ratio=False, grid_width = None, grid_height = None, caption = None, style = None):
        # image_set: dict, key = image_name, value = image_path
        # grid_spec: dict, key = image_name, value = (x,y,w,h) [mark left top corner as 0,0]
        # ratio: indicate grid by ratio only. if True, grid_width and grid_height are required.
        X = self.x
        Y = self.y

        maximum_y = 0
        maximum_x = 0

        for image_name, (x,y,w,h) in grid_spec.items():
            if ratio:
                x *= grid_width
                y *= grid_height
                w *= grid_width
                h *= grid_height
                grid_spec[image_name] = (x,y,w,h)
                maximum_y = grid_height
                maximum_x = grid_width
            else:
                maximum_y = max(maximum_y,y+h)

        if X+maximum_x>self.w:
            print('Error: figure will exceed the page edge on the right, exiting plotting.')
            return False

        if caption is None:
            if Y+maximum_y>self.h-self.foot_size:
                print('Warning: figure will exceed the page bottom, adding a new page.')
                self.add_page()
        else:
            ## TODO: estimate the caption height, 10 is hardcoded
            if self.y + maximum_y + 5 > self.h - self.foot_size:
                print('Warning: figure will exceed the page bottom, adding a new page.')
                self.add_page()

        self.my_write_line(caption,style=style)
        X = self.x
        Y = self.y
        if type(image_set) == dict:
            for image_name, image_path in image_set.items():
                pos = grid_spec[image_name]
                x, y, w, h = pos
                self.image(image_set[image_name], X+x, Y+y, w, h, '', '')

        if type(image_set) == list:
            ## follow the index
            for idx, image_path in enumerate(image_set):
                pos = grid_spec[idx]
                x, y, w, h = pos
                self.image(image_path, X+x, Y+y, w, h, '', '')

        self.ln(maximum_y)
        return True

