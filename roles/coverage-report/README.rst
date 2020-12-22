Collects coverage data (if any) and generates HTML coverage report.


**Role Variables**

.. zuul:rolevar:: coverage_output_format
    :default: ""

    Format of coverage output file. By default is determined by file contents.

.. zuul:rolevar:: coverage_output_file
    :default: .coverage

    File with coverage tool output.

.. zuul:rolevar:: coverage_output_dir
    :default: .

    Set dir where coverage tool output will be searched.
