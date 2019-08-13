from fpdf import FPDF
import datetime
import re
import os
import logging

LOGGER = logging.getLogger(__name__)





class ReportWriter(FPDF):
    def __init__(self,
                 usecase_name: str,
                 author: str,
                 version='',
                 report_name='Training Report'):
        """
        set up the basic information for report
        Args:
            usecase_name(str): use case name, (suggest to be no longer than 20 characters), displayed in header as "[usecase_name] [version]: [report_name]"
            author(str): use case team name, (suggest to be no longer than 20 characters) displayed in header as "created by [author] on [system datetime]"
            version(str): version number, (suggest to be no longer than 10 characters) displayed in header as "[usecase_name] [version]: [report_name]"
            report_name(str): the report name, (suggest to be no longer than 20 characters ) displayed in header as "[usecase_name] [version]: [report_name]"
        """
        FPDF.__init__(self)
        # initialize for report information
        self.usecase_name = usecase_name
        self.version = version
        self.create_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.report_name = report_name
        self.author = author
        self.set_title("%s %s: %s" % (self.usecase_name, self.version, self.report_name))

        ## initilization for font
        # Font sample: https://www.dafont.com/linux-biolinum.font
        font_path = os.path.join(os.path.dirname(__file__), 'fonts')
        try:
            self.add_font('acm_title', '', os.path.join(font_path, 'LinBiolinum_R.ttf'),
                          uni=True)
            self.add_font('acm_title', 'B', os.path.join(font_path, 'LinBiolinum_RB.ttf'),
                          uni=True)
            self.add_font('acm_title', 'I', os.path.join(font_path, 'LinBiolinum_RI.ttf'),
                          uni=True)
            self.add_font('acm_title', 'IB', os.path.join(font_path, 'LinBiolinum_aBL.ttf'),
                          uni=True)

            self.add_font('acm_text', '', os.path.join(font_path, 'LinLibertine_R.ttf'),
                          uni=True)
            self.add_font('acm_text', 'B', os.path.join(font_path, 'LinLibertine_RB.ttf'),
                          uni=True)
            self.add_font('acm_text', 'I', os.path.join(font_path, 'LinLibertine_RI.ttf'),
                          uni=True)
            self.add_font('acm_text', 'IB', os.path.join(font_path, 'LinLibertine_RBI.ttf'),
                          uni=True)
            self.title_font = 'acm_title'
            self.content_font = 'acm_text'
        except Exception as e:
            LOGGER.info("Failed to find the font files. Loading Times and Arial fonts by default.")
            self.title_font = 'Times'
            self.content_font = 'Arial'

        # initilization for format
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

    def header(self):
        """
        override FPDF header function, show report name, author and create date
        """
        # Calculate width of title and position

        self.set_font(self.title_font, 'B', 20)
        text_width = self.get_string_width(self.title) + 6

        self.set_x((210 - text_width) / 2)
        # Colors of frame, background and text

        # self.set_draw_color(0, 80, 180)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(58, 81, 110)
        # Thickness of frame (1 mm)
        self.set_line_width(0)
        # Title
        self.cell(text_width, 9, self.title, 0, 0, 'C', 1)
        # Line break
        self.ln(10)

        author_date = '%s created on %s' % (self.author, self.create_date)
        text_width = self.get_string_width(author_date) + 6
        self.set_x((210 - text_width) / 2)

        self.set_font('', '', 10)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(58, 81, 110)
        self.set_line_width(0)
        # Title
        self.cell(text_width, 5, author_date, 0, 0, 'C', 1)
        # Line break
        self.ln(10)

        # reset back the font
        self.set_font(self.content_font, '', 12)

    def footer(self):
        """
        override FPDF footer function, show page number
        """
        # Position at 1.5 cm from bottom
        self.set_y(-self.foot_size)
        # Arial italic 8
        self.set_font(self.content_font, 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def add_ribbon(self, title):
        """
        add a blue color ribbon with title
        Args: 
            title(str): text to display on the ribbon
        """
        # Arial 12
        self.set_font(self.title_font, 'B', 15)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, title, 0, 1, 'L', 1)

        # Line break
        self.ln(4)

        # reset back the font
        self.set_font(self.content_font, '', 12)

    def add_section(self, title, link=None):
        """
        add a section title (with blue ribbon)
        Args:
            title (str): section title
            link (int): internal anchor
        """
        self.add_page()
        self.cur_sec += 1
        self.cur_subsec = 0
        self.cur_subsubsec = 0
        if link is not None:
            self.set_link(link)
        self.add_ribbon("%s  %s" % (self.cur_sec, title))

    def add_subsection(self, title, link=None):
        """
        add a subsection title in the format of section_number.subsection_number in bold
        Args:
            title (str): subsection title
            link (int): internal anchor

        """
        self.cur_subsec += 1
        self.cur_subsubsec = 0
        if link is not None:
            self.set_link(link)
        self.add_new_line("%s.%s  %s" % (self.cur_sec, self.cur_subsec, title), style='B')

    def add_subsubsection(self, title, link=None):
        """
        add a subsubsection title in the format of section_number.subsection_number.subsubsection_number in bold and italic
        Args:
            title (str): subsubsection title
            link (int): internal anchor
        """
        self.cur_subsubsec += 1
        if link is not None:
            self.set_link(link)
        self.add_new_line("%s.%s.%s  %s" % (self.cur_sec, self.cur_subsec, self.cur_subsubsec, title), style='BI')

    def start_itemize(self, symbol='-'):
        """
        start a new indent block, each line inside the block start with the defined symbol
        Args:
            symbol (str): itemized item header (e.g. '-', '*', '#', '')
        """
        self.itemize_symbol = " %s " % symbol
        self.itemize_level += 1

    def end_itemize(self):
        """
        end the current indent block, pair with "start_itemize"
        """
        self.itemize_level -= 1
        if self.itemize_level == 0:
            self.itemize_symbol = ''

    def write_html(self, html, link=None):
        """
        parse html and write to PDF report
        Args:
             html(str): html content
             link (int): link idx created earlier for internal anchor
        """
        if link is None:
            link = ''
        def set_style(tag, enable):
            # Modify style and select corresponding font
            t = getattr(self, tag.lower())
            if enable:
                t += 1
            else:
                t -= 1
            setattr(self, tag.lower(), t)
            style = ''
            for s in ('B', 'I', 'U'):
                if (getattr(self, s.lower()) > 0):
                    style += s
            self.set_font('', style)

        def open_tag(tag, attr):
            # Opening tag
            if tag in ('B', 'I', 'U'):
                set_style(tag, 1)
            if tag == 'A':
                self.href = attr['HREF']
            if tag == 'BR':
                self.ln(5)

        def close_tag(tag):
            # Closing tag
            if tag in ('B', 'I', 'U'):
                set_style(tag, 0)
            if tag == 'A':
                self.href = ''

        def put_link(url, txt):
            # Put a hyperlink
            self.set_text_color(0, 0, 255)
            set_style('U', 1)
            self.write(5, txt, url)
            set_style('U', 0)
            self.set_text_color(0)

        # HTML parser
        html = html.replace("\n", ' ')
        a = re.split('<(.*?)>', html)
        for i, e in enumerate(a):
            if i % 2 == 0:
                # Text
                if self.href:
                    put_link(self.href, e)
                else:
                    self.write(5, e, link=link)
            else:
                # Tag
                if e[0] == '/':
                    close_tag(e[1:].upper())
                else:
                    # Extract attributes
                    attr = {}
                    a2 = e.split(' ')
                    tag = a2.pop(0).upper()
                    for v in a2:
                        a3 = re.findall('''^([^=]*)=["']?([^"']*)["']?''', v)
                        if a3:
                            attr[a3[0].upper()] = a3[1]
                    open_tag(tag, attr)

    def add_table(self, header, data, col_width=None, row_height=6, x=None, y=None):
        """
        add a table into the pdf report (not support auto-text-swapping for now)
        Args:
            header (list(str)): table header
            data (list(list)): table data
            col_width (list(int)): column width. Set to balanced column width if None.
            x (int): x position of current page to start the table (left top corner)
            y (int): y position of current page to start the table (left top corner)
        """
        # Colors, line width and bold font
        self.set_fill_color(23, 63, 95)
        self.set_text_color(255)
        self.set_draw_color(23, 63, 95)
        self.set_line_width(0.3)
        self.set_font('', 'B')

        # Header
        if col_width is None:
            col_w = int(180 / len(header))
            w = [col_w] * len(header)
        else:
            w = col_width
        if y is not None:
            self.Y = y
        for i in range(0, len(header)):
            if x is not None:
                self.X = x
            self.cell(w[i], row_height, header[i], 1, 0, 'L', 1)
        self.ln()
        # Color and font restoration
        self.set_fill_color(224, 235, 255)
        self.set_text_color(0)
        self.set_font('')
        # Data
        fill = 0
        for row in data:
            for i in range(len(data[0])):
                self.cell(w[i], row_height, str(row[i]), 'LR', 0, 'L', fill)
            self.ln()
            fill = not fill
        self.cell(sum(w), 0, '', 'T')
        self.add_new_line()

    def add_text(self, text, link=None, style=''):
        """
        add text string to pdf report
        Args:
            text (str): text string written to pdf, with current global indent level
            link (int): link idx created earlier for internal anchor
            style (str): styles applied to the text
                        'B': bold,
                        'I': italic,
                        'U': underline,
                        or any combination of above
        """
        html_text = "%s%s%s" % ("   " * self.itemize_level, self.itemize_symbol, text)

        if 'B' in style:
            html_text = "<B>%s</B>" % html_text
        if 'I' in style:
            html_text = "<I>%s</I>" % html_text
        if 'U' in style:
            html_text = "<U>%s</U>" % html_text
        self.write_html(html_text, link=link)

    def add_new_line(self, line='', link=None, style=''):
        """
        add a new line with text string to pdf report
        Args: 
            line (str): text string written to pdf, with current global indent level
            link (int): link idx created earlier for internal anchor
            style (str): styles applied to the text
                        'B': bold,
                        'I': italic,
                        'U': underline,
                        or any combination of above
        """
        if type(line) == str:
            self.add_text(line, link=link, style=style)
            self.write_html('<BR>')
        if type(line) == int:
            for i in range(line):
                self.write_html('<BR>')

    def add_key_value_pair(self, key, value):
        """
        add a key-value pair in the format of "KEY: VALUE" (with a new line) to pdf, with current global indent level
        Args:
            key (str): item key
            value (str): item value
        """
        if value is None or value == '':
            return
        self.write_html("%s%s" % ("   " * self.itemize_level, self.itemize_symbol))
        self.write_html("%s: " % key)
        self.write_html("<B>%s</B>" % str(value))
        self.write_html('<BR>')

    def add_large_image(self, image_path, caption=None, style=None):
        '''
        add an default large image to pdf with a caption above (80% of the report width, w/h = 2.0)
        Args:
            image_path (str): path of the image
            caption (str): image caption above the image
            style (str): style for caption
        '''
        width = (self.w - self.r_margin - self.l_margin) * 0.80
        height = width / 2

        if caption is None:
            if self.y + height > self.h - self.foot_size:
                LOGGER.warning('Warning: figure will exceed the page bottom, adding a new page.')
                self.add_page()
        else:
            ## TODO: estimate the caption height, 10 is hardcoded
            if self.y + height + 5 > self.h - self.foot_size:
                LOGGER.warning('Warning: figure will exceed the page bottom, adding a new page.')
                self.add_page()
        if caption is not None:
            self.add_new_line(caption, style=style)
        X = self.x
        Y = self.y

        self.image(image_path, X, Y, width, height, '', '')
        self.ln(height)

    def add_table_image_group(self, image_path, table_header, table_content, grid_spec, caption=None, style=None):
        '''
        add a block of image with table (table on the left, image on the right)
        Args:
            image_path (str): path of the image
            table_header (list(str)):  table header
            table_content: list(list(string)), 2D nested list with table content
            grid_spec (dict): with "table", "image" as key
            - 'table': (w,h), width and height of the table
            - 'image': (w,h), width and height of the image
            caption (str): group caption
            style (str): caption style
        Returns:
            (bool) True if an image-table block written to PDF successfully, otherwise False
        '''
        X = self.x
        Y = self.y

        if 'image' not in grid_spec:
            LOGGER.error("Error in image_table_spec: no 'image' key found.")
            return False
        else:
            image_width, image_height = grid_spec['image']
        if 'table' not in grid_spec:
            LOGGER.error("Error in image_table_spec: no 'table' key found.")
            return False
        else:
            table_width, table_height = grid_spec['table']

        if X + image_width + table_width > self.w - self.r_margin:
            LOGGER.warning('Warning: figure will exceed the page edge on the right, rescale the whole group.')
            total_maximum_width = self.w - self.r_margin - X

            rescale_ratio = total_maximum_width / (image_width + table_width)

            image_width *= rescale_ratio
            image_height *= rescale_ratio
            table_width *= rescale_ratio
            table_height *= rescale_ratio

        block_height = max(table_height, image_height)

        if caption is None:
            if Y + block_height > self.h - self.foot_size:
                LOGGER.warning('Warning: figure will exceed the page bottom, adding a new page.')
                self.add_page()
        else:
            ## TODO: estimate the caption height, 5 is hardcoded
            if Y + block_height + 5 > self.h - self.foot_size:
                LOGGER.warning('Warning: figure will exceed the page bottom, adding a new page.')
                self.add_page()
            self.add_new_line(caption, style=style)

        X = self.x
        Y = self.y

        if table_header is not None and table_content is not None:
            self.add_table(table_header, table_content, col_width=[table_width / len(table_header)] * len(table_header),
                           row_height=min(table_height / len(table_content), 6), x=X, y=Y)
        if image_path is not None:
            self.image(image_path, x=X + table_width, y=Y, w=image_width, h=image_height)

        # reset to original point and advance
        self.x = X
        self.y = Y
        self.ln(block_height)
        return True

    def add_grid_images(self, image_set, grid_spec, ratio=False, grid_width=None, grid_height=None, caption=None,
                        style=None):
        """
        add an block of images formatted with grid specification
        Args:
            image_set (dict or list):
                dict, indicate image paths
                    - key: image_name
                    - value: image_path
                or list, indicate image paths in sequence

            grid_spec (dict): indicate image size and position
                - key: image_name, or index if image_set is a list
                - value: (x,y,w,h) position and weight/height of image, with left top corner of the block as (0,0), unit in mm

            ratio (bool): indicate grid specification by ratio instead of absolute size.
                      If True, grid_width and grid_height are required.

            grid_width (int): width of the entire grid block (unit in mm)

            grid_height (int): height of the entire grid block (unit in mm)

            caption (str): caption of the entire grid block

            style (str): style of caption
        Returns:
            (bool) True if image blocks generate successfully, otherwise False
        """

        X = self.x
        Y = self.y

        maximum_y = 0
        maximum_x = 0

        for image_name, (x, y, w, h) in grid_spec.items():
            if ratio:
                x *= grid_width
                y *= grid_height
                w *= grid_width
                h *= grid_height
                grid_spec[image_name] = (x, y, w, h)
                maximum_y = grid_height
                maximum_x = grid_width
            else:
                maximum_y = max(maximum_y, y + h)

        if X + maximum_x > self.w:
            LOGGER.error('Error: figure will exceed the page edge on the right, exiting plotting.')
            return False

        if caption is None:
            if Y + maximum_y > self.h - self.foot_size:
                LOGGER.warning('Warning: figure will exceed the page bottom, adding a new page.')
                self.add_page()
        else:
            ## TODO: estimate the caption height, 10 is hardcoded
            if self.y + maximum_y + 5 > self.h - self.foot_size:
                LOGGER.warning('Warning: figure will exceed the page bottom, adding a new page.')
                self.add_page()

        if caption is not None:
            self.add_new_line(caption, style=style)

        X = self.x
        Y = self.y
        if type(image_set) == dict:
            for image_name, image_path in image_set.items():
                pos = grid_spec[image_name]
                x, y, w, h = pos
                self.image(image_set[image_name], X + x, Y + y, w, h, '', '')

        if type(image_set) == list:
            ## follow the index
            for idx, image_path in enumerate(image_set):
                pos = grid_spec[idx]
                x, y, w, h = pos
                self.image(image_path, X + x, Y + y, w, h, '', '')

        self.ln(maximum_y)
        return True

    def add_list_of_grid_images(self, image_set, grid_spec, ratio=False, grid_width=None, grid_height=None,
                                caption=None, style=None):
        """
        add a list of image blocks with each block formatted by a grid specification
        Args
            image_set: list, the list of image_paths

            grid_spec (dict): indicate image size and position
                - key: image_name, or index if image_set is a list
                - value: (x,y,w,h) position and weight/height of image, with left top corner of the block as (0,0), unit in mm

            ratio (bool): indicate grid specification by ratio instead of absolute size.
                      If True, grid_width and grid_height are required.

            grid_width (int): width of the entire grid block (unit in mm)

            grid_height (int): height of the entire grid block (unit in mm)

            caption (str): caption of the entire grid block

            style (str): style of caption
        Returns:
            (bool) True if image blocks generate successfully, otherwise False
        """
        grid_size = len(grid_spec)
        title_drawed = False
        for idx in range(0, len(image_set), grid_size):
            if not title_drawed:
                success = self.add_grid_images(image_set[idx:idx + grid_size], grid_spec, ratio=ratio,
                                               grid_width=grid_width,
                                               grid_height=grid_height, caption=caption,
                                               style=style)
            else:
                success = self.add_grid_images(image_set[idx:idx + grid_size], grid_spec, ratio=ratio,
                                               grid_width=grid_width,
                                               grid_height=grid_height, caption=None,
                                               style=None)
            if not success:
                return False
            title_drawed = True
        return True
