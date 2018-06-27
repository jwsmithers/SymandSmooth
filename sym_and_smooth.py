
from itertools import islice
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.patches as mpatches

Systematic={}

with open('ee_mumu_emu_merged.config', 'r') as f:
    for line in f:
        if 'Systematic:' in line:
            name = line.replace("Systematic:","").replace('"','').replace("_","\\_").strip()
            block = ''.join(islice(f, 10))
            Systematic[name] = block

cleaned_systematic={}
for key, value in Systematic.iteritems():
  cleaned_systematic[key] = {}
  if "Smoothing" in value:
    if "\%Smoothing" in value:
      cleaned_systematic[key]["Smoothing"] = 0
    elif "PreSmoothing" in value:
      cleaned_systematic[key]["Smoothing"] = 0
    else:
      cleaned_systematic[key]["Smoothing"] = 1
  else: 
    cleaned_systematic[key]["Smoothing"] = 0


  if "PreSmoothing" in value:
    if "\%PreSmoothing" in value:
      cleaned_systematic[key]["PreSmoothing"] = 0
    else:
      cleaned_systematic[key]["PreSmoothing"] = 1
  else: 
    cleaned_systematic[key]["PreSmoothing"] = 0


  if "Symmetrisation" in value:
    if "\%Symmetrisation" in value: 
      cleaned_systematic[key]["Symmetrisation"]= 0
    else:
      if "ONESIDED" in value:
        cleaned_systematic[key]["Symmetrisation"] = "ONESIDED"
      elif "TWOSIDED" in value:
        cleaned_systematic[key]["Symmetrisation"] = "TWOSIDED"
  else:
    cleaned_systematic[key]["Symmetrisation"]= 0


labels = []
plt.figure(figsize=(10, 20))
ax = plt.subplot(1,1,1)


i = 0
ewidth = 18
errorwidth=0.2
for key2, value2 in sorted(cleaned_systematic.iteritems()):
  if "bTag" in key2:continue
  if "JET" in key2:continue
  if "MUON" in key2:continue
  if "MET" in key2:continue

  # if "bTag" not in key2:continue
  # if "JET" not in key2:continue
  # if "MUON" not in key2 and "MET" not in key2:continue

  labels.append(key2)
  # print value2["Smoothing"]
  if value2["Smoothing"] ==1:
    plt.errorbar(0.5, i,xerr=errorwidth, ecolor="blue",color="blue",marker="None",ms=3,
        elinewidth=ewidth,capsize=0)
  if value2["PreSmoothing"] ==1:
    plt.errorbar(1, i,xerr=errorwidth, ecolor="red",color="red",marker="None",ms=3,
        elinewidth=20,capsize=0)
  if value2["Symmetrisation"] == "TWOSIDED":
    plt.errorbar(1.5, i,xerr=errorwidth, ecolor="purple",color="purple",marker="None",ms=3,
        elinewidth=ewidth,capsize=0)
  if value2["Symmetrisation"] == "ONESIDED":
    plt.errorbar(2, i,xerr=errorwidth, ecolor="green",color="green",marker="None",ms=3,
      elinewidth=ewidth,capsize=0)
  i = i +1

plt.yticks(np.arange(len(labels)), labels)
# plt.yticks(np.arange(len(labels)), r'%s' %labels)

plt.gca().yaxis.grid(True)
plt.axis([0.2, 2.2,-0.5,len(labels)+3])

Smoothing = mpatches.Patch(color='blue', label='Smoothing')
PreSmoothing = mpatches.Patch(color='red', label='PreSmoothing')
TWOSIDED = mpatches.Patch(color='purple', label='TwoSided')
ONESIDED = mpatches.Patch(color='green', label='OneSided')
plt.legend(handles=[Smoothing, PreSmoothing,TWOSIDED,ONESIDED],loc=1,frameon=False,ncol=2,borderaxespad=0.,columnspacing=0.4)
plt.text(0.08,0.985,r"\textit{\textbf{ATLAS}} \large{Internal}",
          fontsize=18, color='black',transform=ax.transAxes)
plt.text(0.08,0.97,r"$\sqrt{s}=13$~TeV, 36.1, fb$^{-1}$",
          fontsize=14, color='black',transform=ax.transAxes)
# plt.text(0.08,0.955,r"Dilepton",
#           fontsize=14, color='black',transform=ax.transAxes)
plt.text(0.08,0.955,r"Single lepton",
          fontsize=14, color='black',transform=ax.transAxes)
plt.tight_layout()

plt.savefig("dilepton1.pdf")