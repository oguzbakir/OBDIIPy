# /***************************************************************************/
# /* ELM327 OBDII CAN BUS Diagnostic Software.                               */
# /*                                                                         */
# /*                                                                         */
# /* Class: PDF                                                              */
# /* Create save and print PDF reports.                                      */
# /***************************************************************************/


import os
import io
import PyPDF2
import reportlab.pdfgen.canvas
import reportlab.pdfbase.ttfonts
import ELM327

PDF_Y_MARGIN = 50
PDF_X_MARGIN = 25


class PDF:
    def __init__(self):
        return

    def CreateReport(self, FileName, FontName, TextPages):
        # Create a PDF file to write to.
        SavePDF = PyPDF2.pdf.PdfFileWriter()
        for ThisPage in TextPages:
            # Create a page of the report.
            ThisPageBytes = io.BytesIO()
            ThisPageCanvas = reportlab.pdfgen.canvas.Canvas(ThisPageBytes, pagesize=reportlab.lib.pagesizes.landscape(
                reportlab.lib.pagesizes.A4))
            (PageWidth, PageHeight) = reportlab.lib.pagesizes.landscape(reportlab.lib.pagesizes.A4)
            reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont(FontName, FontName + '.ttf'))
            FontSize = 32
            ThisPageCanvas.setFont(FontName, FontSize)
            yOffset = PageHeight - PDF_Y_MARGIN
            ThisPageCanvas.setFillColorRGB(0.0, 0.0, 0.0)
            ThisPageCanvas.drawString(PDF_X_MARGIN, yOffset, ThisPage[0])
            yOffset -= FontSize
            FontSize = 12
            ThisPageCanvas.setFont(FontName, FontSize)
            for ThisLine in ThisPage[1].split('\n'):
                ThisLineElements = ThisLine.split('|')
                ThisPageCanvas.setFillColorRGB(0.0, 0.0, 0.75)
                ThisPageCanvas.drawString(PDF_X_MARGIN, yOffset, ThisLineElements[ELM327.FIELD_PID_DESCRIPTION])
                if len(ThisLineElements) > ELM327.FIELD_PID_FORMAT_1:
                    ReportText = ThisLineElements[ELM327.FIELD_PID_FORMAT_1]
                    if len(ThisLineElements) > ELM327.FIELD_PID_FORMAT_2:
                        ReportText += " " + ThisLineElements[ELM327.FIELD_PID_FORMAT_2]
                    ThisPageCanvas.setFillColorRGB(0.0, 0.75, 0.0)
                    ThisPageCanvas.drawRightString(PageWidth - PDF_X_MARGIN, yOffset, ReportText)
                yOffset -= FontSize
            ThisPageCanvas.save()
            # Add the report page to the PDF file.
            ThisPageBytes.seek(0)
            NewPdfPage = PyPDF2.pdf.PdfFileReader(ThisPageBytes)
            SavePDF.appendPagesFromReader(NewPdfPage)
        # Save PDF report to disk.
        File = open(FileName, "wb")
        SavePDF.write(File)
        File.close()
