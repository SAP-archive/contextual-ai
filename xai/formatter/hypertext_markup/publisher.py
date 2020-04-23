#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""HTML Report Formatter - Publisher"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import datetime

from yattag import Doc, indent


################################################################################
### Custom File for HTML
################################################################################
class CustomHtml:

    COPY_RIGHT = 'Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved'

    def __init__(self, name='html_report', *, path='./', style=None,
                 script=None) -> None:
        """
        Generate HTML File

        Args:
            name (str, Optional): file name,
                       (default is 'report_file')
            path (str, Optional): output path
                       (default current dict './')
            style (str, Optional): css style file path
                       (default to same as 'path')
            script (str, Optional): jsp script file path
                       (default to same as 'path')
        """
        self._name = name
        self._path = path

        self._style = style
        if self._style is None:
            self._style = os.path.join(self._path, 'simple.css')

        self._script = script
        if self._script is None:
            self._script = os.path.join(self._path, 'simple.js')

        self._extension = 'html'

        self._html_body_header = list()
        self._html_body_section_article = list()

        self._create_date = datetime.datetime.now().strftime("%Y-%m-%d "
                                                             "%H:%M:%S")

    @property
    def path(self):
        """Returns file output path"""
        return self._path

    @property
    def style(self):
        """Returns css file path"""
        return self._style

    @property
    def script(self):
        """Returns jsp file path"""
        return self._script

    @property
    def name(self):
        """Returns file name."""
        return self._name

    @property
    def extension(self):
        """Returns file extension."""
        return self._extension

    @property
    def header(self):
        """Returns HTML Body Section Header"""
        return self._html_body_header

    @property
    def article(self):
        """Returns HTML Body Section Article """
        return self._html_body_section_article

    @staticmethod
    def add_unordered_list(items: list):
        """
        add unordered list

        Args:
            items (list): list of section title to add to unordered list
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('ul'):
            for item in items:
                with doc.tag('li'):
                    doc.asis(item)
        return doc.getvalue()

    @staticmethod
    def add_unordered_kay_value_pair_list(items: list):
        """
        add unordered list Key:Value pair list

        Args:
            items (list): list of key:value pairs to add to unordered list
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('ul'):
            for key, value in items:
                with doc.tag('li'):
                    doc.asis('%s: <b>%s</b>' % (key, value))
        return doc.getvalue()

    @staticmethod
    def add_overview_table(data: list):
        """
        add overview table

        Args:
            data (list): list of key:value pairs to add to table row
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('table'):
            doc.attr(klass='overview_table')
            for key, item in data:
                with doc.tag('tr'):
                    doc.asis('<td><b>%s</b></td>' % key)
                    if isinstance(item, tuple):
                        joined = ",".join(str(v) for v in item)
                        doc.asis('<td>(%s)</td>' % joined)
                    else:
                        doc.asis('<td>%s</td>' % item)
        return doc.getvalue()

    @staticmethod
    def add_basic_nested_info(data: list):
        """
        add basic nested info

        Args:
             data (list): list of tuple / list of (list of tuple))
                multi-level rendering, e.g. to display `model_info`
        Returns: HTML String
        """
        def add_paragraph(x, itemize_level='&nbsp&nbsp- '):
            doc = Doc()
            for key, item in x:
                if (type(item) is list) or (type(item) is tuple):
                    doc.asis('%s%s:<br>' % (itemize_level, key))
                    new_indent = '&nbsp&nbsp' + itemize_level
                    doc.asis(add_paragraph(item, new_indent))
                else:
                    doc.asis('%s%s: <b>%s</b><br>' % (
                            itemize_level, key, item))

            return doc.getvalue()

        outter_doc = Doc()
        with outter_doc.tag('p'):
            outter_doc.asis(add_paragraph(data))
        return outter_doc.getvalue()

    @staticmethod
    def add_overview_table_with_dict(data: dict):
        """
        add overview table with dict

        Args:
            data (dict): list of key:value pairs to add to table row
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('table'):
            doc.attr(klass='overview_table')
            for key, items in data.items():
                with doc.tag('tr'):
                    doc.asis('<td><b>%s</b></td>' % key)
                    for item in items:
                        doc.asis('<td>%s</td>' % item)
        return doc.getvalue()

    @staticmethod
    def add_table(header: list, data: list):
        """
        add table

        Args:
            header (list): list of header
            data (list): list of rows (list)
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('table'):
            doc.attr(klass='standard_table')
            with doc.tag('tr'):
                for h in header:
                    with doc.tag('th'):
                        doc.text(h)
            for row in data:
                with doc.tag('tr'):
                    for item in range(len(data[0])):
                        with doc.tag('td'):
                            doc.text(row[item])
        return doc.getvalue()

    @staticmethod
    def add_table_with_dict(data: dict):
        """
        add table

        Args:
            data (dict): list of key:value pairs to add to table row
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('table'):
            doc.attr(klass='standard_table')
            for key, items in data.items():
                with doc.tag('tr'):
                    doc.asis('<td>%s</td>' % key)
                    doc.asis('<td><b>%s</b></td>' % str(items))
        return doc.getvalue()

    @staticmethod
    def add_anchor(text: str, link=None, on_click=False):
        """
        add link idx as anchor

        Args:
            text (str): text string written to pdf, with current
                        global indent level
            link (str): link idx created earlier for internal anchor
            on_click (bool): indicate if the list item (menu) click-able,
                                default False
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('a'):
            if link is None and not (text is None):
                link = "%s" % text.lower().replace(" ", "-")
            doc.attr(href="#a%s" % link)
            if on_click:
                doc.attr(onclick="Section(event, 't%s')" % link)
            doc.attr(klass='tab_links')
            doc.text(text)
        return doc.getvalue()

    @staticmethod
    def add_header(text: str, heading: str, link=None, style=False):
        """
        add text string as header

        Args:
            text (str): text string written to pdf, with current
                        global indent level
            heading (str): heading elements of the text (h1 - h6)
            link (str): link idx created earlier for internal anchor
            style (bool): css style class
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag(heading):
            if not (link is None):
                doc.attr(id="a%s" % link)
            if style:
                doc.attr(klass='section-title')
            doc.text(text)
        return doc.getvalue()

    @staticmethod
    def __add_text(text: str, style=''):
        """
        add text string

        Args:
            text (str): text string written to pdf, with current
                        global indent level
            style (str): styles applied to the text
                        'B': bold,
                        'I': italic,
                        'U': underline,
                        or any combination of above
        Returns: HTML String
        """
        if 'B' in style:
            text = "<b>%s</b>" % text
        if 'I' in style:
            text = "<i>%s</i>" % text
        if 'U' in style:
            text = "<u>%s</u>" % text
        return text

    @staticmethod
    def add_paragraph(text: str, link=None, style=''):
        """
        add a new paragraph with text string

        Args:
            text (str): text string written to html,
                        with current global indent level
            link (int): link idx created earlier for internal anchor
            style (str): styles applied to the text
                        'B': bold,
                        'I': italic,
                        'U': underline,
                        or any combination of above
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('p'):
            if not (link is None):
                doc.attr(href=link)
            doc.asis(CustomHtml.__add_text(text=text, style=style))
        return doc.getvalue()

    @staticmethod
    def add_image(src: str, alt: str, *, width=None, height=None):
        """
        add an image

        Args:
            src (str): image path
            alt (str): image attribute
            width (int): width of image
            height (int): height of image
        Returns: HTML String
        """
        import base64
        with open(src, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        doc = Doc()
        with doc.tag('img'):
            doc.attr(src='data:image/png;base64, %s' %
                         encoded_string.decode('utf-8'))
            doc.attr(alt=alt)
            if not (width is None):
                doc.attr(width=str(width))
            if not (height is None):
                doc.attr(height=str(height))
        return doc.getvalue()

    @staticmethod
    def add_table_image_group(header: list, data: list,
                              src: str, alt: str, *, width=None, height=None):
        """
        add a block of image with table (table on the left, image on the right)

        Args:
            header (list(str)):  table header
            data: list(list(string)), 2D nested list with table content
            src (str): image path
            alt (str): image attribute
            width (int): width of image
            height (int): height of image
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('div'):
            doc.asis(CustomHtml.add_table(header=header, data=data))
            doc.asis(CustomHtml.add_image(src=src, alt=alt,
                                          width=width, height=height))
        return doc.getvalue()

    @staticmethod
    def add_grid_image(srcs: dict, *, width=None, height=None):
        """
       add an block of images formatted with grid specification

        Args:
            srcs (dict): image paths with attribute as key
            width (int): width of image
            height (int): height of image
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('div'):
            for key, value in srcs.items():
                doc.asis(CustomHtml.add_image(src=value, alt=key,
                                              width=width, height=height))
        return doc.getvalue()

    @staticmethod
    def create_head(style: str):
        """
        create HTML Head

        Args:
            style (str): CSS Style
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('head'):
            with doc.tag('title'):
                doc.text('SAP Explainable AI Report')
            doc.stag('meta', charset="utf-8", name="viewport",
                     content="width=device-width, initial-scale=1")
            with doc.tag('style'):
                doc.asis(style)
        return doc.getvalue()

    @staticmethod
    def create_body_header(header: list):
        """
        create HTML Body Header

        Args:
            header (list): Header Content
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('header'):
            for i in header:
                doc.asis(i)
        return doc.getvalue()

    @staticmethod
    def create_body_nav(nav: list):
        """
        create HTML Body Navigator

        Args:
            nav (list): Nav Content
        Returns: HTML String
        """
        # -- Create HTML Body Section Nav --
        doc = Doc()
        with doc.tag('nav'):
            for i in nav:
                doc.asis(i)
        return doc.getvalue()

    @staticmethod
    def create_div(contents: list, *, link=None, tab=False):
        """
        create div

        Args:
            contents (list): Division Content
            link (str): link idx created earlier for internal anchor
            tab (bool): Content tab indicator

        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('div'):
            if not link is None:
                doc.attr(id="t%s" % link)
            if tab:
                doc.attr(klass="tab_contents")
            for content in contents:
                doc.asis(content)
        return doc.getvalue()

    @staticmethod
    def create_body_section(articles: list, create_date: str):
        """
        create HTML Body Section

        Args:
            articles (list): Article Content
            create_date (str) Article Create Date
        Returns: HTML String
        """
        idx = 0
        nav_items = list()
        article_div = list()
        for div in articles:
            if len(div.items) <= 0:
                continue
            if div.title is None:
                div.title = 'Section %s' % str(idx)
            nav_items.append(CustomHtml.add_anchor(text=div.title,
                                                   link=idx, on_click=True))
            article_div.append(CustomHtml.create_div(contents=div.items,
                                                     link=idx, tab=True))
            idx += 1
        _nav_list = CustomHtml.add_unordered_list(items=nav_items)
        doc = Doc()
        with doc.tag('section'):
            doc.asis(CustomHtml.create_body_nav([_nav_list]))
            with doc.tag('article'):
                with doc.tag('i'):
                    doc.text('created on %s ' % create_date)
                for div in article_div:
                    doc.asis(div)
        return doc.getvalue()

    @staticmethod
    def create_body_footer(text: str):
        """
        create HTML Body Footer

        Args:
            text (str): Footer Text
        Returns: HTML String
        """
        doc = Doc()
        with doc.tag('footer'):
            with doc.tag('i'):
                doc.text(text)
        return doc.getvalue()

    @staticmethod
    def _get_file_to_string(path: str):
        with open(path, "rb") as file:
            str = file.read()
        return str.decode('utf-8').replace('/n', '')

    def generate(self):
        """Generate HTML"""
        doc = Doc()
        doc.asis('<!DOCTYPE html>')
        with doc.tag('html'):
            doc.asis(self.create_head(style=self._get_file_to_string(path=self.style)))
            with doc.tag('body'):
                doc.asis(self.create_body_header(header=self.header))
                doc.asis(self.create_body_section(articles=self.article,
                                                  create_date=self._create_date))
                doc.asis(self.create_body_footer(text=self.COPY_RIGHT))
                with doc.tag('script'):
                    doc.asis(self._get_file_to_string(path=self.script))
        return doc.getvalue()

    def to_file(self):
        """
        Output HTML to some destination
        """
        out = os.path.join(self.path, '.'.join((self.name, self.extension)))
        file = open(out, 'w')
        file.write(self.generate())
        file.close()

################################################################################
### Div Object
################################################################################
class Div:

    def __init__(self) -> None:
        """
        Division Place Holder
        """
        self._title = None
        self._items = list()

    @property
    def title(self):
        """Returns division title."""
        return self._title

    @title.setter
    def title(self, title):
        """Set division title."""
        self._title = title

    @property
    def items(self):
        """Returns division item list."""
        return self._items
