import subprocess, shutil

# parse config file
configFile = open('kmerCountCompare.txt','r') #generate in integrated analysis


def parseConfigFindPath(stringFind,configFile):
    """findPath will find path of associated specified string"""
    for line in configFile:
        if stringFind in line: # if find string specified, return pathname/info
            configFile.seek(0)
            return line.split()[-1].strip('\n')

# system path to find allmaps installation files
path = parseConfigFindPath('systemPath',configFile)
sortPath = parseConfigFindPath('SortPath',configFile)
sortFiles = filter(None,str(subprocess.Popen(['ls', '%s' % sortPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()).split('\n'))


def kmercounttodict(sort2fname,sortPath):
    """Change sort2 into a dictionary object with keys being genes of species sort2, allows for ease of access of data"""
    inputFile = open(sortPath+sort2fname,'r')
    dictConverted = {}
    for line in inputFile:
        if line:
            lineList = line.split()
            """dictionary w/ key gene --> (chr,xi,xf)"""
            dictConverted[lineList[0]]=(int(lineList[1].strip('\n')))
    inputFile.close()
    return dictConverted

dictOfGenes = {}
for file in sortFiles:
    # create dictionary of species, each species entry has their own sort file converted to dictionary for ease access
    dictOfGenes[file.split('.')[0]] = kmercounttodict(file,sortPath)
    # what does this print, test
    print file.split('.')[0]



# geneCount = {}
# for i in range(len(unOutSyntenies)):
#     # find query and target species names from unout files
#     qspeciesName = unOutSyntenies[i][unOutSyntenies[i].find('.')+1:unOutSyntenies[i].find('-')]
#     tspeciesName = unOutSyntenies[i][unOutSyntenies[i].find('_')+1:unOutSyntenies[i].rfind('_')].strip('0.')
#     # initialize genecounts for each species if doesn't already exist. If exists, continue gene count
#     if qspeciesName not in geneCount.keys():
#         geneCount[qspeciesName]=0
#     if tspeciesName not in geneCount.keys():
#         geneCount[tspeciesName]=0
#
# # output query and target file objects
# outq = open(outFileNames[0], 'w')
# outt = open(outFileNames[1], 'w')
# for line in inputFile:
#     if line:
#         if '[' not in line and read == 1:  # Chr05N,3014546,Pavir.5NG471200.1,Chr05,1013018,Pahal.E01839.1	3:1	5	115	782	0.0	0.871794871794872
#             # (target species gene name, query species gene name)
#             genes = (line.split()[0].split(',')[-1], line.split()[0].split(',')[2])
#             # add to genecounts to establish mapping, will rename gene names to reflect gene count but still grab sequence information
#             geneCount[tspeciesName] += 1
#             geneCount[qspeciesName] += 1
#             # the genes found in unout have been renamed into "fakegenes", will still carry same sequence info
#             # (target species fakegene name, query species fakegene name)
#             fakegenes = (
#             '%s_%d' % (tspeciesName, geneCount[tspeciesName]), '%s_%d' % (qspeciesName, geneCount[qspeciesName]))
#             # write that fake gene has information of actual gene
#             outq.write('%s\t%s\t%s\t%s\t100\t+\n' % (dictOfGenes[qspeciesName][genes[1]] + (fakegenes[1],)))
#             outt.write('%s\t%s\t%s\t%s\t100\t+\n' % (dictOfGenes[tspeciesName][genes[0]] + (fakegenes[0],)))
#             # print qspeciesName,dictOfGenes[qspeciesName].has_key(genes[1]),tspeciesName,dictOfGenes[tspeciesName].has_key(genes[0])
#             # establish relationship between two syntenic genes through genemap file
#             outputFileGenemap.write('%s\t%s\t100\n' % fakegenes)
#         if '[' in line:
#             read = 0
#             # only take in genes that pass loci threshold
#             if int(line.split()[-6]) >= lociThreshold:
#                 read = 1

# outputFileGenemap.close()
# outq.close()
# outt.close()
#
# inputFile.close()

