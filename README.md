# pdfparser-hlidace-statu

This is a single-purpose script - not only useless by itself, but even
when integrated (or planned to be integrated) into a larger pipeline,
it's of interest only to people who 1) speak Czech, and 2) are
interested in Czech Open data and/or public procurement.

www.hlidacstatu.cz indexes and curates data made available
(compulsorily and not very conveniently) by Czech public
administration - public contracts, companies supplying them,
politicians on their boards etc. Among other things, it publishes a
developer API (described at https://hlidacstatu.docs.apiary.io/)
allowing registered 3rd parties to upload structured data they
consider relevant to the site's mission.

One such dataset is the list of public electromobile charging
stations, available from
https://www.mpo.cz/cz/energetika/statistika/statistika-cerpacich-stanic-pohonnych-hmot/seznam-verejnych-dobijecich-stanic-_-stav-k-31--10--2019--250631/
as a PDF file containing a simple table. The make-json.py script
converts it into a machine-readable format.

make-json.py depends on PDFMiner (www.github.com/euske/pdfminer). For
configuration, it requires a config.json file in the current
directory, with a mandatory setting "sourceFile" for path to the
downloaded PDF. The "targetDir" setting specifies the output
directory, by default "json". A separate file is generated there for
every table row, in a format suitable for upload by
www.github.com/vbar/krmic-hlidace-statu . Note the script overwrites
files in "targetDir" if they already exist - if you want to preserve
results of a specific run, copy them somewhere else.

Generated JSON conforms to the included schema; the full JSON for
registration of a new dataset (in a format documented at
https://hlidacstatu.docs.apiary.io/) is also included, as an example.
