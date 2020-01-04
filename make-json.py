#!/usr/bin/python3

import json
import os
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator


def get_mandatory(cfg, name):
    v = cfg.get(name)
    if v is None:
        raise Exception("define %s in config.json" % name)

    return v


def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


class Generator:
    def __init__(self, cfg):
        self.source_file = get_mandatory(cfg, "sourceFile")
        self.target_dir = cfg.get("targetDir", "json")
        ensure_dir(self.target_dir)
        self.space_rx = re.compile("\\s+")

    def run(self):
        with open(self.source_file, 'rb') as fp:
            parser = PDFParser(fp)
            document = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            first = True
            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
                if first: # skip title page
                    first = False
                else:
                    layout = device.get_result()
                    self.process(layout)

    def process(self, layout):
        height = 0
        columns = [] # of list of height length
        for obj in layout:
            if isinstance(obj, LTTextBoxHorizontal):
                raw = obj.get_text()
                col = raw.split("\n")
                l = len(col)
                # remember columns of maximum height
                if l > height:
                    height = l
                    columns = []

                if l == height:
                    columns.append(col)

        if len(columns) != 7:
            raise Exception("table not found")

        for row in map(list, zip(*columns)): # transpose
            self.handle_row(row)

    def handle_row(self, row):
        try:
            row_id = int(row[0])
        except ValueError:
            return # skip empty row (normally last one on page)

        target_path = os.path.join(self.target_dir, "%d.json" % row_id)
        with open(target_path, 'w') as f:
            json.dump({
                "Id": str(row_id),
                "street": self.respace(row[1]),
                "zip": self.respace(row[2], ""),
                "municipality": self.respace(row[3]),
                "lau1": row[4].strip(),
                "charging_point_count": int(row[5]),
                "since": row[6].strip()
            }, f, ensure_ascii=False)

    def respace(self, item, repl=" "):
        return self.space_rx.sub(repl, item.strip())


def main():
    with open("config.json") as cf:
        cfg = json.load(cf)

    gen = Generator(cfg)
    gen.run()

if __name__ == "__main__":
    main()
