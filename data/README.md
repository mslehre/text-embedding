# Title

## Split list of profs
```
wc -l proflist 
137 proflist
```

Split into one chunk for each developer
```
split -l 20 -a 1 --additional-suffix=.txt proflist proflist-
```

| developer | chunk|
|---|--|
|MS | a|
|NJ | b|
|FB | c|
|LR | d|
|MG | e|
|HT | f|
|LH | g|


links-{chunk}.txt