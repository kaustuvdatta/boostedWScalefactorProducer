#!/usr/bin/env python


DATASETPATH = "/eos/home-m/mhuwiler/data/Wtagging/Mergedefinition2017/"


class Dataset: 

    def __init__(self, year): 
        self.year = year

        self.directory = {}
        
        self.samples = {} 


        self.directory[2018] = "/eos/home-m/mhuwiler/data/Wtagging/Mergedefinition2017/"
  

        self.samples[2018] = {
          "Data":         ["SingleMuon-Run2018A.root", "SingleMuon-Run2018B.root", "SingleMuon-Run2018C.root", "SingleMuon-Run2018D.root"], 
          "tt":           ["TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8.root", "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"], 
          "ttpowheg":     ["TT_TuneCH3_13TeV-powheg-herwig7.root"],
          "ttamcatnlo":   ["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root"],
          "WJets":        ["WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8.root"], 
          "st":    ["ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8.root", "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8.root", "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8.root", "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8.root", "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8.root"], 
          "VV":           ["WW_TuneCP5_13TeV-pythia8.root", "WZ_TuneCP5_13TeV-pythia8.root", "ZZ_TuneCP5_13TeV-pythia8.root"], 
          "QCD":          ["QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8.root"] #"QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8.root", 

        }


        self.directory[2020] = "/eos/home-m/mhuwiler/data/Wtagging/lightweight/"

        self.samples[2020] = {
          "Data":   ["SingleMuon-Run2018A.root", "SingleMuon-Run2018B.root", "SingleMuon-Run2018C.root", "SingleMuon-Run2018D.root"], 
          "tt":     ["TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8.root", "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"], 
          "ttpowheg": ["TT_TuneCH3_13TeV-powheg-herwig7.root"],
          "ttamcatnlo":  ["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root"],
          "WJets":  ["WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8.root", "WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8.root"], 
          "st":  ["ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8.root", "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8.root", "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8.root", "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8.root", "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8.root"], 
          "VV":  ["WW_TuneCP5_13TeV-pythia8.root", "WZ_TuneCP5_13TeV-pythia8.root", "ZZ_TuneCP5_13TeV-pythia8.root"], 
          "QCD":          ["QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8.root"] #"QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8.root", 

        }

        self.directory[2017] = "/eos/home-m/mhuwiler/data/Wtagging/2017UL/"

        self.samples[2017] = {
          "Data":         ["SingleMuon_B_2017ULwithWeights.root", "SingleMuon_C_2017ULwithWeights.root", "SingleMuon_D_2017ULwithWeights.root", "SingleMuon_E_2017ULwithWeights.root", "SingleMuon_F_2017ULwithWeights.root"], 
          "tt":           ["TTToSemileptonic_powheg_pythia8_2017ULwithWeights.root", "TTTo2L2Nu_powheg_pythia8_2017ULwithWeights.root"], 
          #"ttpowheg":     ["TT_TuneCH3_13TeV-powheg-herwig7.root"],
          "ttamcatnlo":   ["TTJets_amcatnloFXFX-_pythia8_2017ULwithWeights.root"],
          "WJets":        ["WJetsToLNu_madgraphMLM_pythia8_2017ULwithWeights.root"], 
          "st":    ["ST_s-channel_amcatnlo_pythia8_2017ULwithWeights.root", "ST_t-channel_antitop_powheg_pythia8_2017ULwithWeights.root", "ST_t-channel_top_powheg_pythia8_2017ULwithWeights.root", "ST_tW_antitop_powheg_pythia8_2017ULwithWeights.root", "ST_tW_top_powheg_pythia8_2017ULwithWeights.root"], 
          "VV":           ["WW_TuneCP5_13TeV-pythia8.root", "WZ_TuneCP5_13TeV-pythia8.root", "ZZ_TuneCP5_13TeV-pythia8.root"], 
          "QCD":          ["QCD_Pt_170to300_pythia8_2017ULwithWeights.root", "QCD_Pt_300to470_pythia8_2017ULwithWeights.root", "QCD_Pt_470to600_pythia8_2017ULwithWeights.root", "QCD_Pt_600to800_pythia8_2017ULwithWeights.root", "QCD_Pt_800to1000_pythia8_2017ULwithWeights.root", "QCD_Pt_1000to1400_pythia8_2017ULwithWeights.root", "QCD_Pt_1400to1800_pythia8_2017ULwithWeights.root", "QCD_Pt_1800to2400_pythia8_2017ULwithWeights.root", "QCD_Pt_2400to3200_pythia8_2017ULwithWeights.root", "QCD_Pt_3200toInf_pythia8_2017ULwithWeights.root"], #"QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8.root", "QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8.root", 
          "bkg":          ["QCD_Pt_300to470_pythia8_2017ULwithWeights.root", "QCD_Pt_470to600_pythia8_2017ULwithWeights.root"] # Here we only keep the samples that are relevant for the pT cuts applied in the fakerate estimate


        }


    def getSample(self, sample): 
        return self.prependPath(self.samples[self.year][sample])

    def prependPath(self, collection): 
        return [self.directory[self.year]+x for x in collection]


