import pytest  # type: ignore
from qa_std import qa_diagnostics as Diagnostics


def test_qa_def() -> None:
    assert Diagnostics.ModDiagnostics.qa_def()


def test_qa_dtc() -> None:
    assert Diagnostics.ModDiagnostics.qa_dtc()


def test_locale() -> None:
    assert Diagnostics.ModDiagnostics.locale()


def test_src_files() -> None:
    assert Diagnostics.ModDiagnostics.check_source_files()
