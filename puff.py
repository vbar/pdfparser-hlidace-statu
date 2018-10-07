import re
from StringIO import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter

class Puff:
    def __init__(self, source_file):
        self.source_file = source_file
        self.puff = {}

        with open(source_file, 'r') as f:
            # https://quantcorner.wordpress.com/2014/03/16/parsing-pdf-files-with-python-and-pdfminer/
            parser = PDFParser(f)

            document = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            laparams = LAParams()

            device = TextConverter(rsrcmgr, retstr, codec = 'utf-8', laparams = laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
                self.add_text(retstr.getvalue())

    def reexpand(self, key):
        return self.puff.get(key, key)

    def add_text(self, text):
        for ln in text.splitlines():
            # one space good, more spaces bad
            v = re.sub("\\s+", " ", ln.strip())
            if v:
                k = re.sub(" ", "", v)
                self.puff[k.decode('utf-8')] = v
