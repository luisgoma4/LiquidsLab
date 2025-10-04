import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os
from lmfit.models import LorentzianModel


def read_data_from_csv(file_path):
    # Read CSV file specifying the decimal separator
    df = pd.read_csv(file_path, decimal='.', header=None)
    temperatures = df.iloc[0, 1:].values.astype(float)  # Get temperatures from the second column
    frequencies = df.iloc[1:, 0].values.astype(float)    # Get frequencies from the second row
    data = df.iloc[1:, 1:].values.astype(float)        # Get capacitance data as float numbers
    return temperatures, frequencies, data

def local_max(x, y, interval, sens):
    indices_max = []

    i = 0
    while i < len(x) - interval:
        # Encontrar el índice relativo del máximo local en el intervalo actual
        local_max_index = np.argmax(y[i:i+interval])
        # Convertir el índice relativo al índice absoluto
        max_index = i + local_max_index
        
        # Verificar que el máximo local cumpla con la sensibilidad deseada
        if (max_index - sens >= 0 and max_index + sens < len(y) and
            all(y[max_index] >= y[j] for j in range(max_index - sens, max_index)) and
            all(y[max_index] >= y[j] for j in range(max_index + 1, max_index + sens + 1))):
            indices_max.append(max_index)

        # Mover al siguiente intervalo
        i += interval
    
    return indices_max

def lorentz(x, y, max, sens, ax):

    lore=LorentzianModel()
    index_max=max

    # Selecting data for the Stokes peak
    x_stoke = x[index_max - sens: index_max + sens]
    y_stoke = y[index_max - sens: index_max + sens]

    # Guessing initial parameters for the Lorentzian fit
    param_s = lore.guess(y_stoke, x=x_stoke)
    # Fitting the Lorentzian model to the Stokes peak data
    result_s = lore.fit(y_stoke, param_s, x=x_stoke)
    # Obtaining the center value of the Stokes peak
    center_s = result_s.params['center'].value

    # Obtaining the standar error 
    center_error_s = result_s.params['center'].stderr

    # Obtaining the Full Width at Half Maximum.
    fwhm_s = result_s.params['fwhm'].value

    # Obtaining the error in Full Width at Half Maximum.
    fwhm_error_s = result_s.params['fwhm'].stderr


    ax.plot(x_stoke, result_s.best_fit, 'r-')

    return center_s, np.max(result_s.best_fit)

def filter_bad_freq(frequencies, capacitance, bad_freq, threshold):
    """
    Filter out the bad frequencies from the data.
    """
    filtered_data = [(freq, cap) for freq, cap in zip(frequencies, capacitance) if abs(freq - bad_freq) > threshold]
    if filtered_data:
        frequencies, capacitance = zip(*filtered_data)
        return np.array(frequencies), np.array(capacitance)
    else:
        return np.array([]), np.array([[]])

def analize(sample, interval, sens_max, sens_lorentz):
    # Load data from CSV files
    # sample='watercarbon'
    directorio=f'/home/luisg/Documents/Liquids Lab/Dielectric Spectroscopy 2/{sample}/'
    real_csv_file = f'{directorio}ReCap_{sample}.csv'
    imaginary_csv_file = f'{directorio}ImCap_{sample}.csv'

    # Read real and imaginary capacitance data from CSV files
    temperatures, frequencies, real_capacitance = read_data_from_csv(real_csv_file)
    _, _, imaginary_capacitance = read_data_from_csv(imaginary_csv_file)


    frec_peak = []
    epsi_peak=[]
    temp_peak=[]

    for i in range(len(temperatures)):

        # Clip the frequency = 50Hz
        threshold = 1  # range in frequency 
        bad_freq = 50
        filtered_frequencies, filtered_imaginary_capacitance = filter_bad_freq(frequencies, imaginary_capacitance[:, i], bad_freq, threshold)
        
        if filtered_frequencies.size == 0 or filtered_imaginary_capacitance.size == 0:
            continue

        temp=temperatures[i]
        frequencies_log = np.log(filtered_frequencies)


        x=frequencies_log
        y=filtered_imaginary_capacitance

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_ylabel(r'$\epsilon^{\prime\prime}$')
        ax.set_xlabel('Log(f)')
        ax.set_title(f'Temp={temp:.2f}')
        list_max=local_max(x, y, interval, sens_max)
        # print(list_max)
        print(temp)
        if len(list_max)>=1 and temp>=125:
            for j in range(len(list_max)):
                max=list_max[j]
                frec, epsi = lorentz(x, y, max, sens_lorentz, ax) 
                frec_peak.append(np.exp(frec))
                epsi_peak.append(epsi)
                temp_peak.append(temperatures[i])
        else: pass
        # plt.show()

        plot='epsi_bs_frec'
        plt.savefig(os.path.join(f'{directorio}{plot}_T', f'{plot}{temp:.2f}.png'))
        plt.clf()
        plt.close()

    temp_peak=np.array(temp_peak)
    frec_peak=np.array(frec_peak)
    epsi_peak=np.array(epsi_peak)
    time= 1/(2*np.pi*frec_peak)

    pd.DataFrame({'Tau': time, 'Temp': temp_peak}).to_csv(f'{directorio}/relaxation_time.csv', index=False)

    print(np.shape(temp_peak), np.shape(time))

    fig, ax = plt.subplots()

    ax.semilogy(temp_peak, time, 'x', color='b')
    # ax.set_xscale('linear')
    # ax.set_yscale('log')

    ax.set_title('Relaxation Time')
    ax.set_xlabel('T')
    ax.set_ylabel(r'log($\tau$)')

    # ax.scatter(temp_peak, time)
    # plt.show()

    plot='relax_time_loglin'
    plt.savefig(os.path.join(f'{directorio}', f'{plot}.png'))
    plt.clf()
    plt.close()


analize('watersilica2', 5, 5, 5)

 