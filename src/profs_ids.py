import os
from settings import DATA_DIR

def write_profs_and_id():
    proflist = open (os.path.join(DATA_DIR, "prof.tbl"), "r")
    proflist_lines = proflist.readlines()
    f = open(os.path.join(DATA_DIR, "profs_and_ids.tbl"), "w")
    f.write("")
    f.close()
    f = open(os.path.join(DATA_DIR, "profs_and_ids.tbl"), "a")
    proflist_lines.pop(0)
    for line in proflist_lines:
        this_line = line.split("\t")
        f.write(this_line[0] + "\t" + this_line[2] + " " + this_line[1] + "\n")
    f.close()
