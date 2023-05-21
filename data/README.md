# Title

## To create list of profs:
```
Searched his.uni-greifswald.de under 'Personensuche' seperately for 'Professoren', 'Professorinnen', 'Lehrstuhlinhaber' and 'Lehrstuhlinhaberinnen' and copy pasted the resulting lists into a simple text file, then formatted it with bash commands (awk, sed) and some manual corrections into the tab seperated format of:
title first name last name function
Then excluded duplicates with sort -u
```

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
