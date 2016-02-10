# coding: utf-8
# (c) 2015-12-09 Teruhisa Okada

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.fftpack
import pandas as pd


def fft(x, method='np'):
    if method == 'np':
        return fft_np(x)
    elif method == 'sp':
        pass


def fft_np(x):
    fs = 1.0/24/366
    start = 0  # サンプリングする開始位置
    N = len(x)   # FFTのサンプル数
    X = np.fft.fft(x[start:start+N])  # FFT
    freqList = np.fft.fftfreq(N, d=1.0/fs)  # 周波数軸の値を計算
    amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]  # 振幅スペクトル
    phaseSpectrum = [np.arctan2(int(c.imag), int(c.real)) for c in X]    # 位相スペクトル
    return freqList, amplitudeSpectrum, phaseSpectrum


def fft_sp(x):
    pass


def plot_phase(freqList, phaseSpectrum):
    plt.figure(figsize=(10,10))
    # 位相スペクトルを描画
    plt.subplot(313)
    plt.loglog(freqList, phaseSpectrum, '-', alpha=0.5)
    #plt.axis([0, fs/2, -np.pi, np.pi])
    plt.xlabel("frequency [Hz]")
    plt.ylabel("phase spectrum")


def plot_value(x):
    plt.figure(figsize=(10,3))
    plt.plot(x, '-')
    plt.xlabel("time [sample]")
    plt.ylabel("amplitude")


def plot_power(freqList, amplitudeSpectrum):
    plt.figure(figsize=(5,5))
    plt.loglog(freqList, amplitudeSpectrum, '-')
    #plt.xlim(0, fs/2)
    plt.xlim(10**-8, 10**-3)
    plt.xlabel("frequency [Hz]")
    plt.ylabel("amplitude spectrum")


def plot(x):
    freqList, amplitudeSpectrum, phaseSpectrum = fft(x)
    plot_value(x)
    plot_power(freqList, amplitudeSpectrum)


def test_tide():
    csvfile = 'F:/okada/Data/tide/tide_OS_2012.csv'
    df = pd.read_csv(csvfile)
    x = df.tide.dropna().values
    plot(x)


def test_tide():
    csvfile = 'F:/okada/Data/tide/tide_OS_2012.csv'
    df = pd.read_csv(csvfile)
    x = df.tide.dropna().values
    plot(x)


def test_mp_osaka():
    from parse_mp import pickup
    tmpfile = 'F:/okada/Data/mp/mp_{0:03d}_A_20111231_20130101.csv'
    vname = 'temp'

    df = pickup(tmpfile, station=3, layer=1.0)
    x = df[vname].dropna().values
    plot(x)


if __name__ == '__main__':
    #test_tide()
    test_mp_osaka()
    plt.show()
