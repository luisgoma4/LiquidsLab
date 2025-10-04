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

# Load data from CSV files
real_csv_file = '/home/luisg/Documents/Liquids Lab/Dielectric Spectroscopy/Water+Silica/real_silica_water_norm.csv'
imaginary_csv_file = '/home/luisg/Documents/Liquids Lab/Dielectric Spectroscopy/Water+Silica/imag_silica_water_norm.csv'

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
ax.set_title('Capacitance Module and Phase vs Temperature and Logarithm of Frequency')

# Initialize rotation angles and acceleration parameters
angles = [0, 0, 0]  # Initial rotation angles for x, y, z axes
angular_velocities = [1, 1, 1]  # Constant angular velocities for x, y, z axes
acceleration_axis = random.choice([0, 1, 2])  # Randomly choose initial axis for acceleration
cbar = fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(0, 1), cmap='hsv'), ax=ax, label='Normalized Phase')

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

# # Create animation
# ani = FuncAnimation(fig, update, frames=np.arange(0, 1000), interval=50, blit=True)

# Show the animation
plt.show()
