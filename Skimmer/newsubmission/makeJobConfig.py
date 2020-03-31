#!/usr/bin/env python

import argparse
import os

#custom imports
import Dataset
import DASTools


def WriteJobConfigFile(filename, dataset, queue, multiplicity, maxtime, sepath, scratchpath="/scratch"): 
    with open("./lib/template.conf", "r") as template: 
        configfile = open(filename+".conf", 'w')
        workdir = "./"+filename+"_GCwork"
        datasettext=""
        for line in dataset: 
        	datasettext+=("\t"+line+"\n")

        filecontent = template.read()
        filecontent = filecontent.replace("$workdir$", workdir)
        filecontent = filecontent.replace("$queue$", queue)
        filecontent = filecontent.replace("$scratchpath$", scratchpath)
        filecontent = filecontent.replace("$maxtime$", str(maxtime))
        filecontent = filecontent.replace("$dataset$", datasettext)
        filecontent = filecontent.replace("$multiplicity$", str(multiplicity))
        filecontent = filecontent.replace("$sepath$", "srm://t3se01.psi.ch:8443/srm/managerv2?SFN=/pnfs/psi.ch/cms/trivcat/store/user/$USER/production/Wtagging")

        configfile.write(filecontent)
        configfile.close()
  	


if __name__ == "__main__":

   parser = argparse.ArgumentParser(description='GC: makeJobConfig') 

   parser.add_argument('descriptor', default = None, help="Which dataset to produce [mandatory]")
   parser.add_argument('-d','--dry', action = 'store_true', help = 'Run in dry mode (create but do not submit jobs)')
   parser.add_argument('-b','--batch', action = 'store_true', help = 'run in batch mode (no printout) ')
   parser.add_argument('-o', '--output', action = 'store', type=str, dest='outdir', default="catalogue", help = 'Where to store the config dataset files')
   parser.add_argument('-v', '--verbose', action='store_true', help = 'Give a lot of output (verbose)')
   parser.add_argument('-f', '--force', action='store_true', help="Force overwriting (the catalogue or job config file)")
   parser.add_argument('-m', '--multiplicity', action='store', type=int, default=10, help="Number of files per job") 

   args = parser.parse_args()  
 

   datasetfiles = []

   #args.descriptor = "TT" # choose in [TT, ST, VV, WJets, QCD, mc, data, all]

   for dataset in Dataset.getDataset(args.descriptor): 
        datasetfiles.append(DASTools.GenerateGCDatasetFiles(dataset, args.outdir))

   # print datasetfiles

   os.system(". ./makeEnv.sh")	# Droping the environment variables into a file for GC 


   WriteJobConfigFile(args.outdir, datasetfiles, "wn", 10, 8, "srm://t3se01.psi.ch:8443/srm/managerv2?SFN=/pnfs/psi.ch/cms/trivcat/store/user/$USER/production/Wtagging", "/scratch")



