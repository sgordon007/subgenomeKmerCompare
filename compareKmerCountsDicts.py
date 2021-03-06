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
kmercountPath = parseConfigFindPath('SortPath',configFile)
kmercountFiles = filter(None,str(subprocess.Popen(['ls', '%s' % kmercountPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()).split('\n'))


def kmercounttodict(kmercount2fname,kmercountPath):
    """Change kmercount2 into a dictionary object with keys being genes of species kmercount2, allows for ease of access of data"""
    inputFile = open(kmercountPath+kmercount2fname,'r')
    dictConverted = {}
    for line in inputFile:
        if line:
            lineList = line.split()
            """dictionary w/ key gene --> (chr,xi,xf)"""
            dictConverted[lineList[0]]=(int(lineList[1].strip('\n')))
            # print lineList[0] + lineList[1]
    inputFile.close()
    return dictConverted

dictOfGenes = {}
for file in kmercountFiles:
    # creates a dictionary that associates a species to its dictionary of the kmer : count key value pairs
    # kmercounttodict function is called to create the kmer : count key value pairs
    dictOfGenes[file.split('.')[0]] = kmercounttodict(file,kmercountPath)
    # what does this print, test
    # print file.split('.')[0]

# we now have two dictionaries (or more if we add more than two kmer count files to the kmercount_files path
# now compare the two dictionaries in both directions to find kmers that are high in kmer dict 1 and low in kmer dict 2 and vice versa


# this gets the dictionary name for the first kmer dict
dict1 = dictOfGenes[kmercountFiles[0].split('.')[0]]
dict2 = dictOfGenes[kmercountFiles[1].split('.')[0]]

# output kmers and counts for differential kmers
# output file names
outFileNames = []
for file in kmercountFiles:
    outFileNames.append("%s.higher.kmers.txt" % (file.split('.')[0]))

# create files for writing
for filename in outFileNames:
    open(filename, 'w').close()

# check dict 1 against dict 2
out1 = open(outFileNames[0], 'w')
# iterate through the keys of dict1 and identify kmers that are at least 10 fold higher in dict1
for key, value in dict1.iteritems():
    val1 = value
    val2 = dict2.get(key, 3)
    if (val1 / val2) > 30:
        # print the at least 10 fold higher kmers in dict1
        out1.write('%s\t%d\t%d\n' % (key, val1, val2))
out1.close()

# do same for other direction of query, # check dict 2 against dict 1
out2 = open(outFileNames[1], 'w')
for key, value in dict2.iteritems():
    val1 = value
    val2 = dict1.get(key, 3)
    if (val1 / val2) > 30:
        # print the at least 10 fold higher kmers in dict2
        out2.write('%s\t%d\t%d\n' % (key, val1, val2))
out2.close()

