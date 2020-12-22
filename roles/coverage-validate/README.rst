Validates if test coverage matches given validations.


**Role Variables**

.. zuul:rolevar:: coverage_validate
    :default: false

    Enable coverage validation

.. zuul:rolevar:: coverage_fail
    :default: true

    Make failing coverage return exit code 1.

.. zuul:rolevar:: coverage_output_format
    :default: ""

    Format of coverage output file. By default is determined by file contents.

.. zuul:rolevar:: coverage_output_file
    :default: .coverage

    File with coverage tool output.

.. zuul:rolevar:: coverage_output_dir
    :default: .

    Set dir where coverage tool output will be searched.

.. zuul:rolevar:: coverage_min_total
    :default: 80%

    Set total coverage minimum.

.. zuul:rolevar:: coverage_min_file
    :default: 70%

    Set single source file coverage minimum.
