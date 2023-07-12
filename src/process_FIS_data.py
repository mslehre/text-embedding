import pandas as pd

# Read in the data of Publikationen.csv and Personen_Einrichtungen_2023_06.csv
publication_data = pd.read_csv('../data/FIS/Publikationen.csv', sep=';', 
                               names = ["author_ID", "author_name", "person_ID",
                               "inst_ID", "institution_long", "faculty_ID", 
                               "faculty", "journal", "year", "title"], 
                               skiprows=1, encoding = 'latin-1')
person_data = pd.read_csv('../data/FIS/Personen_Einrichtungen_2023_06.csv', 
                          sep=';', names = ["person_ID", "lastname", "forename",
                          "institution", "faculty"], skiprows=1, 
                          encoding='latin-1')

# Add two new columns to publication_data with full names of authors if they
# exist in person_data

# Create empty lists to store the lastnames and forenames
lastnames = []
forenames = []    
# Iterate over the person_IDs in the publication_data
for person_ID in publication_data["person_ID"]:
    # Check if the person_ID is in the person_data
    if person_ID in person_data["person_ID"].values:
        # If it is in the person_data, get the lastname and forename
        lastname = person_data.loc[person_data["person_ID"] == person_ID, "lastname"].values[0]
        forename = person_data.loc[person_data["person_ID"] == person_ID, "forename"].values[0]
    else:
        # If it is not in the person_data, set the lastname and forename to 
        # "NaN"
        lastname = "NaN"
        forename = "NaN"
    # Append the lastname and forename to the lists
    lastnames.append(lastname)
    forenames.append(forename)    
# Add the lists as new columns to the publication_data dataframe
publication_data["lastname"] = lastnames
publication_data["forename"] = forenames

# Find for each person_ID in publication_data all entries in publication_data 
# with the same person_ID and join the titles of the publications into the same 
# row separared by a tab and add these publications to a new column called 
# 'titles', but only once per person_ID (i.e. the first time the person_ID is 
# encountered in the data) and delete the other rows with the same person_ID.
publication_data['titles'] = publication_data.groupby('person_ID')['title'].transform(lambda x: '\t'.join(x))
publication_data.drop_duplicates(subset='person_ID', inplace=True)

def write_publications(person_ID):
    # Get the row of the person
    row = modified_publication_data.loc[modified_publication_data["person_ID"] == person_ID]
    # Get the titles of the person_ID and separate the tab-separated titles by
    # a new line
    titles = row["titles"].values[0].replace("\t", "\n")
    # Get lastname and forename of the person
    lastname = row["lastname"].values[0]
    forename = row["forename"].values[0]
    fileText = ""
    # Test if forename and lastname of the person exist
    if (not pd.isnull(lastname) and not pd.isnull(forename)):
        fileText += lastname + ", " + forename + "\t" + str(person_ID) + "\n" + titles
    else:
        # Get the author_name of the person if forename and lastname do not
        # exist
        author_name = row["author_name"].values[0]
        fileText += author_name + "\t" + str(person_ID) + "\n" + titles
    # Write the publications to a file
    with open('../data/FIS_publications/' + str(person_ID) + '.txt', 'w') as file:
        file.write(fileText)
        file.close()

# Drop the columns 'author_ID', 'journal', 'year', 'title' and 'titles' of 
# publication_data
titles = publication_data["titles"].values
publication_data.drop(columns=['author_ID', 'journal', 'year', 'title', 'titles'], 
                      inplace=True)

institution_short = []
# Iterate over the institution_long column of publication_data
for institution in publication_data["institution_long"]:
    # Get the first part until '/' of the institution_long
    institution_short.append(institution.split("/")[0].strip())
# Add the institution_short column to publication_data
publication_data["institution"] = institution_short
# Drop the institution_long column of publication_data
# publication_data.drop(columns=['institution_long'], inplace=True)
publication_data.to_csv('../data/FIS/persons.csv', sep = ';', 
                        na_rep = 'NaN', encoding = 'latin-1')
modified_publication_data = pd.read_csv('../data/FIS/persons_modified_names.csv',
                                        sep = ';', names = ["line", 
                                        "author_name", "person_ID", "inst_ID",
                                        "institution_long", "faculty_ID", 
                                        "faculty", "lastname", "forename",
                                        "institution"], skiprows = 1, 
                                        encoding = 'latin-1')
modified_publication_data.drop(columns=['line'], inplace=True)
modified_publication_data["titles"] = titles

# Get all person_IDs in publication_data to write publicaion lists for each
# person_ID add FIS in front of the filename!!!
#person_IDs = modified_publication_data["person_ID"].values
#for person_ID in person_IDs:
#    write_publications(person_ID)

# Get unique values of the institution column of modified_publication_data
institutions = modified_publication_data["institution"].unique()
print(institutions)

# Make a dictionary
institutions_dict = {}
institutions_dict['Zentrum für Innere Medizin'] = 'Innere Medizin'
institutions_dict['Zentrum für Kinder- und Jugendmedizin'] = 'Kinder- und Jugendmedizin'
institutions_dict['Institut für Community Medicine'] = 'Community Medicine'
institutions_dict['Zentrum für Zahn-, Mund- und Kieferheilkunde'] = 'Zahn-, Mund- und Kieferheilkunde'
institutions_dict['Deutsches Zentrum für Neurodegenerative Erkrankungen Rostock'] = 'Neurodegenerative Erkrankungen'
institutions_dict['Institut für Pharmakologie'] = 'Pharmakologie'
institutions_dict['Institut für Pharmazie'] = 'Pharmazie'
institutions_dict['Institut für Klinische Chemie und Laboratoriumsmedizin'] = 'Klinische Chemie und Laboratoriumsmedizin'
institutions_dict['Klinik und Poliklinik für Unfall-, Wiederherstellungschirurgie und Rehabilitative Medizin'] = 'Unfallchirurgie'
institutions_dict['Institut für Medizinische Psychologie'] = 'Medizinische Psychologie'
institutions_dict['Zentrum für Radiologie'] = 'Radiologie'
institutions_dict['Klinik und Poliklinik für Neurochirurgie'] = 'Neurochirurgie'
institutions_dict['Institut für Immunologie und Transfusionsmedizin'] = 'Immunologie und Transfusionsmedizin'
institutions_dict['Institut für Pathologie'] = 'Pathologie'
institutions_dict['Institut für Pharmazie, AK Klinische Pharmazie (Leitung: Prof. Dr. Christoph Ritter)'] = 'Pharmazie'
institutions_dict['Klinik und Poliklinik für Psychiatrie und Psychotherapie'] = 'Psychiatrie und Psychotherapie'
institutions_dict['Institut für Mathematik und Informatik'] = 'Mathematik und Informatik'
institutions_dict['Institut für Physik'] = 'Physik'
institutions_dict['Theologische Fakultät'] = 'Theologie'
institutions_dict['Fachbereich Wirtschaftswissenschaften'] = 'Wiwi'
institutions_dict['Klinik und Poliklinik für Chirurgie'] = 'Chirurgie'
institutions_dict['Institut für Humangenetik'] = 'Humangenetik'
institutions_dict['Klinik und Poliklinik für Hals-Nasen-Ohrenkrankheiten, Kopf- und Halschirurgie'] = 'HNO'
institutions_dict['Klinik und Poliklinik für Orthopädie und Orthopädische Chirurgie'] = 'Orthopädie'
institutions_dict['Zoologisches Institut und Museum'] = 'Zoologie'
institutions_dict['Institut für Psychologie'] = 'Psychologie'
institutions_dict['Institut für Medizinische Biochemie und Molekularbiologie'] = 'Mediz. Biochemie und Molekularbiologie'
institutions_dict['Institut für Mikrobiologie'] = 'Mikrobiologie'
institutions_dict['Klinik und Poliklinik für Augenheilkunde'] = 'Augenheilkunde'
institutions_dict['Institut für Rechtsmedizin'] = 'Rechtsmedizin'
institutions_dict['Klinik und Poliklinik für Urologie'] = 'Urologie'
institutions_dict['Interfakultäres Institut für Genetik und Funktionelle Genomforschung'] = 'Genetik und Funktionelle Genomforschung'
institutions_dict['Beschaffung'] = 'Beschaffung'
institutions_dict['Klinik und Poliklinik für Hautkrankheiten'] = 'Hautkrankheiten'
institutions_dict['Institut für Hygiene und Umweltmedizin'] = 'Hygiene und Umweltmedizin'
institutions_dict['Institut für Botanik und Landschaftsökologie'] = 'Botanik'
institutions_dict['Klinik und Poliklinik für Neurologie'] = 'Neurologie'
institutions_dict['Institut für Anatomie und Zellbiologie'] = 'Anatomie'
institutions_dict['Psychologie'] = 'Psychologie'
institutions_dict['Unfall-, Wiederherstellungschirurgie und Rehabilitative Medizin'] = 'Unfallchirurgie'
institutions_dict['Psychiatrie und Psychotherapie'] = 'Psychiatrie und Psychotherapie'
institutions_dict['Community Medicine'] = 'Community Medicine'
institutions_dict['Zahn-, Mund- und Kieferheilkunde'] = 'Zahn-, Mund- und Kieferheilkunde'
institutions_dict['Hals-Nasen-Ohrenkrankheiten, Kopf- und Halschirurgie'] = 'HNO'
institutions_dict['Immunologie und Transfusionsmedizin'] = 'Immunologie und Transfusionsmedizin'
institutions_dict['Biochemie'] = 'Biochemie'
institutions_dict['Genetik und Funktionelle Genomforschung'] = 'Genetik und Funktionelle Genomforschung'
institutions_dict['Neurologie'] = 'Neurologie'
institutions_dict['Frauenheilkunde und Geburtshilfe'] = 'Frauenheilkunde und Geburtshilfe'
institutions_dict['Urologie'] = 'Urologie'
institutions_dict['Neurodegenerative Erkrankungen Rostock'] = 'Neurodegenerative Erkrankungen'
institutions_dict['Mikrobiologie'] = 'Mikrobiologie'
institutions_dict['Hygiene und Umweltmedizin'] = 'Hygiene und Umweltmedizin'
institutions_dict['Radiologie'] = 'Radiologie'
institutions_dict['Chirurgie'] = 'Chirurgie'
institutions_dict['Humangenetik'] = 'Humangenetik'
