

#PARAMETRES ____________________________________________________________

#chemin vers le csv a importer :
csvPath=r"S:\4- PASSERELLE\23- GSI\tests\1- exportGCFT.csv"
#nom de la table dans laquelle charger le csv
nomTable="suivi_wf_gcft"
#True pour supprimer les anciennes lignes, False pour ajouter au tableau
supprimerAnciennesLignes = True


#recuperation des couches_________________________________________________
#table comme vecteur
tableLayer=QgsMapLayerRegistry.instance().mapLayersByName(nomTable)[0]

#recuperation du csv en liste
print("Traitement du csv ... "+csvPath)
import csv
rawRows=[]
with open(csvPath) as file :
    csv_reader = csv.reader(file, delimiter=';')
    for line in csv_reader:
        rawRows.append(line)
print("TERMINE : "+str(len(rawRows)-1)+" lignes extraites")

#traitement des colonnes __________________________________________________
print("traitement des colonnes ...")
headers=rawRows.pop(0)
headersDict={}
for i, title in enumerate(headers):
    headersDict[title]=i

tableFields=tableLayer.fields()

commonFields=[]
for field in tableLayer.fields():
    if field.name() in headers:
        commonFields.append(field.name())
        
print("TERMINE : "+str(len(commonFields))+" colonnes en commun")

#copie colle des entites______________________________________________________
print("preparation des lignes a coller ...")
features = []
count=0
palierProgression=len(rawRows)/4
for csvLine in rawRows:
    resultFeat=QgsFeature()
    resultFeat.setFields(tableFields)
    #recup attributs dessin
    for fieldName in commonFields:
        resultFeat[fieldName]=csvLine[headersDict[fieldName]]
    
    features.append(resultFeat)
    count+=1
    #if count % palierProgression ==0:
    #    print(str(count)+" lignes preparees")

print("TERMINE : "+str(count)+" lignes preparees")

#demande de confirmation _____________________________________________________
"""avec les titres et le nombre de ligne"""


#suppression des entites _____________________________________________________
if supprimerAnciennesLignes == True :
    print("suppression des anciennes lignes ...")
    with edit(tableLayer):
        for feat in tableLayer.getFeatures():
            tableLayer.deleteFeature(feat.id())
    tableLayer.commitChanges()


#import des nouvelles entites _______________________________________________
print("import des nouvelles lignes ...")
tableLayer.startEditing()
tableLayer.dataProvider().addFeatures(features)
tableLayer.commitChanges()

print("TRAITEMENT TERMINE")

