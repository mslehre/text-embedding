import pandas as pd

# Read in the data
publication_data = pd.read_csv('../data/FIS/Publikationen.csv', sep=';', 
                               names = ["author_ID", "author_name", "person_ID",
                               "inst_ID", "institution", "faculty_ID", "faculty",
                               "journal", "year", "title"], skiprows=1, encoding = 'latin-1')
person_data = pd.read_csv('../data/FIS/Personen_Einrichtungen_2023_06.csv', 
                          sep=';', names = ["person_ID", "lastname", "forename",
                          "institution", "faculty"], skiprows=1, encoding='latin-1')
publication_data['lastname'] = publication_data['person_ID'].apply(lambda x: person_data.loc[person_data['person_ID'] == x, 'lastname'].values[0])
publication_data['forename'] = publication_data['person_ID'].apply(lambda x: person_data.loc[person_data['person_ID'] == x, 'forename'].values[0])
# Write a fuction that finds for each person_ID in publication_data all entries 
# in publication_data with the same person_ID and joins the titles of the
# publications into the same row separared by a tab and adds these publications
# to a new column called 'titles' but only once per person_ID (i.e. the first
# time the person_ID is encountered in the data) and deletes the other rows with
# the same person_ID. The function should return the modified publication_data.
publication_data['titles'] = publication_data.groupby('person_ID')['title'].transform(lambda x: '\t'.join(x))
publication_data.drop_duplicates(subset='person_ID', inplace=True)