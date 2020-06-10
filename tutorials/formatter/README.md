### Contextual AI formatter tutorials

The following notebooks demonstrate different functionality of `contextual-ai` formatter:

#### PDF Report
* :ref:doc:`PDF_Report_Generation.ipynb <tutorials/formatter/tutorial_pdf_report_generation>`:
    * demos for :ref:doc:`xai.formatter <formatter/formatter>` package, it shows how you can format your own 
    PDF report based on the information generated from the other packages. 
    * The report is persist to current directory (default)
    * The report can be generate and re-generate at any step of process 
    (adding contents)
    * The demo generates few sample report:
        * `first-sample-report` - first sample report to show the PDF 
        structure - mainly section title, header and paragraph
        * `sample-report-with-data-section-only` - a sample report generated 
        with only data section has been added
        * `sample-report-with-data-and-feature-section` - another sample 
        report generated after data and feature section has been added
        * `sample-report-with-data-feature-training-section` - sample report 
        generated together with data, feature and training section
        * `sample-report-with-data-feature-training-evaluation-section` - a 
        sample report generated with all sections
        * `sample-report-final-with-summary` - final sample report generated 
        with summary contents as summary page
