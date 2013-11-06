#!/usr/bin/env python

import csv
with open("plaintext_table.csv","rb") as source:
    rdr= csv.reader( source )
    with open("plaintext_lookup.csv","wb") as result:
        wtr= csv.writer( result )
        for r in rdr:
		if r[12]:
			wtr.writerow( (r[1], r[2], r[3], r[4]) )
