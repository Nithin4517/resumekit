"""resumekit: tailor, build and check ATS-friendly .docx resumes."""
from .builder import build, build_from_files, merge, to_pdf
from .bold import bold_docx
from .lint import lint
from .check_pdf import check_pdf
from .screen import screen

__all__ = ["build", "build_from_files", "merge", "to_pdf", "bold_docx", "lint", "check_pdf", "screen"]
__version__ = "0.2.0"
