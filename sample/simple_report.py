#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Sample Code to generate report """

import sys
sys.path.append('../')
import json

from xai.formatter.report import Report
from xai.formatter.portable_document import PdfWriter

################################################################################
### Sample Report
################################################################################


def main():
    ## Create Report
    report = Report(name='Sample Report')

    ### Create Cover Section
    report.cover.add_section_title(text="Summary")
    report.cover.add_paragraph(text="This is summary Info")

    ### Create Contents Section - Header
    report.content.add_section_title(text="Example for Header")
    #### Header Level 1 and it paragraph
    report.content.add_header_level_1(text='Section Header 1')
    report.content.add_paragraph(text="This is content Info of header 1")
    #### Header Level 2 and it paragraph
    report.content.add_header_level_2(text='Section Header 2')
    report.content.add_paragraph(text="This is content Info of header 2")
    #### Header Level 3 and it paragraph
    report.content.add_header_level_3(text='Section Header 3')
    report.content.add_paragraph(text="This is content Info of header 3")

    ### Create Contents Section - more
    report.content.add_new_page()
    report.content.add_section_title("Example for Data Module ")
    #### Header Level 1 and it paragraph
    report.content.add_header_level_1(text='Data Module')
    ### Add Missing Value as level 2 content under data module
    report.content.add_header_level_2(text='Missing Value Checking')
    report.content.add_paragraph(text="Some desc on missing value ...")
    """
    Sample: Missing value
    """
    with open('./sample_data/missing_value.json', 'r') as f:
        missing_value = json.load(f)

    missing_count = missing_value["missing_count"]
    total_count = missing_value["total_count"]
    report.content.add_data_missing_value(missing_count=missing_count,
                                          total_count=total_count)

    ### Add Numbering Subsection for data distribution as level 2
    """
    Sample: Dataset distribution
    """
    with open('./sample_data/data_distribution.json', 'r') as f:
        data_dist = json.load(f)

    data_distributions = []
    for k, v in data_dist.items():
        data_distributions.append((k, v))
    report.content.add_data_set_distribution(data_distributions)
    # ###

    ### Add another level 2 header + content under data module
    report.content.add_paragraph_title(text='Some topic under data module')
    report.content.add_paragraph(text="More desc on the topic ...")


    ### Lastly generate report with the writer instance
    report.generate(writer=PdfWriter(name='sample-report'))

if __name__ == "__main__":
    main()

