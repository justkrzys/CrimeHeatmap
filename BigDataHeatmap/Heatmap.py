import pandas
import matplotlib.pyplot as plt

file = open('Crimes2010Present.csv')
df = pandas.read_csv(file)

file1 = open('Vacant.csv')
vacant = pandas.read_csv(file1)

def ward_count(df, col, value, unique_id, ward_num):
    '''Returns count of unique_id in df ward_num rows w/entry value in column col'''
    rows = df[ df[col] == value] # boolean slice of rows we want
    if ward_num not in rows['Ward'].values:
        return 0
    grouped = rows.groupby('Ward')
    return grouped[unique_id].count()[ward_num]

def make_ward_dictionary(df, col, value, unique_id):
    '''Takes in paramaters for dataframe, column, value, and unique_id and returns a dictionary with the ward number as keys and its respective values'''
    ward_dictionary = {}
    for i in range(51):
        if i == 0:
            continue
        ward_dictionary[i] = ward_count(df, col, value, unique_id, i)
    return ward_dictionary

file.close()
file1.close()

dictionary_narc = make_ward_dictionary(df, 'Primary Type', 'NARCOTICS', 'Case Number')

max_narc = max(list(dictionary_narc.values()))

#Narcotics are arbitrarily weighted 2.5 more than abandoned/vacant buildings as an example of combining data
for val in range(len(dictionary_narc)):
    dictionary_narc[val+1] /= max_narc
    dictionary_narc[val+1] *= 2.5

dictionary_vacant = make_ward_dictionary(vacant, 'SERVICE REQUEST TYPE', 'Vacant/Abandoned Building', 'SERVICE REQUEST NUMBER')

max_vacant = max(list(dictionary_vacant.values()))

for val in range(len(dictionary_vacant)):
    dictionary_vacant[val+1] /= max_vacant
    
weighted_dict = {}

for i in range(50):
    weighted_dict[i+1] = dictionary_narc[i+1] + dictionary_vacant[i+1]
    
def ward_array(dictionary):
    '''Creates a 10x5 array using values from the dictionary parameter'''
    matrix = []
    
    for j in range(10):
        new_row = []
        for i in range(5):
            new_row.append(0)
        matrix.append(new_row)
    
    a = 0
    b = 0
    
    for key in dictionary:
        matrix[a][b] = dictionary[key]
        b += 1
        if b % 5 == 0:
            b = 0
        if key % 5 == 0:
            a += 1
    
    return(matrix)

#The three different predefined arrays which can be graphed
narc_array = ward_array(dictionary_narc)
vacant_array = ward_array(dictionary_vacant)
weighted_array = ward_array(weighted_dict)

#Graphing code
plt.pcolor(narc_array)
plt.colorbar()
plt.summer()
plt.title('Narcotics by Ward')
plt.xlabel('Ward Number Mod 5 on Right')
