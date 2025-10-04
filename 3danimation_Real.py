import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import random

# Function to read temperature and frequency data from a CSV file
def read_data_from_csv(file_path):
    # Read CSV file specifying the decimal separator
    df = pd.read_csv(file_path, decimal='.', header=None)
    temperatures = df.iloc[0, 1:].values.astype(float)  # Get temperatures from the second column
    frequencies = df.iloc[1:, 0].values.astype(float)    # Get frequencies from the second row
    data = df.iloc[1:, 1:].values.astype(complex)        # Get capacitance data as complex numbers
    return temperatures, frequencies, data

def plot3D(sample):
    # Load data from CSV files
    real_csv_file = f'/home/luisg/Documents/Liquids Lab/Dielectric Spectroscopy/{sample}/ReCap_{sample}.csv'
    imaginary_csv_file = f'/home/luisg/Documents/Liquids Lab/Dielectric Spectroscopy/{sample}/ImCap_{sample}.csv'

    # Read real and imaginary capacitance data from CSV files
    temperatures, frequencies, real_capacitance = read_data_from_csv(real_csv_file)
    _, _, imaginary_capacitance = read_data_from_csv(imaginary_csv_file)

    # Combine real and imaginary parts to form complex capacitance
    capacitance = real_capacitance + 1j * imaginary_capacitance
    module = np.abs(capacitance)  # Calculate capacitance magnitude
    phase = np.angle(capacitance)  # Calculate capacitance phase

    # Take logarithm of frequencies
    log_frequencies = np.log10(frequencies)

    # Normalize phase to [0, 1]
    normalized_phase = (phase - phase.min()) / (phase.max() - phase.min())

    # Create a 2D grid of coordinates for temperatures and logarithm of frequencies
    T, F_log = np.meshgrid(temperatures, log_frequencies)

    # Check and clean up module and phase data (remove non-finite values)
    module = np.nan_to_num(module)

    # Create a 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the module on the z-axis and normalized phase in colors
    surf = ax.plot_surface(T, F_log, module, facecolors=plt.cm.hsv(normalized_phase), shade=False)

    # Set labels and title
    ax.set_xlabel('Temperature')
    ax.set_ylabel('Logarithm of Frequency')
    ax.set_zlabel('Capacitance Module')
    ax.set_title(f'{sample}')

    # Initialize rotation angles and acceleration parameters
    angles = [0, 0, 0]  # Initial rotation angles for x, y, z axes
    angular_velocities = [1, 1, 1]  # Constant angular velocities for x, y, z axes
    acceleration_axis = random.choice([0, 1, 2])  # Randomly choose initial axis for acceleration

    # Animation function to update plot
    def update(frame):
        global angles, acceleration_axis
        
        # Update rotation angles based on constant angular velocities
        angles = [(angles[i] + angular_velocities[i]) % 360 for i in range(3)]
        
        # Add random acceleration to one axis every ten seconds
        if frame % 200 == 0:  # Frame duration is 50 ms, 200 frames ≈ 10 seconds
            acceleration_axis = random.choice([0, 1, 2])  # Randomly choose axis for acceleration
        
        # Apply acceleration to the chosen axis
        angular_velocities[acceleration_axis] += np.random.uniform(-0.5, 0.5)
        
        # Update view angle for animation
        ax.view_init(30, angles[0])  # Rotate around x-axis
        ax.view_init(angles[1], angles[2])  # Rotate around y and z axes
        
        return surf,
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])  # reducir el ancho del gráfico

    # Añadir la colorbar y ajustarla
    cbar = fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(0, 1), cmap='hsv'), ax=ax,shrink=0.5, aspect=10, pad=0.1, label='Normalized Phase')
    # # Create animation
    # ani = FuncAnimation(fig, update, frames=np.arange(0, 1000), interval=50, blit=True)
    plt.tight_layout()
    # Show the animation
    plt.show()

plot3D('watercarbon')
 