from pyCEvNS.plot import CrediblePlot
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib as mpl


import numpy as np

def upsilonConstraint(m, g_tau):
  return np.sqrt((1.74e-8)*32*np.pi*m) / g_tau

def upsilonConstraintLowMass(m, g_tau):
    mups = 9.46
    mf = (mups ** 2 ) / (m ** 2 - mups ** 2)
    return 4*np.pi * 0.015 / (137 * mf * g_tau)

def upsilonConstraintAloni(m, g_tau):
  #return (-0.0613788 + 0.0418243 * np.sqrt(2.15445 + 0.001466 * (m**2))) / g_tau
  #return (3.29 * 0.01 / (40 ** 2)) * (m ** 2) / g_tau
  return (-0.001841350393086527 + 0.00002057437358467554 * (m ** 2)) / g_tau

def upsilonConstraintZeroTauMass(m, g_tau):
  return (3.29 * 0.01 / (40 ** 2)) * (m ** 2) / g_tau

def upsilonConstraint181102567(m,g_tau):
  return (4*np.pi / g_tau)*(0.01 / 1.7)*((m / 70)**2)

def gxUpsilonConstraint(m):
  return np.sqrt((1.74e-8)*32*np.pi*m / 0.10543)

n_pts = np.linspace(30, 350, 200)

#fake_line_150 = 0.03*np.ones(200) + 0.005*np.random.random_sample(200)

mpl.rcParams["legend.facecolor"] = 'white'
print("Plotting XS*BR limit")
fig, ax = plt.subplots()
ax.set_facecolor('steelblue')
plt.yscale('log')
plt.fill_between(n_pts, 0.001, 0.002, facecolor='white', alpha=1)
#plt.fill_between(n_pts, 0.018, 0.003, facecolor='royalblue', alpha=1)
plt.fill_between(n_pts, 0.002, 0.02, facecolor='lightskyblue', alpha=1)

cp150 = CrediblePlot("mn_out_asymptotic_xsbr_largeMass_150/mn_out_asymptotic_xsbr_largeMass_150.txt")
cp300 = CrediblePlot("mn_out_asymptotic_xsbr_largeMass_300/mn_out_asymptotic_xsbr_largeMass_300.txt")
cp3000 = CrediblePlot("mn_out_asymptotic_xsbr_largeMass_3000/mn_out_asymptotic_xsbr_largeMass_3000.txt")

cp150.credible_2d([1,0], credible_level=(0.95,), nbins=42, ax=ax, color='royalblue')
cp300.credible_2d([1,0], credible_level=(0.95,), nbins=42, ax=ax, color='lightskyblue')
cp3000.credible_2d([1,0], credible_level=(0.95,), nbins=42, ax=ax, color='w')
patch150 = mpatches.Patch(color='steelblue', label=r'150 fb$^{-1}$')
patch300 = mpatches.Patch(color='royalblue', label=r'300 fb$^{-1}$')
patch3000 = mpatches.Patch(color='lightskyblue', label=r'3000 fb$^{-1}$')

plt.xlabel(r"$m_{Z^\prime}$ [GeV]", fontsize=12)
plt.ylabel(r"$\sigma \times BR(Z^\prime \to \tau \tau)$ [pb]", fontsize=12)

plt.legend(handles=[patch150, patch300, patch3000],facecolor='white', framealpha=1.0)
plt.ylim((0.001, 1))
plt.xlim((33,350))

plt.savefig("plots/ttzpout_asymptotic_limits_30_350_gev_xsbr.png")
plt.savefig("plots/ttzpout_asymptotic_limits_30_350_gev_xsbr.pdf")



plt.clf()



# Plot coupling versus mass.
print("plotting g vs m limit")

n_pts_350GeV = np.linspace(30, 350, 200)


fig2, ax2 = plt.subplots()
ax2.set_facecolor('steelblue')
plt.yscale('log')
cp150 = CrediblePlot("mn_out_asymptotic_largeMass_gaus_150/mn_out_asymptotic_largeMass_gaus_150.txt")
cp300 = CrediblePlot("mn_out_asymptotic_largeMass_gaus_300/mn_out_asymptotic_largeMass_gaus_300.txt")
cp3000 = CrediblePlot("mn_out_asymptotic_largeMass_gaus_3000/mn_out_asymptotic_largeMass_gaus_3000.txt")

cp150.credible_2d([1,0], credible_level=(0.95,), nbins=38, ax=ax2, color='royalblue')
cp300.credible_2d([1,0], credible_level=(0.95,), nbins=38, ax=ax2, color='lightskyblue')
cp3000.credible_2d([1,0], credible_level=(0.95,), nbins=38, ax=ax2, color='w')
plt.plot(n_pts_350GeV, upsilonConstraintAloni(n_pts_350GeV,0.5), c='darkorange', ls='dashed',
         linewidth=3, label=r'$\Upsilon \to \tau^+ \tau^-$')
patch150 = mpatches.Patch(color='steelblue', label=r'150 fb$^{-1}$')
patch300 = mpatches.Patch(color='royalblue', label=r'300 fb$^{-1}$')
patch3000 = mpatches.Patch(color='lightskyblue', label=r'3000 fb$^{-1}$')
upsilon_line = mlines.Line2D([], [], color='darkorange', linestyle='dashed',
                          markersize=15, label=r'$\Upsilon \to \tau^+ \tau^-$')
plt.legend(handles=[upsilon_line])

plt.xlabel(r"$m_{Z^\prime}$ [GeV]", fontsize=12)
plt.ylabel(r"$g_t$", fontsize=12)
plt.title(r'$g_\tau = 0.5$', loc='right')
plt.legend(handles=[upsilon_line, patch150, patch300, patch3000],facecolor='white',
           loc='upper right', framealpha=1.0)
plt.ylim((0.01, 1))
plt.xlim((34,350))

plt.savefig("plots/ttzpout_asymptotic_300_3000_95_largeMass_gaus.png")
plt.savefig("plots/ttzpout_asymptotic_300_3000_95_largeMass_gaus.pdf")


