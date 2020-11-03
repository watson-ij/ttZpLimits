import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import crystalball
from scipy.integrate import quad
from scipy.special import gammaln
import pymultinest
import mpi4py

import sys


def Integral(m):
    return 4769 * np.power(m, -0.9)


def Alpha(m):
    return -0.00785 * m - 0.512

def Sigma(m):
    return 0.2 * m - 2.8

def Mu(m):
    return 0.582 * m + 5.43


def SignalCB(mass):
    alpha = Alpha(mass)
    mu = Mu(mass)
    sigma = Sigma(mass)

    n = 1.5

    return crystalball(beta=abs(alpha), m=n, loc=-mu, scale=sigma)


def ttVCB():
    return crystalball(0.99, 1.6, -60.5, 16.3)


def ttWCB():
    return crystalball(1.11, 1.37, -85.6, 55.37)


def AsymptoticSignalGenerator(param_arr, lumi=3000):
    g = param_arr[0]
    m = param_arr[1]

    # Parametrically define the CB params in terms of the mass.
    kfact = 1.23
    gscale = ((g / 0.1) ** 2)
    integral = kfact * gscale * Integral(m) * (lumi / 3000)
    alpha = Alpha(m)
    n = 1.5
    mu = Mu(m)
    sigma = Sigma(m)

    nbins = 26

    # we have to define the crystalball in negative x and then flip the values since scipy.stats does not suppoer
    # left-tailed CBs.
    bin_arr = np.linspace(-200, 0, nbins)
    def density_function(x):
        return crystalball.pdf(x, beta=abs(alpha), m=n, loc=-mu, scale=sigma)

    obs = np.zeros(bin_arr.shape[0] - 1)
    left_edge = bin_arr[0]
    for i in range(1, bin_arr.shape[0]):
        right_edge = bin_arr[i]
        obs[i-1] = quad(density_function, left_edge, right_edge)[0]
        left_edge = right_edge

    return integral * np.flip(obs)


def AsympXsBrSignalGenerator(param_arr, lumi=3000):
    xs = param_arr[0]
    m = param_arr[1]

    # Parametrically define the CB params in terms of the mass.
    kfact = 1.23
    efficiency = 0.0000165 * m - 0.0000595
    integral = kfact * xs * lumi * efficiency * 1000
    alpha = Alpha(m) #-0.007150252625905558 * m - 0.41051963479597414
    n = 1.5
    mu = Mu(m) #0.562757569969562 * m + 4.464695509350186
    sigma = Sigma(m) #0.20556116057791995 * m - 3.241756041434955

    nbins = 26

    # we have to define the crystalball in negative x and then flip the values since scipy.stats does not suppoer
    # left-tailed CBs.
    bin_arr = np.linspace(-200, 0, nbins)

    def density_function(x):
        return crystalball.pdf(x, beta=abs(alpha), m=n, loc=-mu, scale=sigma)

    obs = np.zeros(bin_arr.shape[0] - 1)
    left_edge = bin_arr[0]
    for i in range(1, bin_arr.shape[0]):
        right_edge = bin_arr[i]
        obs[i - 1] = quad(density_function, left_edge, right_edge)[0]
        left_edge = right_edge

    return integral * np.flip(obs)


def AsymptoticTTVGenerator(lumi=3000):
    # Encode background PDFs
    # K-factor [1507.05640]
    kfact = 1.26
    integral = (170*lumi/3000) * kfact

    nbins = 26

    bin_arr = np.linspace(-200, 0, nbins)
    def density_function(x):
        return crystalball.pdf(x, 0.99, 1.6, -60.5, 16.3)

    obs = np.zeros(bin_arr.shape[0] - 1)
    left_edge = bin_arr[0]
    for i in range(1, bin_arr.shape[0]):
        right_edge = bin_arr[i]
        obs[i-1] = quad(density_function, left_edge, right_edge)[0]
        left_edge = right_edge

    return integral * np.flip(obs)



def AsymptoticTTWGenerator(lumi=3000):
    # Encode background PDFs
    # K-factor [1507.05640]
    kfact = 1.22
    integral = (107 * lumi / 3000) * kfact

    nbins = 26

    bin_arr = np.linspace(-200, 0, nbins)
    def density_function(x):
        return crystalball.pdf(x, 1.11, 1.37, -85.6, 55.37)

    obs = np.zeros(bin_arr.shape[0] - 1)
    left_edge = bin_arr[0]
    for i in range(1, bin_arr.shape[0]):
        right_edge = bin_arr[i]
        obs[i-1] = quad(density_function, left_edge, right_edge)[0]
        left_edge = right_edge

    return integral * np.flip(obs)




# Map the interval [0,1] to the appropriate intervals for g and m ([0,1] and [30,200], respectively).
def FlatPrior(cube, ndim, nparams):
    cube[0] = cube[0] # coupling
    cube[1] = cube[1] * 350 + 30  # mass



def main(luminosity=3000):

    # Plot some sample distributions
    plot = False
    if plot == True:
        # Test the PDF shapes.
        def amp(g,m):
            gscale = ((g / 0.1) ** 2)
            return gscale * (217 - 35.8 * np.log(m))

        ttv_int = 209
        ttw_int = 140

        fig, ax = plt.subplots(1, 1)
        bins = np.linspace(4,196,25)
        x = np.linspace(0,200,1000)
        cb40 = SignalCB(40)
        cb70 = SignalCB(70)
        cb150 = SignalCB(150)
        ax.plot(x, 7.6*Integral(40)*cb40.pdf(-x), color='blue', ls='dashed', label="40 GeV Fit")
        ax.plot(x, 8*Integral(70)*cb70.pdf(-x), color='orange', ls='dashed', label="70 GeV Fit")
        ax.plot(x, 8*Integral(150)*cb150.pdf(-x), color='red', ls='dashed', label="150 GeV Fit")
        ax.plot(bins, AsymptoticTTVGenerator(), drawstyle='steps-mid', color='black', label="ttV")
        ax.plot(bins, AsymptoticTTWGenerator(), drawstyle='steps-mid', color='grey', label="ttW")
        ax.plot(bins, AsymptoticSignalGenerator([0.1, 40]), drawstyle='steps-mid', color='blue', label="40 GeV")
        ax.plot(bins, AsymptoticSignalGenerator([0.1, 70]), drawstyle='steps-mid', color='orange', label="70 GeV")
        ax.plot(bins, AsymptoticSignalGenerator([0.1, 150]), drawstyle='steps-mid', color='red', label="150 GeV")
        plt.xlabel("test")
        plt.legend()
        plt.ylim((0,75))
        plt.xlim((16,200))
        plt.savefig("plots/mass_histos_asymptotic.png")


    # Define model parameters
    bkg = AsymptoticTTWGenerator(lumi=luminosity) + AsymptoticTTWGenerator(lumi=luminosity)
    n_bins = bkg.shape[0]
    width = np.sqrt(bkg) + 1
    def LogLikelihood(cube, D, N):
        signal = AsympXsBrSignalGenerator(cube, lumi=luminosity)
        sig_bkg = signal + bkg
        ll = np.zeros(n_bins)

        for i in range(2,n_bins):  # Begin at i=2 corresponding to the 16 GeV bin
            if width[i] == 0:
                continue
            ll[i] = -0.5 * np.log(2 * np.pi * width[i] ** 2) - 0.5 * ((sig_bkg[i] - bkg[i]) / width[i]) ** 2
        return np.sum(ll)

    def LogPoisson(cube, D, N):
        signal = AsympXsBrSignalGenerator(cube, lumi=luminosity)
        sig_bkg = signal + bkg
        ll = np.zeros(n_bins)

        for i in range(2,n_bins):  # Begin at i=2 corresponding to the 16 GeV bin
            mu = sig_bkg[i]
            nn = bkg[i]
            ll[i] = nn * np.log(mu) - mu - gammaln(nn+1)
        return np.sum(ll)


    parameters = ["xsbr", "MZp"]
    n_params = len(parameters)
    file_string = "mn_out_asymptotic_xsbr_largeMass_" + str(luminosity)
    text_string = file_string + "/" + file_string
    json_string = file_string + "/params.json"


    #run Multinest
    pymultinest.run(LogLikelihood, FlatPrior, n_params, outputfiles_basename=text_string,
                    resume=False, verbose=True, n_live_points=8000, const_efficiency_mode=True,
                    evidence_tolerance=0.05, sampling_efficiency=0.3)
    json.dump(parameters, open(json_string, 'w'))  # save parameter names




if __name__ == "__main__":
  main(int(sys.argv[1]))
