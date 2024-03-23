import csv
from collections import defaultdict

def calcFireAbove40(data):
    fireCount = len([1 for x in data if x["type"] == "fire"])
    fireCountAbove40 = len([1 for x in data if x["type"] == "fire" and float(x['level']) >= 40])
    print(fireCount, fireCountAbove40) 
    if fireCount != 0:
        return round((fireCountAbove40/fireCount)*100) #returns percentage
    else:
        return 0
    
def weaknessType(data):
    typeDict = {}
    for row in data:
        if(row['type'].lower() != 'nan' and row['weakness'].lower() != 'nan'):
            if(row['weakness'] not in typeDict.keys()):
                typeDict[row['weakness']] = row['type']
    for row in data:
        if(row['type'].lower() == 'nan' and row['weakness'].lower() != 'nan'):
            row['type'] = typeDict[row['weakness']]
    return data

def missingValues(data):
    threshold = 40

    #High Level Average Stats:
    highLvlsAtk = [float(x['atk']) for x in data if float(x['level']) > 40 and x['atk'].lower() != 'nan']
    highLvlAtkAvg = sum(highLvlsAtk)/len(highLvlsAtk)
    highLvlsDef = [float(x['def']) for x in data if float(x['level']) > 40 and x['def'].lower() != 'nan']
    highLvlDefAvg = sum(highLvlsDef)/len(highLvlsDef)
    highLvlsHP = [float(x['hp']) for x in data if float(x['level']) > 40 and x['hp'].lower() != 'nan']
    highLvlHPAvg = sum(highLvlsHP)/len(highLvlsHP)
    highLvlAtkAvg = round(highLvlAtkAvg, 1)
    highLvlDefAvg = round(highLvlDefAvg, 1)
    highLvlHPAvg = round(highLvlHPAvg, 1)
    
    #Low Level Average Stats
    lowLvlsAtk = [float(x['atk']) for x in data if float(x['level']) <= 40 and x['atk'].lower() != 'nan']
    lowLvlAtkAvg = sum(lowLvlsAtk)/len(lowLvlsAtk)
    lowLvlsDef = [float(x['def']) for x in data if float(x['level']) <= 40 and x['def'].lower() != 'nan']
    lowLvlDefAvg = sum(lowLvlsDef)/len(lowLvlsDef)
    lowLvlsHP = [float(x['hp']) for x in data if float(x['level']) <= 40 and x['hp'].lower() != 'nan']
    lowLvlHPAvg = sum(lowLvlsHP)/len(lowLvlsHP)
    lowLvlAtkAvg = round(lowLvlAtkAvg, 1)
    lowLvlDefAvg = round(lowLvlDefAvg, 1)
    lowLvlHPAvg = round(lowLvlHPAvg, 1)
    
    for row in data:
        if float(row['level']) > 40:
            if(row['atk'].lower() == 'nan'):
                row['atk'] = str(highLvlAtkAvg)
            if(row['def'].lower() == 'nan'):
                row['def'] = str(highLvlDefAvg)
            if(row['hp'].lower() == 'nan'):
                row['hp'] = str(highLvlHPAvg) 
        else: 
            if(row['atk'].lower() == 'nan'):
                row['atk'] = str(lowLvlAtkAvg)
            if(row['def'].lower() == 'nan'):
                row['def'] = str(lowLvlDefAvg)
            if(row['hp'].lower() == 'nan'):
                row['hp'] = str(lowLvlHPAvg )
    return data

def personalityTypes(data):
    personalityTypeMap = defaultdict(list)
    for row in data:
        if(row['personality'] not in personalityTypeMap[row['type']]):
            personalityTypeMap[row['type']].append(row['personality'])
    for key in personalityTypeMap.keys():
        personalityTypeMap[key].sort()
    return personalityTypeMap

def avgStage3HP(data):
    stage3HP = [float(x['hp']) for x in data if float(x['stage']) == 3.0]
    avg = round((sum(stage3HP)/len(stage3HP)))
    return avg

filename = 'pokemonTrain.csv'
with open(filename, 'r') as file: # Make a dictionary for each pokemon
    reader = csv.DictReader(file)
    data = list(reader)
    #print(data) 

# Problem 1:
fireAbove40 = calcFireAbove40(data)
with open('pokemon1.txt', 'w') as outfile:
    outfile.write(f"Percentage of fire type Pokemons at or above level 40 = {fireAbove40}\n")


# Problem 2 and 3:
data = weaknessType(data)
data = missingValues(data)
output_file = 'pokemonResult.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)


filename = 'pokemonResult.csv'
with open(filename, 'r') as file: # Make a dictionary for each pokemon
    reader = csv.DictReader(file)
    data = list(reader)

# Problem 4:
typePersonalityMap = personalityTypes(data)
with open('pokemon4.txt', 'w') as outfile:
    outfile.write("Pokemon type to personality mapping:\n")
    for key in sorted(typePersonalityMap.keys()):
        outfile.write(f"\t{key}: {', '.join(typePersonalityMap[key])}\n")

# Problem 5:
avg = avgStage3HP(data)
with open('pokemon5.txt', 'w') as outfile:
    outfile.write(f"Average hit point for Pokemons of stage 3.0 = {avg}\n")