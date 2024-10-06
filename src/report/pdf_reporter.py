import os.path
import uuid
from pathlib import Path

from fpdf import FPDF

from src.config import static_base_config
from src.report.schemas import ReportsListSchema


class PDFReporter:
    def __init__(self, data: ReportsListSchema):
        self.data = data
        self.pdf = FPDF()
        self.filename = self.data.title + str(uuid.uuid4())[:8] + ".pdf"


    def create_report(self) -> None:
        self.pdf.add_page()
        self.pdf.set_font("Times", "B", 24)
        self.pdf.cell(0, 10, self.data.title, ln=True, align='C')


    def save_pdf(self) -> str:
        if not os.path.exists(static_base_config.MEDIA_NAME):
            os.makedirs(static_base_config.MEDIA_NAME)

        file_path = os.path.join(static_base_config.MEDIA_NAME, self.filename)

        self.pdf.output(file_path)

        return file_path
