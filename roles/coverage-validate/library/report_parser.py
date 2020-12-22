import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Callable, Dict, List
from xml.etree.ElementTree import Element

from lxml import etree


class NotEnoughCoverage(Exception):
    """Coverage value is too low"""

    def __init__(self, *msg_parts):
        super().__init__("\n".join(msg_parts))


class UnsupportedFormat(Exception):
    """Unsupported coverage file format"""


@dataclass
class CheckResults:
    """Results of coverage report parsing"""

    total: float
    per_file: Dict[str, float]


def parse_cobertura(file_path: str) -> CheckResults:
    """Parse XML file in cobertura format"""
    root = etree.parse(file_path).getroot()
    total_prc = float(root.attrib["line-rate"]) * 100

    classes: List[Element] = root.xpath("//class")
    pkg_cov = {}
    for pkg in classes:
        name = pkg.attrib["filename"]
        line_rate = float(pkg.attrib["line-rate"])
        pkg_cov[name] = line_rate * 100

    return CheckResults(total_prc, pkg_cov)


FMT_MAPPING: Dict[str, Callable[[str], CheckResults]] = {
    "xml_cobertura": parse_cobertura,
}


def determine_fmt(file_path) -> str:
    """Get file report format"""
    cob = "xml_cobertura"
    txt_go = "txt_golang"
    coverage = ".coverage"

    with open(file_path) as r_f:
        first_line = r_f.readline()
    if first_line.startswith("<?xml version=\"1.0\""):
        return cob
    if first_line.startswith("mode: "):
        return txt_go
    if first_line.startswith("!coverage.py: This is a private format,"
                             "don't read it directly!"):
        return coverage
    return "unknown"


def parse(file_path: str, fmt: str = None) -> CheckResults:
    """Parse given coverage report file"""

    if fmt is None:
        fmt = determine_fmt(file_path)

    fnc = FMT_MAPPING.get(fmt, None)
    if fnc is None:
        valid_fmts = ", ".join(FMT_MAPPING)
        raise UnsupportedFormat(
            f"Only the following formats are supported: {valid_fmts}")
    return fnc(file_path)


def validate(results: CheckResults, total_min: float, file_min: float) -> None:
    """Raises `NotEnoughCoverage` if coverage minimum values not reached"""

    if results.total < total_min:
        raise NotEnoughCoverage(
            f"Total coverage ({results.total}%) is less than {total_min}%")

    messages = []
    for fl, cov in results.per_file.items():
        if cov >= file_min:
            continue
        messages.append(f"{fl}: {cov}%")
    if messages:
        raise NotEnoughCoverage(
            f"Coverage for the following files is less than {file_min}%:",
            *messages
        )


if __name__ == '__main__':
    AGP = ArgumentParser(description="Parse coverage tool output file and check if coverage passes expectations")
    AGP.add_argument("results", help="Coverage tool output file")
    AGP.add_argument("--min-file", dest="min_file", help="Minimum file/module coverage percent, e.g. 80", default=60)
    AGP.add_argument("--min-total", dest="min_total", help="Minimum total coverage percent, e.g. 90", default=80)
    AGP.add_argument("--rc0", help="Make return code always to be 0", default=False, action="store_true")
    AGP.add_argument("--format", help="Coverage output format", default=None)
    ARGS = AGP.parse_args()

    RES = parse(ARGS.results, ARGS.format)
    try:
        validate(RES, ARGS.min_total, ARGS.min_file)
    except NotEnoughCoverage:
        sys.exit(not ARGS.rc0)
