#!/usr/bin/env python

import csv
with open("punchtape.csv","rb") as source:
    rdr= csv.reader( source )
    with open("result.csv","wb") as result:
        wtr= csv.writer( result )
        for r in rdr:
		if r[14]:
			wtr.writerow( (r[1], r[2], r[14], r[15]) )