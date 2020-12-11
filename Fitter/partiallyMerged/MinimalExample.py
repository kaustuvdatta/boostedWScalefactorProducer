import ROOT
import os
import sys
import WtaggingFitter


debug = True
# Create the model
variable = ROOT.RooRealVar("variable", "variable", -5, 5)
tagger = ROOT.RooRealVar("tagger", "tagger", 0, 10)
 

a0 = ROOT.RooRealVar("a0", "a0", -3.5, -5,5)
a1 = ROOT.RooRealVar("a1", "a1", -1.5, -1,1)
sigma = ROOT.RooRealVar("sigma", "width of gaussian", 1.5)
 
fy = ROOT.RooFormulaVar("fy", "fy", "a0-a1*sqrt(10*abs(tagger))", ROOT.RooArgList(tagger,a0,a1))
 
modelgen = ROOT.RooGaussian("modelgen", "Gaussian with shifting mean", variable, fy, sigma)

# taken from https://root.cern.ch/doc/v608/rf309__ndimplot_8C_source.html

data = modelgen.generate(ROOT.RooArgSet(variable, tagger), 10000)

if debug: 
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
	histo = data.createHistogram(variable, tagger, 20, 20)
	histo.Draw()
	canvas.Draw() # works so far 

regions = ROOT.RooCategory("regions", "regions")
regions.defineType("HP")
regions.defineType("LP")

# Simple model
mu1 = ROOT.RooRealVar("mu1", "mu1", -5., 5.)
sigma1 = ROOT.RooRealVar("sigma1", "sigma1", 0., 2)
modelHP = ROOT.RooGaussian("modelHP", "Gaussian with shifting mean", variable, mu1, sigma1)
mu2 = ROOT.RooRealVar("mu2", "mu2", -5., 5.)
sigma2 = ROOT.RooRealVar("sigma2", "sigma2", 0., 2)
modelLP = ROOT.RooGaussian("modelLP", "Gaussian with shifting mean", variable, mu2, sigma2)
model = ROOT.RooSimultaneous("simultaneousMCmodel", "simultaneousMCmodel", regions)
model.addPdf(modelHP, "HP") # self.LoadPdf("HP:fullMC:model"), "HP"
model.addPdf(modelLP, "LP")


tagger.setRange("fitRange_HP", 0., 5.)
tagger.setRange("fitrange_LP", 5., 10)

# Clumsy way to generate two RooDataSets according to the ranges on tagger (split the initial one into the two categories)
fullMCHP = ROOT.RooDataSet(data)
fullMCHP = fullMCHP.reduce(ROOT.RooFit.CutRange("fitRange_HP"))
fullMCHP = fullMCHP.reduce(ROOT.RooArgSet(variable))
fullMCHP.Print()

fullMCLP = ROOT.RooDataSet(data)

fullMCLP = fullMCLP.reduce(ROOT.RooFit.CutRange("fitRange_LP"))
fullMCLP = fullMCLP.reduce(ROOT.RooArgSet(variable))
fullMCLP.Print()




	

sample = ROOT.RooDataSet("combinedMC", "combined MC dataset", ROOT.RooArgSet(variable), ROOT.RooFit.Index(regions), ROOT.RooFit.Import("HP", fullMCHP), ROOT.RooFit.Import("LP", fullMCLP))


model.fitTo(sample)


canvasHP = ROOT.TCanvas("canvasHP", "HP fit on MC", 800, 600)
plotHP = variable.frame()
sample.plotOn(plotHP, ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson), ROOT.RooFit.Cut("regions==regions::HP")) #Works 
model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample)) 
plotHP.Draw()
canvasHP.Draw()


#model.Print()

rep = ""
print "Do you want to quit the script (close all windows)?"
while not rep in [ 'yes']:
	rep = raw_input( "(type 'yes' or 'no'): " ).lower()
