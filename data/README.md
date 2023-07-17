# Title

## To create list of profs:
```
Searched his.uni-greifswald.de under 'Personensuche' seperately for 'Professoren', 'Professorinnen', 'Lehrstuhlinhaber' and 'Lehrstuhlinhaberinnen' 
and copy pasted the resulting lists into a simple text file, 
then formatted it with bash commands (awk, sed) and some manual corrections into the tab seperated format of:
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

## Table with institute, faculty and web of science ID
Export spreadsheet from Drive in tab-separated format on  Mo 5. Jun 13:46:39 CEST 2023 to obtain
`proflist-drieve5Jun.tsv`.

Create master table with profs
```
FNAME=prof.tbl
echo -e "id\tlastname\tfirstname\tinstitute\tfaculty\ttitle\tWoSID" > $FNAME
tail -n +2  proflist-drive5Jun.tsv | perl -ne 'chomp; @f = split /\t/; $i=0 if !defined $i; print "$i\t$f[2]\t$f[1]\t$f[7]\t$f[6]\t$f[0]\t$f[5]\n"; $i++' >> $FNAME
```
```
# head -n 5 prof.tbl
# tail  -n 5 prof.tbl
id      lastname        firstname       institute       faculty title   WoSID
0       Link    Andreas Institut für Pharmazie  MNF     Prof. Dr. rer. nat.     1152429
1       Frosch  Christian       Caspar-David-Friedrich-Institut CDFI    Prof.
2       Wacker  Alexander       Zoologisches Institut und Museum        MNF     Prof. Dr.       1070397
3       Tamminga        Allard  Institut für Philosophie        PHIL    Prof. Dr.       16382291
...
132     Kuhn    Thomas  Theologische Fakultät   THEO    Prof. Dr. theol.
133     Braune-Krickau  Tobias  Theologische Fakultät   THEO    Prof. Dr.       5781747
134     Fried   Torsten Historisches Institut   PHIL    Prof. Dr.
135     Soltau  Michael Caspar-David-Friedrich-Institut CDFI    Prof.
136     Warr    Laurence        Institut für Geographie und Geologie    MNF     Prof. PhD       16185175
```

### Mapping Institutes and Faculty to Colors

Faculties
```
cut -f 5 prof.tbl | sort -u > colors.fak.tbl
```
manually add colors `colors.fak.tbl`:
```
# more colors.fak.tbl
faculty color
MNF     0
PHIL    1
RSF     2
THEO    3
CDFI    4
CSFI    5
```

Institutes
```
echo -e "institute_long\tcolor\tinstitute_short" > colors.inst.tbl
cut -f 4 prof.tbl | sort -u  | grep -Pv "^$" | perl -ne 'chomp; @f = split /\t/; $i=0 if !defined $i; print "$f[0]\t$i\t$f[0]\n"; $i++' >> colors.inst.tbl
```
manually edit `colors.inst.tbl` and short the names:
```
# head colors.inst.tbl
faculty color
institute_long  color   institute_short
Caspar-David-Friedrich-Institut 1       CDFI
Fachbereich Rechtswissenschaften        2       Jura
Fachbereich Wirtschaftswissenschaften   3       Wiwi
Historisches Institut   4       Geschichte
Institut für Anatomie und Zellbiologie  6       Anatomie
Institut für Anglistik und Amerikanistik        7       Anglistik
Institut für Baltistik  8       Baltistik
Institut für Biochemie  9       Biochemie
Institut für Botanik und Landschaftsökologie    10      Botanik
```

### Remove links from publication lists

```
cd publications
for f in *.txt; do cat $f | perl -pe 's/\t.*//' > $f.new; mv $f.new $f; done
```

### Remove WebOfScience ID from the first line of each publication list

```
cd publications
for f in *.txt; do cat $f | perl -pe 's/^([^\d]+)\s?,\d+;/$1/' > $f.new; mv $f.new $f; done
```

## To create pre-version of list of publishers:
Read in `Publikationen.csv` and `Personen_Einrichtungen_2023_06.csv` from 
`/data/FIS` and add two new columns `lastname` and `forename` to 
`Publikationen.csv`. The last- and fornames are columns in 
`Personen_Einrichtungen_2023_06.csv`. After that, create another new column 
`titles` for `Publikationen.csv` that contains all publications that are listed 
in this dataframe for the respective person and delete duplicate entries of
persons. Then create a new column `institution` that contains only the part of 
the description of the institution in `Publikationen.csv` up to the first `/`.
Delete unnecessary columns `author_ID`, `journal`, `year` and `title` and write
the resulting dataframe to `/data/FIS/persons.csv`.
