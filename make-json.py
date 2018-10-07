#!/usr/bin/python

import json
import os
from pdftables.pdf_document import PDFDocument
from pdftables.pdftables import page_to_tables
from puff import Puff

def get_mandatory(cfg, name):
    v = cfg.get(name)
    if v is None:
        raise Exception("define %s in config.json" % name)

    return v

def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

# pdftables removes spaces from multi-word cells, although the
# underlying PDFMiner parses them correctly - so let's process the
# source twice: in this class with pdftables, and in the base with
# PDFMiner, creating a map from shrunken to correct strings.
class Generator(Puff):
    def __init__(self, cfg):
        Puff.__init__(self, get_mandatory(cfg, "sourceFile"))
        self.target_dir = cfg.get("targetDir", "json")
        ensure_dir(self.target_dir)

    def run(self):
        doc = PDFDocument.from_path(self.source_file)

        for page_number, page in enumerate(doc.get_pages()):
            if page_number: # skip title page
                tables = page_to_tables(page)
                for table in tables:
                    for row in table.data:
                        if len(row) == 8:
                            row_id = None
                            try:
                                row_id = int(row[1])
                            except ValueError:
                                pass

                            if row_id is not None:
                                self.handle_row(row_id, row[2:])
        
    def handle_row(self, row_id, row_tail):
        target_path = os.path.join(self.target_dir, "%d.json" % row_id)
        with open(target_path, 'wb') as f:
            json.dump({
                "Id": str(row_id),
                "street": self.reexpand(row_tail[0].strip()),
                "zip": row_tail[1].strip(),
                "municipality": self.reexpand(row_tail[2].strip()),
                "lau1": row_tail[3].strip(),
                "charging_point_count": int(row_tail[4]),
                "since": row_tail[5].strip()
            }, f, ensure_ascii=False)
    
def main():
    with open("config.json") as cf:
        cfg = json.load(cf)

    gen = Generator(cfg)
    gen.run()
    
if __name__ == "__main__":
    main()
                        
    
