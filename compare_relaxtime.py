import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


samples = ['water', 'watercarbon', 'watersilica2']
markers = ['x', '.', '^']
fig, ax = plt.subplots()

for i, sample in enumerate(samples):
    
    directorio=f'/home/luisg/Documents/Liquids Lab/Dielectric Spectroscopy 2/{sample}/'
    time_temp = f'{directorio}relaxation_time.csv'
    
    df = pd.read_csv(time_temp, decimal='.', header=0)
    time = df.iloc[:, 0].values.astype(float)  # Get time from the first colum
    temp = df.iloc[:, 1].values.astype(float)
    

    ax.semilogy(temp, time, markers[i], label=f'{sample}')

ax.set_title('Relaxation Time')
ax.set_xlabel('T')
ax.set_ylabel(r'$\tau$')
ax.set_ylim(0.0000001,1 )
ax.set_xlim(125, 300)

ax.relim()
ax.autoscale_view()

plt.legend(loc='best')
plt.show() 