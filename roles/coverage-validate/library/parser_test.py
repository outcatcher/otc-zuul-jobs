import os
import unittest

from .report_parser import NotEnoughCoverage, parse, validate

BASE_PATH = os.path.abspath(f"{os.path.dirname(__file__)}/test-fixtures")

COBERTURA_XML = f"{BASE_PATH}/cobertura.xml"


def _cobertura():
    """Parse cobertura xml report"""
    return parse(COBERTURA_XML, "xml_cobertura")


class TestCobertura(unittest.TestCase):

    def test_parse(self):
        _cobertura()

    def test_parse_no_explicit(self):
        parse(COBERTURA_XML)

    def test_validate(self):
        validate(_cobertura(), 85, 83)

    def test_validate_low_total(self):
        self.assertRaisesRegex(NotEnoughCoverage,
                               "^Total coverage .+",
                               validate, _cobertura(), 100, 83)

    def test_validate_low_file(self):
        self.assertRaisesRegex(NotEnoughCoverage,
                               "^Coverage for the following files.+",
                               validate, _cobertura(), 85, 100)


if __name__ == '__main__':
    unittest.main()
