#!/usr/bin/env python

import ROOT
import os
import sys
from WTopScalefactorProducer.Fitter.tdrstyle import *
from Dataset import Dataset
from Fitter import Fitter



WORKSPACENAME = "WTaggingFitter"



class WTaggingFitter(Fitter):  # class WTaggingFitter(Fitter)
	def __init__(self, options):
		# Loading custom Roofit PDFs 
		ROOT.gROOT.LoadMacro("PDFs/HWWLVJRooPdfs.cxx+")

		self.workspacename = WORKSPACENAME #Fixme 
		Fitter.__init__(self, options) # python 3 super().__init__(options)

		#TODO: add a mapping from Dataset name to RooDataset name (if needed, unless using RooRealVar.setRange())
		

		#dataset = self.LoadDataset("HP:tt")

		#print dataset

		self.fitvarname = options.massvar

		self.taggername = options.tagger

		self.weightname = options.weightvar

		possibleyears = [2018, 2020] #2017, 2018, 2020
		assert(options.year in possibleyears), "ERROR: Please specify a year (with option --year ) within the following: {}".format(possibleyears)

		# Defining the samples
		self.background = ["tt", "VV", "SingleTop", ] # TODO: define a class "sample" with a chain and cut on it 

		# TODO: fix directroy handling
		self.directory = {} 
		self.directory["fitMC"] = "plots/{}/fitMC/".format(options.year)
		self.directory["fitMClogs"] = "logs/{}/fitMC/".format(options.year)

		self.saveasformats = [".pdf", ".png"]

		# Creatring the output directories if they don't exist 
		for directory in self.directory.values(): 
			if not os.path.isdir(directory): 
				assert(not os.path.isfile(directory)), "ERROR: The path '{}' is a file, cannot create directory with such name!" 
				os.system("mkdir -p "+directory)

		# Defining the fit options to be used 
		#ROOT.Math:MinimizerOptions.SetDefaultTolerance()
		#self.fitoptions = roofitoptions

		self.constraintlist = []

		self.savemodel = False

		# --- Making the HP and LP ranges ---- 
		tagger = self.LoadVariable(options.tagger)
		tagger.setRange("fitRange_HP", 0., options.cutHP)
		tagger.setRange("fitrange_LP", options.cutHP, options.cutLP)

		massvar = self.LoadVariable(self.fitvarname)
		massvar.setRange("fitRange", 50., 130.) # The range over which to fit # TODO: set from options 
		#self.ImportToWorkspace(tagger, False, ROOT.RooFit.RecycleConflictNodes())
		#self.taggervar = tagger # Hack because cannot import variable with range
		#self.workspace.Print()
		tagger.getBinning("fitRange_HP").Print()

		self.debug = True


		self.MakeFitModel(self.savemodel)



	def FitMC(self, instancename = "FitMC", fitoptions = ""): 
		# TODO: might remove options and set massvar as attribute 
		print "Fitting MC... "

		#self.MakeFitModel(True)

		

		massvar = self.LoadVariable(self.fitvarname)

		#roofitoptions = ROOT.RooLinkedList()
		#roofitoptions.Add(ROOT.RooFit.Save(1)) # Produce the fit result
		#roofitoptions.Add(ROOT.RooFit.SumW2Error(ROOT.kTRUE)) # Interpret errors as errors on MC (see https://root.cern.ch/doc/master/classRooAbsPdf.html#af43c48c044f954b0e0e9d4fe38347551)
		#roofitoptions.Add(ROOT.RooFit.Extended(ROOT.kTRUE)) # Add extended likelihood term 
		#roofitoptions.Add(ROOT.RooFit.Minimizer("Minuit2")) # Use the Minuit2 minimizer (possible options: OldMinuit, Minuit (default), Minuit2, GSLMultiMin, GSLSimAn)
		##roofitoptions.Add(ROOT.RooFit.Verbose(ROOT.kFALSE)) # Disable verbosity 

		self.FitSampleStr("HP:tt:real:model", "ttrealW" , "fitRange_HP", massvar, "TTsignalHP", True, self.directory["fitMC"]) #self.FitSample({self.LoadPdf("HP:tt:real:model"):self.workspace.data("ttrealW").reduce(ROOT.RooFit.SelectVars(ROOT.RooArgSet(massvar, self.LoadVariable(self.taggername))), ROOT.RooFit.CutRange("fitRange_HP")).reduce(ROOT.RooFit.SelectVars(ROOT.RooArgSet(massvar)))}, "fitRange_HP", massvar, "TTsignal", True, self.directory["fitMC"]) # TODO: give "fitMC" and name as arguments and create everything within FitSample (plot, stream, snapshoot) # TODO: give "fitMC" and name as arguments and create everything within FitSample (plot, stream, snapshoot)


		self.FitSampleStr("HP:VV:model", "VV", "fitRange_HP", massvar, "VVbackgroundHP", True, self.directory["fitMC"])


		self.FitSampleStr("HP:st:model", "st", "fitRange_HP", massvar, "STbackgroundHP", True, self.directory["fitMC"])

		
		self.FitSampleStr("HP:tt:fake:model", "ttfakeW", "fitRange_HP",massvar, "TTfakeWHP", True, self.directory["fitMC"]) # maybe rename to FitSample1D


		self.FitSampleStr("HP:WJets:model", "WJets", "fitRange_HP",massvar, "WJetsbackgroundHP", True, self.directory["fitMC"])


		# Fitting the LP region 
		self.FitSampleStr("LP:tt:real:model", "ttrealW" , "fitRange_LP", massvar, "TTsignalLP", True, self.directory["fitMC"]) 


		self.FitSampleStr("LP:VV:model", "VV", "fitRange_LP", massvar, "VVbackgroundLP", True, self.directory["fitMC"])


		self.FitSampleStr("LP:st:model", "st", "fitRange_LP", massvar, "STbackgroundLP", True, self.directory["fitMC"])

		
		self.FitSampleStr("LP:tt:fake:model", "ttfakeW", "fitRange_LP",massvar, "TTfakeWLP", True, self.directory["fitMC"]) 


		self.FitSampleStr("LP:WJets:model", "WJets", "fitRange_LP",massvar, "WJetsbackgroundLP", True, self.directory["fitMC"])



		#fitstuff = {
		#	signalmodel:ttsample, 
		#	VVmodel:VVsample, 
		#	STmodel:STsample,
		#}

		#plot, results = self.FitSample(fitstuff, massvar) # Working 

		

		#canvas = ROOT.TCanvas("canvas", "Fit to tt realW", 800, 600)
		#plot.Draw()

		#canvas.Print("fittest.pdf")

	def FitMCtest(self, instancename="FitMCtest", fitoptions = ""): 

		massvar = self.LoadVariable(self.fitvarname)

		self.FitSampleStr("HP:tt:real:model", "ttrealW" , "fitRange_HP", massvar, "TTsignalHP", True, self.directory["fitMC"])


	def FitControlRegion(self, instancename = "FitControl"): 
		print "Fitting data and MC... "
		#self.FitMC(options)

		massvar = self.LoadVariable(self.fitvarname)

		fullMC = ROOT.RooDataSet(self.LoadDataset1D("WJets", massvar, "fitRange_HP"), "fullMC") # TODO: Fix this in case of binned fit 
		fullMC.append(self.LoadDataset1D("st", massvar, "fitRange_HP"))
		fullMC.append(self.LoadDataset1D("VV", massvar, "fitRange_HP"))
		fullMC.append(self.LoadDataset1D("ttfakeW", massvar, "fitRange_HP"))
		fullMC.append(self.LoadDataset1D("ttrealW", massvar, "fitRange_HP"))

		fullMC.Print()
 

		modelMC = self.LoadPdf("simultaneousMCmodel")


		self.LoadSnapshot("STbackgroundHP")

		self.FixAllParametersBase(self.LoadPdf("HP:st:model"), fullMC) # TODO: fix to only take massvar 

		self.LoadSnapshot("VVbackgroundHP")

		self.FixAllParametersBase(self.LoadPdf("HP:VV:model"), fullMC)

		self.LoadSnapshot("WJetsbackgroundHP")

		self.FixAllParametersBase(self.LoadPdf("HP:WJets:model"), fullMC)

		self.LoadSnapshot("STbackgroundLP")

		self.FixAllParametersBase(self.LoadPdf("LP:st:model"), fullMC) # TODO: fix to only take massvar 

		self.LoadSnapshot("VVbackgroundLP")

		self.FixAllParametersBase(self.LoadPdf("LP:VV:model"), fullMC)

		self.LoadSnapshot("WJetsbackgroundLP")

		self.FixAllParametersBase(self.LoadPdf("LP:WJets:model"), fullMC)

		self.LoadSnapshot("TTfakeWLP")

		self.LoadSnapshot("TTsignalLP")


		self.LoadSnapshot("TTfakeWHP")

		self.LoadSnapshot("TTsignalHP")

		#self.FixParameterBase("LP:tt:fake:number", modelMC, fullMC)

		#self.FixParameterBase("LP:MC:number", modelMC, fullMC)

		#self.FixParameterBase("HP:st:number", modelMC, fullMC)

		#self.FixParameterBase("HP:VV:number", modelMC, fullMC)

		#self.FixParameterBase("HP:WJets:number", modelMC, fullMC)


		tagger = self.LoadVariable(self.taggername)
		tagger.getBinning("fitRange_HP").Print()

		weight = self.LoadVariable(self.weightname)

		fullMC = ROOT.RooDataSet(self.LoadDataset("WJets", ROOT.RooArgSet(massvar, tagger)), "fullMC")
		fullMC.append(self.LoadDataset("st", ROOT.RooArgSet(massvar, tagger)))
		fullMC.append(self.LoadDataset("VV", ROOT.RooArgSet(massvar, tagger)))
		fullMC.append(self.LoadDataset("ttfakeW", ROOT.RooArgSet(massvar, tagger)))
		fullMC.append(self.LoadDataset("ttrealW", ROOT.RooArgSet(massvar, tagger)))

		# Make HP and LP datasets by restricting to tagger regions
		fullMCHP = ROOT.RooDataSet(fullMC)
		fullMC.Print()

		fullMCHP = fullMCHP.reduce(ROOT.RooFit.CutRange("fitRange_HP"))
		#fullMCHP = fullMCHP.reduce(ROOT.RooArgSet(massvar))
		fullMCHP.Print()

		fullMCLP = ROOT.RooDataSet(fullMC)

		fullMCLP = fullMCLP.reduce(ROOT.RooFit.CutRange("fitRange_LP"))
		#fullMCLP = fullMCLP.reduce(ROOT.RooArgSet(massvar))
		fullMCLP.Print()
		
		# Recombine them into a single dataset with two categories
		fullMCCombined = ROOT.RooDataSet("combinedMC", "combined MC dataset", ROOT.RooArgSet(massvar, weight), ROOT.RooFit.Index(self.workspace.cat("regions")), ROOT.RooFit.Import("HP", fullMCHP), ROOT.RooFit.Import("LP", fullMCLP), ROOT.RooFit.WeightVar(self.weightname))
		#fullMCCombined = fullMCCombined.reduce(ROOT.RooArgSet(massvar), ROOT.RooFit.Index(self.workspace.cat("regions")))
		print "Sample {} weighted: {}".format(fullMCCombined.GetName(), fullMCCombined.isWeighted())


		modelMC.Print()

		#MCfitresult, MCplot = self.FitSample({modelMC:fullMC}, "fitRange_HP", massvar, "FullMCFit", True, self.directory["fitMC"])
		combinedfitresult = self.CombinedFit(modelMC, fullMCCombined, "fitRange", massvar, "CombinedFit", True, self.directory["fitMC"])


		self.DrawFitResult(modelMC, fullMCCombined, massvar, instancename, self.directory["fitMC"])

		if (self.verbose or self.debug): 
			combinedfitresult.Print()

		modelMC.Print()

		#data = self.workspace.data("HP:data")
		print "Done fitting! "
		modelData = self.LoadPdf("HP:data:model")


	def TestFitControl(self, instancename = "TestFit"): 
		massvar = self.LoadVariable(self.fitvarname)
		tagger = self.LoadVariable(self.taggername)
		weight = self.LoadVariable(self.weightname)

		fullMC = ROOT.RooDataSet(self.LoadDataset("WJets", ROOT.RooArgSet(massvar, tagger)), "fullMC")
		fullMC.append(self.LoadDataset("st", ROOT.RooArgSet(massvar, tagger)))
		fullMC.append(self.LoadDataset("VV", ROOT.RooArgSet(massvar, tagger)))
		fullMC.append(self.LoadDataset("ttfakeW", ROOT.RooArgSet(massvar, tagger)))
		fullMC.append(self.LoadDataset("ttrealW", ROOT.RooArgSet(massvar, tagger)))

		# Make HP and LP datasets by restricting to tagger regions
		fullMCHP = ROOT.RooDataSet(fullMC)
		fullMC.Print()

		fullMCHP = fullMCHP.reduce(ROOT.RooFit.CutRange("fitRange_HP"))
		#fullMCHP = fullMCHP.reduce(ROOT.RooArgSet(massvar))
		fullMCHP.Print()

		fullMCLP = ROOT.RooDataSet(fullMC)

		fullMCLP = fullMCLP.reduce(ROOT.RooFit.CutRange("fitRange_LP"))
		#fullMCLP = fullMCLP.reduce(ROOT.RooArgSet(massvar))
		newWeight = ROOT.RooRealVar("newWeight", "newWeight", 1.)
		fullMCLP.addColumn(newWeight)
		fullMCLP.Print()
		
		# Recombine them into a single dataset with two categories
		fullMCCombined = ROOT.RooDataSet("combinedMC", "combined MC dataset", ROOT.RooArgSet(massvar, weight), ROOT.RooFit.Index(self.workspace.cat("regions")), ROOT.RooFit.Import("HP", fullMCHP), ROOT.RooFit.Import("LP", fullMCLP), ROOT.RooFit.WeightVar(self.weightname))
		#fullMCCombined = fullMCCombined.reduce(ROOT.RooArgSet(massvar), ROOT.RooFit.Index(self.workspace.cat("regions")))
		print "Sample {} weighted: {}".format(fullMCCombined.GetName(), fullMCCombined.isWeighted())



		modelMC = self.LoadPdf("simultaneousMCmodel")


		modelMC.Print()

		combinedfitresult = self.CombinedFit(modelMC, fullMCCombined, "fitRange", massvar, "CombinedFit", True, self.directory["fitMC"])

		self.DrawFitResult(modelMC, fullMCCombined, massvar, instancename, self.directory["fitMC"])

		if (self.verbose or self.debug): 
			combinedfitresult.Print()

		print "Done fitting! "
			



	def WeightDataset(self, dataset, variables, weight): 
		variables.add(self.LoadVariable(weight))
		weighteddataset = ROOT.RooDataSet("weighted_"+dataset.GetName(), "weighted_"+dataset.GetName(), dataset, variables, "1", weight)
		print "Sample {} weighted: {}".format(weighteddataset.GetName(), weighteddataset.isWeighted())
		return weighteddataset


	def FitSampleStr(self, modelname, samplename, fitrange, variable, instancename="", savesnapshot = False, directory="", fitoptions=None): 
		#sample = self.LoadDataset1D(samplename, variable, fitrange)
		weight = self.LoadVariable(self.weightname)
		sample = self.LoadDataset(samplename, ROOT.RooArgSet(variable, weight))
		sample = self.WeightDataset(sample, ROOT.RooArgSet(variable), self.weightname)
		print "Sample {} weighted: {}".format(sample.GetName(), sample.isWeighted())
		model = self.LoadPdf(modelname)
		return self.FitSample({model:sample}, fitrange, variable, instancename, savesnapshot, directory, fitoptions)

	def FitSample(self, samplelist, fitrange, variable, instancename="", savesnapshot=False, directory="", fitoptions=None): 
		if (fitoptions==None): # TODO: fix! 
			if hasattr(self, "fitoptions"): 
				fitoptions = self.fitoptions
			else: 
				fitoptions = ROOT.RooLinkedList()

		print fitoptions

		params = ROOT.RooArgSet()

		plot = variable.frame()

		fitresult = []
		for model, dataset in samplelist.items():
			result = model.fitTo(dataset, ROOT.RooFit.Range(fitrange), ROOT.RooFit.SplitRange(), ROOT.RooFit.Save(1), ROOT.RooFit.SumW2Error(ROOT.kTRUE), ROOT.RooFit.Extended(ROOT.kTRUE), ROOT.RooFit.Minimizer("Minuit2")) 
			fitresult.append(result)
			dataset.plotOn(plot, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
			model.plotOn(plot)

			if (savesnapshot): 
				params.add(model.getParameters(dataset)) # TODO: put here variable

			if (self.verbose): 
				result.Print()
			

		if not (directory == ""):
			canvas = ROOT.TCanvas("canvas", "Fit", 800, 600)
			plot.Draw()

			for savingformat in self.saveasformats: 
				canvas.Print(directory+instancename+savingformat)

		if (savesnapshot): 
			self.SaveSnapshotParams(params, instancename)

		return plot, fitresult

	def CombinedFit(self, model, sample, fitrange, variable, instancename="", savesnapshot=False, directory=""): 
		model.Print()
		sample.Print()
		variable.Print()
		self.workspace.Print()
		regions = self.workspace.cat("regions")
		
		fitresult = model.fitTo(sample, ROOT.RooFit.Range(fitrange), ROOT.RooFit.SplitRange(), ROOT.RooFit.Save(1), ROOT.RooFit.SumW2Error(ROOT.kTRUE), ROOT.RooFit.Extended(ROOT.kTRUE), ROOT.RooFit.Minimizer("Minuit2"))

		# HP plot
		"""
		canvasHP = ROOT.TCanvas("canvasHP", "HP fit on MC", 800, 600)
		plotHP = variable.frame()
		sample.plotOn(plotHP, ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson), ROOT.RooFit.Cut("regions==regions::HP"), rt.RooFit.XErrorSize(0)) #Works 
		model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:fullMC:model")) 
		model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:tt:fake:shape,HP:VV:shape,HP:st:shape,HP:WJets:shape"), ROOT.RooFit.LineStyle(rt.kDashed)) 
		if (self.debug): 
			model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:tt:real:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed)) 
			model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:tt:fake:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+1)) 
			model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:VV:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+2)) 
			model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:st:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+3)) 
			model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:WJets:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+4)) 
		plotHP.Draw()
		canvasHP.Draw()

		# LP plot
		canvasLP = ROOT.TCanvas("canvasLP", "LP fit on MC", 800, 600)
		plotLP = variable.frame(ROOT.RooFit.Title("LP"))
		sample.plotOn(plotLP, ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson), ROOT.RooFit.Cut("regions==regions::LP"), rt.RooFit.XErrorSize(0))
		model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(regions), sample), ROOT.RooFit.Components("LP:fullMC:model")) # model.plotOn(plotLP, ROOT.RooFit.Slice(regions, "LP"), ROOT.RooFit.ProjWData(regions, sample))
		#model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(regions), sample), ROOT.RooFit.Components("LP:tt:fake:shape"))
		model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:tt:fake:shape,LP:VV:shape,LP:st:shape,LP:WJets:shape"), ROOT.RooFit.LineStyle(rt.kDashed)) 
		if (self.debug): 
			model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:tt:real:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed)) 
			model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:tt:fake:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+1)) 
			model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:VV:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+2)) 
			model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:st:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+3)) 
			model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:WJets:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+4)) 
		plotLP.Draw()
		canvasLP.Draw()

		for savingformat in self.saveasformats: 
			canvasHP.Print(directory+instancename+"HP"+savingformat)
			canvasLP.Print(directory+instancename+"LP"+savingformat)

		if (savesnapshot): 
			self.SaveSnapshotParams(model.getParameters(sample), instancename)
		"""

		return fitresult


	def DrawFitResult(self, model, sample, variable, instancename="", directory=""): 
		# Making the plots
		canvasHP = ROOT.TCanvas("canvasHP", "HP fit on MC", 800, 600)
		plotHP = variable.frame()
		sample.Print()
		sample = sample.reduce(ROOT.RooArgSet(variable, self.workspace.cat("regions")))
		sample.Print()
		#self.LoadPdf("HP:st:model").plotOn(plotHP, ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(434))
		#self.LoadPdf("HP:WJets:model").plotOn(plotHP, ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(633))
		#self.LoadSnapshot("TTfakeWHP")
		#self.LoadPdf("HP:tt:fake:model").plotOn(plotHP, ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(415))
		#self.LoadSnapshot("TTrealWHP")
		#self.LoadPdf("HP:tt:real:model").plotOn(plotHP, ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(414))
		#self.LoadSnapshot("CombinedFit")
		# Plot the MC components 
		print "Drawing HP"
		sample.plotOn(plotHP, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.Cut("regions==regions::HP"), ROOT.RooFit.XErrorSize(0)) #Works 
		regions = self.workspace.cat("regions")
		weight = self.LoadVariable(self.weightname)
		variables = ROOT.RooArgSet(regions, variable, weight)
		self.LoadSnapshot("TTfakeWHP")
		self.LoadSnapshot("TTrealWHP")
		model.plotOn(plotHP, ROOT.RooFit.ProjWData(variables, sample), ROOT.RooFit.Cut("regions==regions::HP"), ROOT.RooFit.Components("HP:tt:real:shape,HP:tt:fake:shape,HP:VV:shape,HP:st:shape,HP:WJets:shape"), ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(414)) 
		model.plotOn(plotHP, ROOT.RooFit.ProjWData(variables, sample), ROOT.RooFit.Cut("regions==regions::HP"), ROOT.RooFit.Components("HP:tt:fake:shape,HP:VV:shape,HP:st:shape,HP:WJets:shape"), ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(415)) 
		model.plotOn(plotHP, ROOT.RooFit.ProjWData(variables, sample), ROOT.RooFit.Cut("regions==regions::HP"), ROOT.RooFit.Components("HP:VV:shape,HP:st:shape,HP:WJets:shape"), ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(434)) 
		model.plotOn(plotHP, ROOT.RooFit.ProjWData(variables, sample), ROOT.RooFit.Cut("regions==regions::HP"), ROOT.RooFit.Components("HP:VV:shape,HP:WJets:shape"), ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(633)) 
		sample.plotOn(plotHP, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.Cut("regions==regions::HP"), ROOT.RooFit.XErrorSize(0)) #Works 
		self.LoadSnapshot("CombinedFit")
		model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:fullMC:model")) 
		model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:tt:fake:shape,HP:VV:shape,HP:st:shape,HP:WJets:shape"), ROOT.RooFit.LineStyle(ROOT.kDashed)) 
		

		if (self.debug): 
			model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:tt:real:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed)) 
			model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:tt:fake:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+1)) 
			model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:VV:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+2)) 
			model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:st:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+3)) 
			model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("HP:WJets:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+4)) 
		plotHP.Draw()
		canvasHP.Draw()

		params = model.getParameters(ROOT.RooArgSet(variable))

		# LP plot
		canvasLP = ROOT.TCanvas("canvasLP", "LP fit on MC", 800, 600)
		plotLP = variable.frame(ROOT.RooFit.Title("LP"))
		sample.plotOn(plotLP, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.Cut("regions==regions::LP"), ROOT.RooFit.XErrorSize(0))
		model.plotOn(plotHP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(regions), sample), ROOT.RooFit.Cut("regions==regions::LP"), ROOT.RooFit.Components("LP:tt:real:shape,LP:tt:fake:shape,LP:VV:shape,LP:st:shape,LP:WJets:shape"), ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(414)) 
		model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(regions), sample), ROOT.RooFit.Cut("regions==regions::LP"), ROOT.RooFit.Components("LP:tt:fake:shape,LP:VV:shape,LP:st:shape,LP:WJets:shape"), ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(415)) 
		model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(regions), sample), ROOT.RooFit.Cut("regions==regions::LP"), ROOT.RooFit.Components("LP:VV:shape,LP:st:shape,LP:WJets:shape"), ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(434)) 
		model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(regions), sample), ROOT.RooFit.Cut("regions==regions::LP"), ROOT.RooFit.Components("LP:VV:shape,LP:WJets:shape"), ROOT.RooFit.DrawOption("F"), ROOT.RooFit.FillColor(633)) 
		sample.plotOn(plotLP, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.Cut("regions==regions::LP"), ROOT.RooFit.XErrorSize(0))
		#model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(regions), sample), ROOT.RooFit.Components("LP:fullMC:model")) # model.plotOn(plotLP, ROOT.RooFit.Slice(regions, "LP"), ROOT.RooFit.ProjWData(regions, sample))
		#model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(regions), sample), ROOT.RooFit.Components("LP:tt:fake:shape"))
		model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:tt:fake:shape,LP:VV:shape,LP:st:shape,LP:WJets:shape"), ROOT.RooFit.LineStyle(ROOT.kDashed)) 
		if (self.debug): 
			model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:tt:real:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed)) 
			model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:tt:fake:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+1)) 
			model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:VV:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+2)) 
			model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:st:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+3)) 
			model.plotOn(plotLP, ROOT.RooFit.ProjWData(ROOT.RooArgSet(variable), sample), ROOT.RooFit.Components("LP:WJets:shape"), ROOT.RooFit.LineStyle(rt.kDashed), ROOT.RooFit.LineColor(ROOT.kRed+4)) 
		plotLP.Draw()
		canvasLP.Draw()

		if (self.verbose or self.debug): 
			params.Print()
		params.printLatex(ROOT.RooFit.Format("Format", ROOT.RooFit.AutoPrecision(5), ROOT.RooFit.VerbatimName(), ROOT.RooFit.OutputFile(directory+instancename+"modelParams.tex")))

		for savingformat in self.saveasformats: 
			canvasHP.Print(directory+instancename+"HP"+savingformat)
			canvasLP.Print(directory+instancename+"LP"+savingformat)


	def TestFit(self): 
		self.MakeFitModel(True)

		variable = self.workspace.var(self.fitvarname)

		dataset = self.LoadDataset1D("ttrealW", variable)
		dataset.Print()


		model = self.workspace.pdf("HP:tt:real:model")
		#ttrealWmean   = ROOT.RooRealVar("HP:tt:mean", "HP:tt:mean", 89., 80., 95.) 
		#ttrealWsigma  = ROOT.RooRealVar("HP:tt:sigma", "HP:tt:sigma", 8., 2.5, 50.)
		#ttrealWalpha1  = ROOT.RooRealVar("HP:tt:alpha1", "HP:tt:alpha1", 0.5, 0.1, 10.) 
		#ttrealWalpha2  = ROOT.RooRealVar("HP:tt:alpha2", "HP:tt:alpha2", 1.0, 0.1, 10.) 
		#ttrealWsign1   = ROOT.RooRealVar("HP:tt:sign1", "HP:tt:sign1", 0.2, 0.01, 5.)
		#ttrealWsign2   = ROOT.RooRealVar("HP:tt:sign2", "HP:tt:sign2", 0.2, 0.01, 10.) 
		#ttrealWshape = ROOT.RooDoubleCrystalBall("HP:tt:real:shape","HP:tt:real:shape", variable, ttrealWmean, ttrealWsigma, ttrealWalpha1, ttrealWsign1, ttrealWalpha2, ttrealWsign2)
		#ttrealWnumber = ROOT.RooRealVar("HP:tt:real:number", "HP:tt:real:number", 500., 100., 1e20)
		#model = ROOT.RooExtendPdf("HP:tt:real:model", "HP:tt:real:model", ttrealWshape, ttrealWnumber)

		#mean = ROOT.RooRealVar("HP:tt:mean", "HP:tt:mean", 89., 50., 130.) 
		#sigma = ROOT.RooRealVar("HP:tt:sigma", "HP:tt:sigma", 8., 2.5, 100.)
		#shape = ROOT.RooGaussian("HP:tt:Gaussian", "HP:tt:Gaussian", variable, mean, sigma)

		#model = shape 

		snapshot = self.workspace.getSnapshot("ttinitial")
		params = model.getParameters(ROOT.RooArgSet(variable))
		#params = snapshot

		roofitoptions = ROOT.RooLinkedList()
		roofitoptions.Add(ROOT.RooFit.Save(1)) # Produce the fit result
		roofitoptions.Add(ROOT.RooFit.SumW2Error(ROOT.kTRUE)) # Interpret errors as errors on MC (see https://root.cern.ch/doc/master/classRooAbsPdf.html#af43c48c044f954b0e0e9d4fe38347551)
		roofitoptions.Add(ROOT.RooFit.Extended(ROOT.kTRUE)) # Add extended likelihood term 
		roofitoptions.Add(ROOT.RooFit.Minimizer("Minuit2")) # Use the Minuit2 minimizer (possible options: OldMinuit, Minuit (default), Minuit2, GSLMultiMin, GSLSimAn)


		plot = variable.frame()
		result = model.fitTo(dataset, ROOT.RooFit.Save(1), ROOT.RooFit.SumW2Error(ROOT.kTRUE), ROOT.RooFit.Extended(ROOT.kTRUE), ROOT.RooFit.Minimizer("Minuit2")) 
		result.Print()
		dataset.plotOn(plot, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
		model.plotOn(plot)
		canvas = ROOT.TCanvas("canvas", "Fit", 800, 600)
		plot.Draw()
		canvas.Update()

		savename = "testfit.pdf"
		print "Do you want to save the plot as '{}' ?".format(savename)
		if(self.PromptYesNo(True)): 

			canvas.Print(savename)

		self.workspace.saveSnapshot(model.GetName()+"fitMC", model.getParameters(ROOT.RooArgSet(variable)), ROOT.kTRUE)

	def TestFitSecond(self): 
		print "Fitting data and MC... "
		#self.FitMC(options)

		massvar = self.LoadVariable(self.fitvarname)

		fullMC = ROOT.RooDataSet(self.LoadDataset1D("WJets", massvar), "fullMC")
		fullMC.append(self.LoadDataset1D("st", massvar))
		fullMC.append(self.LoadDataset1D("VV", massvar))
		fullMC.append(self.LoadDataset1D("ttfakeW", massvar))
		fullMC.append(self.LoadDataset1D("ttrealW", massvar))

		fullMC.Print()


		modelMC = self.LoadPdf("HP:fullMC:model")

		modelWJets = modelMC.pdfList().find("HP:WJets:model") 

		print "Parameters:", modelMC.getParameters(fullMC).find("HP:WJets:offset") # works! 

		self.AddConstraintBase(modelMC.getParameters(fullMC).find("HP:WJets:offset"), 61., 10.)

		self.FixAllParametersBase(self.LoadPdf("HP:fullMC:model").pdfList().find("HP:WJets:shape"), fullMC)

		self.FixParameterBase(self.LoadPdf("HP:fullMC:model").pdfList().find("HP:st:shape"), fullMC, "HP:st:mean")

		STshape = self.GetComponent(self.LoadPdf("HP:fullMC:model"), "HP:st:shape")

		self.FixParameterBase(self.LoadPdf("HP:fullMC:model"), fullMC, "HP:st:sigma") # also works 

		variable = self.LoadVariable("SelectedJet_tau21")

		self.FixAllParameters("HP:tt:fake:model", "ttfakeW", "SelectedJet_tau21")

		self.FixAllParameters("HP:tt:fake:model", "ttfakeW", ["SelectedJet_tau21"])

		self.FixAllParameters("HP:tt:fake:model", "ttfakeW", self.LoadVariable("HP:tt:fake:coefficient"))

		self.FixAllParameters("HP:tt:fake:model", "ttfakeW", ROOT.RooArgSet(self.LoadVariable("HP:tt:fake:coefficient"), self.LoadVariable("HP:tt:fake:width")))

		self.AddConstraint("HP:WJets:width", 61., 10.)

		self.FixParameter("HP:tt:fake:model", "ttfakeW", "SelectedJet_tau21", "HP:tt:fake:offset")

		# Some further test
		self.AddConstraint("HP:tt:mean", 85., 10.)

		value = self.GetCurrentValue("HP:tt:mean")

		print value

		self.SetValue("HP:tt:mean", 93.)

		newvalue = self.GetCurrentValue("HP:tt:mean")

		print newvalue

		self.AddConstraint("HP:tt:mean", self.GetCurrentValue("HP:tt:mean"), 10.)

		self.LoadSnapshot("FitTT")


		value = self.GetCurrentValue("HP:tt:mean")

		print value

		self.FitSampleStr("HP:tt:real:model", "ttrealW", massvar, "SignalHP", True, self.directory["fitMC"])

		value = self.GetCurrentValue("HP:tt:mean")

		print value

		self.SetValue("HP:tt:mean", 89.)

		value = self.GetCurrentValue("HP:tt:mean")

		print value

		self.LoadSnapshot("SignalHP")

		value = self.GetCurrentValue("HP:tt:mean")

		print value






		modelMC.Print()

		MCfitresult, MCplot = self.FitSample({modelMC:fullMC}, massvar, "FullMCFit", True, self.directory["fitMC"])

		#data = self.workspace.data("HP:data")
		modelData = self.LoadPdf("HP:data:model")



	def MakeFitModel(self, saveworkspace=False): 
		print "Making fit model"

		fitvariable = self.workspace.var(self.fitvarname)
		#self.workspace.factory("DoubleCrystalBall::HP:tt:SignalModel({}, signalMean1[80., 100.], signalMean1[-10., 10.], signalSigma[0., 50.], signalSigma[0., 50.], sign1[0.01, 5.], sign1[0.01, 10.]".format(self.fitvarname)) # TODO: check how we can use the factory syntax with custom Pdfs. 

		# --- Defining the categories ---- 
		regions = ROOT.RooCategory("regions", "regions")
		regions.defineType("HP")
		regions.defineType("LP")

		# --- HP model ----

		# Signal model in the HP category 
		ttrealWmean   = ROOT.RooRealVar("HP:tt:mean", "HP:tt:mean", 89., 80., 95.) 
		ttrealWsigma  = ROOT.RooRealVar("HP:tt:sigma", "HP:tt:sigma", 8., 2.5, 50.)
		ttrealWalpha1  = ROOT.RooRealVar("HP:tt:alpha1", "HP:tt:alpha1", 0.5, 0.1, 10.) 
		ttrealWalpha2  = ROOT.RooRealVar("HP:tt:alpha2", "HP:tt:alpha2", 1.0, 0.1, 10.) 
		ttrealWsign1   = ROOT.RooRealVar("HP:tt:sign1", "HP:tt:sign1", 0.2, 0.01, 5.)
		ttrealWsign2   = ROOT.RooRealVar("HP:tt:sign2", "HP:tt:sign2", 0.2, 0.01, 10.) 
		ttrealWshape = ROOT.RooDoubleCrystalBall("HP:tt:real:shape","HP:tt:real:shape", fitvariable, ttrealWmean, ttrealWsigma, ttrealWalpha1, ttrealWsign1, ttrealWalpha2, ttrealWsign2)
		ttrealWnumber = ROOT.RooRealVar("HP:tt:real:number", "HP:tt:real:number",1e11, 500., 1e20)
		ttrealWmodel = ROOT.RooExtendPdf("HP:tt:real:model", "HP:tt:real:model", ttrealWshape, ttrealWnumber)

		#getattr(self.workspace, "import")(signalModel)
		self.ImportToWorkspace(ttrealWmodel, saveworkspace)

		#self.workspace.saveSnapshot("ttinitial", ttrealWmodel.getParameters(ROOT.RooArgSet(fitvariable)), ROOT.kTRUE)
		#params = signalModel.getParameters(fitvariable)
		#self.workspace.defineSet("signalParams", params)
		#self.workspace.saveSnapshot("buildmodel", params, ROOT.kTRUE)

		# Background unmerged tt model
		ttfakeWoffset = ROOT.RooRealVar("HP:tt:fake:offset" ,"HP:tt:fake:offset", 80, 10, 200) # 90, 10, 200
		ttfakeWwidth  = ROOT.RooRealVar("HP:tt:fake:width" ,"HP:tt:fake:width", 40, 25, 300) # 40, 25, 100
		ttfakeWcoefficient  = ROOT.RooRealVar("HP:tt:fake:coefficient" ,"HP:tt:fake:coefficient", -0.03, -1., -0.0001) # -0.04, -1, 0.
		ttfakeWshape     = ROOT.RooErfExpPdf("HP:tt:fake:shape", "HP:tt:fake:shape" ,fitvariable, ttfakeWcoefficient, ttfakeWoffset, ttfakeWwidth)
		ttfakeWnumber = ROOT.RooRealVar("HP:tt:fake:number", "HP:tt:fake:number", 1e11, 1e5, 1e20)
		ttfakeWmodel = ROOT.RooExtendPdf("HP:tt:fake:model", "HP:tt:fake:model", ttfakeWshape, ttfakeWnumber)
		
		self.ImportToWorkspace(ttfakeWmodel)

		# Background VV model
		VValpha       = ROOT.RooRealVar("HP:VV:alpha","HP:VV:alpha",-0.01 ,-1., 0.)
		gaus_means  = 8.2653e+01 # Constraining the gaussian part to the mass of the W (well actually 80)
		gaussigmas   = 7.
		VVmean  = ROOT.RooRealVar("HP:VV:mean", "HP:VV:mean", gaus_means, gaus_means*.8, gaus_means*1.2) 
		VVsigma = ROOT.RooRealVar("HP:VV:sigma", "HP:VV:sigma", gaussigmas, gaussigmas*.5, gaussigmas*1.5)
		VVfactor        = ROOT.RooRealVar("HP:VV:factor", "GP:VV:factor", 0.7, 0., 1.)
		VVExp = ROOT.RooExponential("HP:VV:Exponential", "HP:VV:exponential", fitvariable, VValpha)
		VVGauss = ROOT.RooGaussian("HP:VV:Gaussian", "HP:VV:gaussian", fitvariable ,VVmean, VVsigma)
		VVshape = ROOT.RooAddPdf("HP:VV:shape","HP:VV:shape", ROOT.RooArgList(VVExp, VVGauss), ROOT.RooArgList(VVfactor))
		VVnumber = ROOT.RooRealVar("HP:VV:number", "HP:VV:number", 1e10, 500., 1e15)
		VVmodel = ROOT.RooExtendPdf("HP:VV:model", "HP:VV:model", VVshape, VVnumber)
		
		self.ImportToWorkspace(VVmodel)

		# Background single top model
		STcoeff = ROOT.RooRealVar("HP:st:coefficient", "HP:st:coefficient", -0.04, -1., 1.)
		STwidth = ROOT.RooRealVar("HP:st:width","HP:st:width", 30., 0., 400.)
		SToffset = ROOT.RooRealVar("HP:st:offset", "HP:st:offset", 60., 50., 100.)
		STmean = ROOT.RooRealVar("HP:st:mean", "HP:st:mean", gaus_means, gaus_means*.8, gaus_means*1.2)
		STsigma = ROOT.RooRealVar("HP:st:sigma", "HP:st:sigma", gaussigmas, gaussigmas*.5, gaussigmas*1.5)
		STErfExp = ROOT.RooErfExpPdf("HP:st:ErfExp", "HP:st:ErfExp", fitvariable, STcoeff, SToffset, STwidth)
		STGauss = ROOT.RooGaussian ("HP:st:Gaussian" ,"HP:st:Gaussian" , fitvariable, STmean, STsigma)
		STfactor = ROOT.RooRealVar("HP:st:factor", "HP:st:factor", 0.3, 0.0, 0.99)
		STshape = ROOT.RooAddPdf("HP:st:shape", "HP:st:shape", STErfExp, STGauss, STfactor)
		STnumber = ROOT.RooRealVar("HP:st:number", "HP:st:number", 1e11, 500., 1e15)
		STmodel = ROOT.RooExtendPdf("HP:st:model", "HP:st:model", STshape, STnumber)

		self.ImportToWorkspace(STmodel)

		# Backgound W+Jets model
		WJetscoeff  = ROOT.RooRealVar("HP:WJets:coefficient", "HP:WJets:coefficient", -0.026, -0.05, 0.01)
		WJetsoffset = ROOT.RooRealVar("HP:WJets:offset", "HP:WJets:offset" ,80. ,0., 100)
		WJetswidth  = ROOT.RooRealVar("HP:WJets:width", "HP:WJets:width", 30., 1., 100.)
		WJetsshape  = ROOT.RooErfExpPdf("HP:WJets:shape", "HP:WJets:shape", fitvariable, WJetscoeff, WJetsoffset, WJetswidth)
		WJetsnumber = ROOT.RooRealVar("HP:WJets:number", "HP:WJets:number", 1e11, 500., 1e20)
		WJetsmodel = ROOT.RooExtendPdf("HP:WJets:model", "HP:WJets:model", WJetsshape, WJetsnumber)
		
		self.ImportToWorkspace(WJetsmodel, saveworkspace)

		 
		self.workspace.saveSnapshot("buildmodel", ROOT.RooArgSet(STcoeff, STwidth, SToffset, STmean, STsigma, STfactor), ROOT.kTRUE) # works! 
			#self.workspace.saveSnapshot("buildmodel", VVmodel.getParameters(ROOT.RooArgSet(fitvariable)), ROOT.kTRUE) # works too - recommended! 

		# Full background model (MC)
		fullbackgroundMCnumber = ROOT.RooRealVar("HP:background:MC:number", "HP:background:MC:number", 1., 1e15)
		fullbackgroundMCmodel = ROOT.RooExtendPdf("HP:background:MC:model", "HP:background:MC:model", ttfakeWshape, fullbackgroundMCnumber)
		#self.ImportToWorkspace(fullbackgroundMCmodel)

		# Full signal model (MC)
		fullsignalMCnumber = ROOT.RooRealVar("HP:signal:MC:number", "HP:signal:MC:number", 1., 1e15)
		fullsignalMCmodel = ROOT.RooExtendPdf("HP:signal:MC:model", "HP:signal:MC:model", ttrealWshape, fullsignalMCnumber)

		mcTTnumber = ROOT.RooRealVar("HP:MC:number", "HP:MC:number", 1e10, 500., 1e20)

		fullMCmodelHP = ROOT.RooAddPdf("HP:fullMC:model", "HP:fullMC:model", ROOT.RooArgList(ttrealWshape, ttfakeWshape, VVshape, STshape, WJetsshape), ROOT.RooArgList(ttrealWnumber, ttfakeWnumber, VVnumber, STnumber, WJetsnumber)) # TODO: check if want to add models instead of shapes

		self.ImportToWorkspace(fullMCmodelHP, saveworkspace, ROOT.RooFit.RecycleConflictNodes())

		print fullMCmodelHP


		# Full background model in for data
		fullbackgrounddatanumber = ROOT.RooRealVar("HP:background:data:number", "HP:background:data:number", 1e10, 500., 1e15)
		fullbackgrounddatamodel = ROOT.RooExtendPdf("HP:background:data:model", "HP:background:data:model", ttrealWshape, fullbackgrounddatanumber)
		#if (saveworkspace): 
			#self.ImportToWorkspace(fullbackgrounddatamodel)

		# Full signal model for data
		fullsignaldatanumber = ROOT.RooRealVar("HP:signal:data:number", "HP:signal:data:number", 1e10, 500., 1e15)
		fullsignaldatamodel = ROOT.RooExtendPdf("HP:signal:data:model", "HP:signal:data:model", ttrealWshape, fullsignaldatanumber)

		fulldatamodel = ROOT.RooAddPdf("HP:data:model", "HP:data:model", ROOT.RooArgList(fullsignaldatamodel, fullbackgrounddatamodel))

		self.ImportToWorkspace(fulldatamodel, saveworkspace, ROOT.RooFit.RecycleConflictNodes())

		#self.workspace.saveSnapshot("buildmodel", ROOT.RooArgSet(fullMCmodelHP.getParameters(ROOT.RooArgSet(fitvariable)), fulldatamodel.getParameters(ROOT.RooArgSet(fitvariable))), ROOT.kTRUE) # works too - recommended! 

		self.workspace.defineSet("parameters", fullMCmodelHP.getParameters(ROOT.RooArgSet(fitvariable)))
		self.workspace.defineSet("observables", ROOT.RooArgSet(fitvariable))

		if (saveworkspace): 
			self.SaveWorkspace()

		# --- LP model ----
		ttfakeWnumberLP = ROOT.RooRealVar("LP:tt:fake:number", "LP:tt:fake:number", 1e5, 500., 1e20)

		ttrealWshapeLP = ROOT.RooDoubleCrystalBall("LP:tt:real:shape","LP:tt:real:shape", fitvariable, ttrealWmean, ttrealWsigma, ttrealWalpha1, ttrealWsign1, ttrealWalpha2, ttrealWsign2)
		ttrealWnumberLP = ROOT.RooRealVar("LP:tt:real:number", "LP:tt:real:number", 1e5, 500., 1e20)
		ttrealWmodelLP = ROOT.RooExtendPdf("LP:tt:real:model", "LP:tt:real:model", ttrealWshapeLP, ttrealWnumberLP)

		self.ImportToWorkspace(ttrealWmodelLP, saveworkspace, ROOT.RooFit.RecycleConflictNodes())

		ttfakeWoffsetLP = ROOT.RooRealVar("LP:tt:fake:offset" ,"LP:tt:fake:offset", 80, 10, 200) # 90, 10, 200
		ttfakeWwidthLP  = ROOT.RooRealVar("LP:tt:fake:width" ,"LP:tt:fake:width", 40, 25, 300) # 40, 25, 100
		ttfakeWcoefficientLP  = ROOT.RooRealVar("LP:tt:fake:coefficient" ,"LP:tt:fake:coefficient", -0.03, -1., -0.0001) # -0.04, -1, 0.
		ttfakeWshapeLP     = ROOT.RooErfExpPdf("LP:tt:fake:shape", "LP:tt:fake:shape" ,fitvariable, ttfakeWcoefficient, ttfakeWoffsetLP, ttfakeWwidthLP)
		ttfakeWnumberLP = ROOT.RooRealVar("LP:tt:fake:number", "LP:tt:fake:number", 1e5, 500., 1e20)
		ttfakeWmodelLP = ROOT.RooExtendPdf("LP:tt:fake:model", "LP:tt:fake:model", ttfakeWshapeLP, ttfakeWnumberLP)

		self.ImportToWorkspace(ttfakeWmodelLP, saveworkspace, ROOT.RooFit.RecycleConflictNodes())

		VVnumberLP = ROOT.RooRealVar("LP:VV:number", "LP:VV:number", 1e5, 500., 1e20)
		VVshapeLP = ROOT.RooAddPdf("LP:VV:shape","LP:VV:shape", ROOT.RooArgList(VVExp, VVGauss), ROOT.RooArgList(VVfactor))
		VVmodelLP = ROOT.RooExtendPdf("LP:VV:model", "LP:VV:model", VVshapeLP, VVnumberLP)

		self.ImportToWorkspace(VVmodelLP, saveworkspace, ROOT.RooFit.RecycleConflictNodes())

		STcoeffLP = ROOT.RooRealVar("LP:st:coefficient", "LP:st:coefficient", -0.04, -1., 1.)
		STwidthLP = ROOT.RooRealVar("LP:st:width","LP:st:width", 30., 0., 400.)
		SToffsetLP = ROOT.RooRealVar("LP:st:offset", "LP:st:offset", 60., 50., 100.)
		#STmeanLP = ROOT.RooRealVar("LP:st:mean", "LP:st:mean", gaus_means, gaus_means*.8, gaus_means*1.2)
		#STsigmaLP = ROOT.RooRealVar("LP:st:sigma", "LP:st:sigma", gaussigmas, gaussigmas*.5, gaussigmas*1.5)
		STErfExpLP = ROOT.RooErfExpPdf("LP:st:ErfExp", "LP:st:ErfExp", fitvariable, STcoeffLP, SToffsetLP, STwidthLP)
		STGaussLP = ROOT.RooGaussian ("LP:st:Gaussian" ,"LP:st:Gaussian" , fitvariable, STmean, STsigma)
		STfactorLP = ROOT.RooRealVar("LP:st:factor", "LP:st:factor", 0.3, 0.0, 0.99)
		STshapeLP = ROOT.RooAddPdf("LP:st:shape", "LP:st:shape", STErfExpLP, STGaussLP, STfactor)
		STnumberLP = ROOT.RooRealVar("LP:st:number", "LP:st:number", 1e5, 500., 1e20)
		STmodelLP = ROOT.RooExtendPdf("LP:st:model", "LP:st:model", STshapeLP, STnumberLP)

		self.ImportToWorkspace(STmodelLP, saveworkspace, ROOT.RooFit.RecycleConflictNodes()) # TODO: Maybe set this the default behaviour 

		WJetscoeffLP  = ROOT.RooRealVar("LP:WJets:coefficient", "LP:WJets:coefficient", -0.026, -0.05, 0.01)
		WJetsoffsetLP = ROOT.RooRealVar("LP:WJets:offset", "LP:WJets:offset" ,80. ,0., 100)
		WJetswidthLP  = ROOT.RooRealVar("LP:WJets:width", "LP:WJets:width", 30., 1., 100.)
		WJetsshapeLP  = ROOT.RooErfExpPdf("LP:WJets:shape", "LP:WJets:shape", fitvariable, WJetscoeffLP, WJetsoffsetLP, WJetswidthLP)
		WJetsnumberLP = ROOT.RooRealVar("LP:WJets:number", "LP:WJets:number", 1e5, 500., 1e20)
		WJetsmodelLP = ROOT.RooExtendPdf("LP:WJets:model", "LP:WJets:model", WJetsshapeLP, WJetsnumberLP)

		self.ImportToWorkspace(WJetsmodelLP, saveworkspace, ROOT.RooFit.RecycleConflictNodes())

		mcTTnumberLP = ROOT.RooRealVar("LP:MC:number", "LP:MC:number", 1e5, 500., 1e20)

		fullMCmodelLP = ROOT.RooAddPdf("LP:fullMC:model", "LP:fullMC:model", ROOT.RooArgList(ttrealWshapeLP, ttfakeWshapeLP, VVshapeLP, STshapeLP, WJetsshapeLP), ROOT.RooArgList(ttrealWnumberLP, ttfakeWnumberLP, VVnumberLP, STnumberLP, WJetsnumberLP)) # TODO: check if want to add models instead of shapes



		# --- Combined model ---- 

		minimalHPModel = ROOT.RooAddPdf("HP:minimalMC:model", "HP:minimalMC:model", ROOT.RooArgList(ttfakeWshape, ttrealWshape), ROOT.RooArgList(ttfakeWnumber, mcTTnumber)) # TODO: check if want to add models instead of shapes
		minimalLPModel = ROOT.RooAddPdf("LP:minimalMC:model", "LP:minimalMC:model", ROOT.RooArgList(ttfakeWshape, ttrealWshape), ROOT.RooArgList(ttfakeWnumberLP, mcTTnumberLP)) # TODO: check if want to add models instead of shapes
		simultaneousmodel = ROOT.RooSimultaneous("simultaneousMCmodel", "simultaneousMCmodel", regions)
		simultaneousmodel.addPdf(fullMCmodelHP, "HP") # self.LoadPdf("HP:fullMC:model"), "HP"
		simultaneousmodel.addPdf(fullMCmodelLP, "LP")

		#regions.addToRange("fitRange_HP", "HP")
		#regions.addToRange("fitRange_LP", "LP")

		self.ImportToWorkspace(simultaneousmodel, saveworkspace, ROOT.RooFit.RecycleConflictNodes())
		







		#self.SaveWorkspace()


		#getattr(self.workspace, "import")(signalModel)
		#self.ImportToWorkspace(signalModel, True)
		#self.workspace.Write()
		#self.SaveWorkspace()


	def CreateWorkspace(self, options, filename): 
		if (self.CheckWorkspaceExistence(filename)): 
			print "Workspace already exists! "
			print "A workspace with name '{}' already exists, are you sure you want to overwrite it? ".format(filename) 
			rep = self.PromptYesNo()
			if rep == 'no': 
				print "Aborting!"
				sys.exit()

		assert((options.cutHP > 0.) and (options.cutHP < 1.)), "ERROR: Invalid HP cut. Please choose a HP cut in ]0, 1[."
		assert((options.cutLP > 0.) and (options.cutLP < 1.)), "ERROR: Invalid LP cut. Please specify a LP cut in ]0, 1[."
		assert(options.cutHP < options.cutLP), "ERROR: Inverted cuts! Pleas make sure (HP cut) < (LP cut)."
		workspace = ROOT.RooWorkspace(self.workspacename, self.workspacename)

		mass = ROOT.RooRealVar(options.massvar, options.massvar, options.minX, options.maxX) #workspace.var("mass") # TODO: Do we really want to set a range here (additional cut w.r.t. tree variable)?
		tagger = ROOT.RooRealVar(options.tagger, options.tagger, 0., 1.)
		weight = ROOT.RooRealVar(options.weightvar, options.weightvar, 0., 10000000.)    # variables = ROOT.RooArgSet(x, y)
		# For importing a TTree into RooDataSet the RooRealVar names must match the branch names, see: https://root.cern.ch/root/html608/rf102__dataimport_8C_source.html

		cutPass = "({} <= {})".format(options.tagger, options.cutHP)
		cutFail = "({0} > {1}) && ({0} <= {2})".format(options.tagger, options.cutHP, options.cutLP)
		cut = ""

		argset = ROOT.RooArgSet(mass, weight, tagger)  # TODO: Does the weight need to be included here? 

		weightvarname = options.weightvar #"weight" # TODO: put this in the

		dataset = Dataset(options.year) 

		# TODO: investigate usage of RooRealVar.setRange() to set HP and LP ranges 
		for sample in ["VV", "st", "WJets"]: # "tt", 
			getattr(workspace, "import")(self.CreateDataset(dataset.getSample(sample), sample, argset, cut))
			workspace.writeToFile(filename)
			#getattr(workspace, "import")(self.CreateDataset(dataset.getSample(sample), "LP:"+sample, argset, cutFail, weightvarname))
			#workspace.writeToFile(filename)

		# For tt we need an additional cut to separate it into gen matched merged W and unmerged
		additionalCutMerged = "(genmatchedAK82017==1)" #"&&(genmatchedAK82017==1)"
		additionalCutUnmerged = "(genmatchedAK82017==0)" #"&&(genmatchedAK82017==0)"
		merged = ROOT.RooRealVar("genmatchedAK82017", "genmatchedAK82017", 0., 1.)
		argset.add(merged)
		getattr(workspace, "import")(self.CreateDataset(dataset.getSample("tt"), "ttrealW", argset, additionalCutMerged))
		workspace.writeToFile(filename)
		#getattr(workspace, "import")(self.CreateDataset(dataset.getSample("tt"), "HP:ttfakeW", argset, cutPass+additionalCutUnmerged, weightvarname))
		#workspace.writeToFile(filename)
		#getattr(workspace, "import")(self.CreateDataset(dataset.getSample("tt"), "LP:ttrealW", argset, cutFail+additionalCutMerged, weightvarname))
		#workspace.writeToFile(filename)
		getattr(workspace, "import")(self.CreateDataset(dataset.getSample("tt"), "ttfakeW", argset, additionalCutUnmerged))

		# The ranges will be set at a later point
		cutHP = ROOT.RooRealVar("cutHP", "cutHP", options.cutHP) # TODO: do we really want to store the cuts here? should probably be stored as snapshots of ranges 
		cutLP = ROOT.RooRealVar("cutLP", "cutLP", options.cutLP)
		getattr(workspace, "import")(cutHP)
		getattr(workspace, "import")(cutLP)


		#sample = dataset.getSample("tt")
		#roodataset = self.CreateDataset(sample, "tt", argset, cutPass, "weight")
		#getattr(workspace, "import")(roodataset) 

		# TODO: add cut values to workspace
		# TODO: use RooDataSet.merge or RooDataDet.append to generate the bkg dataset 
		
		workspace.writeToFile(filename)

		return workspace


