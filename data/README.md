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

## To create pre-version of list of publishers of FIS data:
Read in `Publikationen.csv` and `Personen_Einrichtungen_2023_06.csv` from 
`/data/FIS` and change `Publikationen.csv` by adding the following columns

* `lastname` of the person from `Personen_Einrichtungen_2023_06.csv`
* `forename` of the person from `Personen_Einrichtungen_2023_06.csv`
* `titles` that contains all publications that are listed in this dataframe for 
the respective person 
* `institution` that contains only the part of the description of the institution in `Publikationen.csv` up to the first `/`

and deleting the columns

* `author_ID`
* `journal`
* `year`
* `title`

In addition, the duplicate rows of persons are deleted and the resulting 
dataframe is written to `/data/FIS/persons.csv`.

## Change names with special characters:
Since there has been a problem with the encoding of 
`Personen_Einrichtungen_2023_06.csv` there is a problem with special characters 
in the `lastnames` and `forenames` column in `/data/FIS/persons.csv`. Therefore,
manually correct missing characters in these columns and save resulting file as
`/data/FIS/persons_modified_names.csv`.

## To create final version of list of publishers of FIS data:
Read in `/data/FIS/persons_modified_names.csv` and change the file by deleting 
the columns:
* `line`, the row in the dataframe
* `inst_ID`, the ID of the institution
* `faculty_ID`, the ID of the faculty

Modify the ID by adding `FIS_` as prefix. Then add another faculty, 
which is `Caspar-David-Friedrich Institut`, and change the faculty of those 
persons whose institution is `Caspar-David-Friedrich Institut` to the new 
faculty. Replace each faculty name in `faculty` column with the abbreviation of 
the faculty name. Reorder and rename the columns of the dataframe and write the 
resulting dataframe to `/data/FIS/publishers.tbl`.

## Create publication lists:
For each person in `/data/FIS/persons_modified_names.csv` write all publications
separated by a new line of this person to a file, if the person has more than 
two publications. These publication lists are saved in the directory 
`data/FIS_publications` and the name of the publication list is the person ID of
the person of which the publication list is. Apart from the publications the
publication list contains the name of the person and the person ID.
Example of publication list `FIS_2.txt`:
```
Philipp, Klaus-Peter	FIS_2
Tödliche Verletzungen, verursacht durch eine Kuh
Untersuchungsstelle für Gewaltopfer am Institut für Rechtsmedizin der Universitätsmedizin Greifswald - Bilanz der ersten 3 Jahre
Klärung eines tödlichen Arbeitsunfalls durch Rekonstruktion
Die Rekonstruktion am Ereignisort als wichtiges Instrument in der Zusammenarbeit zwischen Rechtsmedizin und Ermittlungsbehörden
Der vermeidbare (?) Jagdunfall  tödliche Oberschenkelverletzung durch ein Wildschwein
Die ärztliche Leichenschau  Schritt für Schritt
Zur subjektiven Wahrnehmbarkeit von Alkohol in Wasser
Die mobile rechtsmedizinische Kinderschutzambulanz am Institut für Rechtsmedizin Greifswald: Entwicklung und erste Erfahrungen
Die ärztliche Leichenschau  Schritt für Schritt The medical post-mortem examination - step by step
```

## Table containing the abbreviation of the institutions and colors:
The file `FIS.colors.inst.tbl` in `/data/FIS` contains the manually created 
abbreviations of the institutions in `/data/FIS/publishers.tbl` and a number 
representing a color.
```
head FIS.colors.inst.tbl 
institute       color
Brustzentrum    0
Urologie        1
Bioinformatik   2
Unfallchirurgie 3
Wiwi    4
Mikrobiologie   5
Neurologie      6
Pathophysiologie        7
Universitätsapotheke    8
```

## Table containing the abbreviation of the faculty and colors:
Manually create the tab separated file `FIS.colors.fak.tbl` that contains the
manually created abbreviations of the faculties in `/data/FIS/publishers.tbl` 
and a number representing a color.
```
head FIS.colors.fak.tbl 
faculty color
MNF     0
PHIL    1
RSF     2
THEO    3
CDFI    4
MED     5
INTERFAK        6
VERW    7
```

## File FIS.inst.abbrev.tbl
Make a tab separated file that contains the short form of each institution in
`/data/FIS/publishers.tbl` and the abbreviation for this short form that is 
created manually.
```
head FIS.inst.abbrev.tbl
institute_long  institute_short
Zentrum für Innere Medizin      Innere Medizin
Zentrum für Kinder- und Jugendmedizin   Kinder- und Jugendmedizin
Institut für Community Medicine Community Medicine
Zentrum für Zahn-, Mund- und Kieferheilkunde    Zahn-, Mund- und Kieferheilkunde
Deutsches Zentrum für Neurodegenerative Erkrankungen Rostock    Neurodegenerative Erkrankungen
Institut für Pharmakologie      Pharmakologie
Institut für Pharmazie  Pharmazie
Institut für Klinische Chemie und Laboratoriumsmedizin  Klinische Chemie und Laboratoriumsmedizin
Klinik und Poliklinik für Unfall-, Wiederherstellungschirurgie und Rehabilitative Medizin       Unfallchirurgie
```

## File FIS.fak.abbrev.tbl
Make a tab separated file that contains the name of each faculty in
`/data/FIS/publishers.tbl` and an abbreviation of the faculty that is 
created manually.
```
head FIS.fak.abbrev.tbl
faculty_long    faculty_short
Mathematisch-Naturwissenschaftliche Fakultät    MNF
Philosophische Fakultät PHIL
Rechts- und Staatswissenschaftliche Fakultät    RSF
Theologische Fakultät   THEO
Caspar-David-Friedrich Institut CDFI
Universitätsmedizin Greifswald  MED
Interfakultär   INTERFAK
Zentrale Verwaltung     VERW
```
