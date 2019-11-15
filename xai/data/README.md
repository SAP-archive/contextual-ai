# Data Module

This module provides data statistical analysis and data validation functions.


:py:meth:`Data explorer package <data.explorer>` contains various data analyzers for a range of data types. 
Each analyzer feeds on incoming samples of a particular data type and 
generates aggregated statistics for all previously fed samples.
Currently supported data types include categorical, numerical, datetime and text.


:py:meth:`Data validator package <data.validator>` mainly hosts two types of validators: a dataframe validator which
is capable of single-dataframe validation and multi-dataframe relation validation, 
and an enum validator for possible enum keys validation.



