import csv
import math
from collections import defaultdict
from collections import Counter
import re
#1:
def rangeToAvg(data):
    for row in data:
        match = re.match(r'^(\d+)-(\d+)$', row['age'])
        if match:
            start_age, end_age = map(int, match.groups())
            average = (start_age + end_age) / 2
            row['age'] = round(average)
    return data
            
#2:
def changeDateFormat(data):
    for row in data:
        date_format = re.match(r'^(\d{2})\.(\d{2})\.(\d{4})$', row['date_onset_symptoms'])
        if date_format:
            day, month, year = map(int, date_format.groups()) #map function is used to appply int() on each of elements (day, month, year)
            row['date_onset_symptoms'] = f'{month:02d}.{day:02d}.{year}'

        date_format = re.match(r'^(\d{2})\.(\d{2})\.(\d{4})$', row['date_admission_hospital'])
        if date_format:
            day, month, year = map(int, date_format.groups())
            row['date_admission_hospital'] = f'{month:02d}.{day:02d}.{year}'

        date_format = re.match(r'^(\d{2})\.(\d{2})\.(\d{4})$', row['date_confirmation'])
        if date_format:
            day, month, year = map(int, date_format.groups())
            row['date_confirmation'] = f'{month:02d}.{day:02d}.{year}'
    return data

#3:
def fillLatLong(data):
    provincesLat = defaultdict(list)
    provincesLong = defaultdict(list) 
    avgLat = defaultdict(float)
    avgLong = defaultdict(float)
    for row in data:
        if(row['latitude'].lower() != 'nan'):
            provincesLat[row['province']].append(float(row['latitude']))
        if(row['longitude'].lower() != 'nan'):
            provincesLong[row['province']].append(float(row['longitude']))
    for province in provincesLat.keys():
        avgLat[province] = round((sum(provincesLat[province])/len(provincesLat[province])), 2)
        avgLong[province] = round((sum(provincesLong[province])/len(provincesLong[province])), 2)
    for row in data:
        if(row['latitude'].lower() == 'nan'):
            row['latitude'] = str(avgLat[row['province']])
        if(row['longitude'].lower() == 'nan'):
            row['longitude'] = str(avgLong[row['province']])
    return data
#4:
def fillCity(data):
    provinceToCities = defaultdict(list)
    mostCommonCities = defaultdict(str)
    for row in data:
        if(row['city'].lower() != 'nan'):
            provinceToCities[row['province']].append(row['city'])
    for province in provinceToCities.keys():
        l = (Counter(provinceToCities[province]).most_common(1))
        mostCommonCities[province] = l[0][0]
    for row in data: 
        if(row['city'].lower() == 'nan'):
            row['city'] = mostCommonCities[row['province']]
    return data

#5:
def fillSymptoms(data):
    provinceToSymptoms = defaultdict(list)
    mostCommonSymptoms = defaultdict(str)
    for row in data:
        if(row['symptoms'].lower() != 'nan'):
            provinceToSymptoms[row['province']].extend([x.strip() for x in row['symptoms'].split(';')])
    for province in provinceToSymptoms.keys():
        l = (Counter(provinceToSymptoms[province]).most_common(1))
        mostCommonSymptoms[province] = l[0][0]
    for row in data: 
        if(row['symptoms'].lower() == 'nan'):
            row['symptoms'] = mostCommonSymptoms[row['province']]
    return data

def writeCSV(data, filename):
    fieldnames = data[0].keys()
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

filename = 'covidTrain.csv'
with open(filename, 'r') as file: # Make a dictionary for each pokemon
    reader = csv.DictReader(file)
    data = list(reader)

#1
#processed_data_1 = rangeToAvg(data)
#output_filename = 'Age_processed_covidTrain.csv'
#writeCSV(processed_data_1, output_filename)

#2
#processed_data_2 = changeDateFormat(data)
#output_filename = 'Date_processed_covidTrain.csv'
#writeCSV(processed_data_2, output_filename)

#3
#processed_data_3 = fillLatLong(data)
#output_filename = 'LatLong_processed_covidTrain.csv'
#writeCSV(processed_data_3, output_filename)

#4
#processed_data_4 = fillCity(data)
#output_filename = 'City_processed_covidTrain.csv'
#writeCSV(processed_data_4, output_filename)
    
#5    
#processed_data_5 = fillSymptoms(data)
#output_filename = 'Symptoms_processed_covidTrain.csv'
#writeCSV(processed_data_5, output_filename)
    
#All
data = rangeToAvg(data)
data = changeDateFormat(data)
data = fillLatLong(data)
data = fillCity(data)
data = fillSymptoms(data)
output_file = 'covidResult.csv'
writeCSV(data, output_file)