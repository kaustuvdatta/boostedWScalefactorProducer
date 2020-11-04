#key corresponds to samples, first and second values for keys are cross-section (in pb) the nEvents processed respectively 
#to scale MC do: float(dict['sample'][0])*lumi*1000/dict['sample'][1] 
dict_MCscaling = {
    'TTJets': ["7.546e+02", 298034800561.50085],  
	'TTToSemiLeptonic': ["6.871e+02", 34320777426.760002],
	'TTTo2L2Nu': ["6.871e+02 ", 4778168320.4034],
	'QCD_Pt_170to300': ["1.025e+05", 29522100.0],
	'QCD_Pt_300to470': ["6.762e+03", 57365509.96154332],
	'QCD_Pt_470to600': ["5.461e+02", 27559688.974354904],
	'QCD_Pt_600to800': ["1.549e+02", 64746501.56526525],
	'QCD_Pt_800to1000': ["2.597e+01", 39318800.0],
	'QCD_Pt_1000to1400': ["7.398e+00", 19970300.0],
	'QCD_Pt_1400to1800': ["6.423e-01",. 5250200.0],
	'QCD_Pt_1800to2400': ["8.671e-02", 2998500.0],
	'QCD_Pt_2400to3200': ["5.193e-03", 1911600.0],
	'QCD_Pt_3200toInf': ["1.340e-04", 800000.0],
	'QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8': ["1.347e+09", 251388.21062107597],
	'QCD_Pt-15to7000_TuneCH3_Flat_13TeV_herwig7': ["7.149e+08", 402481.3524021809],

	'WJetsToLNu': ["5.368e+04", 10460319010853.72],
	'W1JetsToLNu': ["8.897e+03", 1446225166840.4084],
	'W2JetsToLNu': ["2.835e+03", 518495842648.7594],
	'W3JetsToLNu': ["8.235e+02", 24242539.06839],
	'W4JetsToLNu': ["3.880e+02", 109148188313.11646],

	#'ST_s-channel': ["3.549e+00", 74634736.73188993], #need to recalculate nEvents
	'ST_t-channel_top': ["1.197e+02", 655197632.5140002],
	'ST_t-channel_antitop': ["7.174e+01", 265124234.84400007],
	'ST_tW_top': ["3.245e+01", 325819206.0297001],
	'ST_tW_antitop': ["3.251e+01", 298789163.8811999]
	}
