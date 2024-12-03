import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import griddata

def generateheatmaps(file_path):
    #data from the text file
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()
    x = data['x']
    y = data['y']
    min_values = data['min']
    grid_x, grid_y = np.mgrid[0:x.max():100j, 0:y.max():100j]
    grid_min_values = griddata((x, y), min_values, (grid_x, grid_y), method='cubic')


    # average time spent in min
    plt.figure(figsize=(10, 8))
    plt.contourf(grid_x, grid_y, grid_min_values, cmap="viridis", levels=50)  # Levels control the smoothness
    plt.colorbar(label='Average Time (min)')
    plt.title('Spatial Gradient of Average Time Spent at 64 Degrees')
    plt.xlabel('X Coordinates')
    plt.ylabel('Y Coordinates')
    plt.tight_layout()
    plt.savefig('2spatial_gradient_average_time.png')
    plt.show()


    # density 
    density = data.groupby(['x', 'y']).size().reset_index(name='count')
    x_density = density['x']
    y_density = density['y']
    count_values = density['count']
    grid_density_values = griddata((x_density, y_density), count_values, (grid_x, grid_y), method='cubic')


    # heatmap for density
    plt.figure(figsize=(10, 8))
    plt.contourf(grid_x, grid_y, grid_density_values, cmap="plasma", levels=50)  # Levels control the smoothness
    plt.colorbar(label='Density')
    plt.title('Spatial Gradient of Density at 64 Degrees')
    plt.xlabel('X Coordinates')
    plt.ylabel('Y Coordinates')
    plt.tight_layout()
    plt.savefig('2spatial_gradient_density.png')
    plt.show()




if __name__ == "__main__":
    file_path = "uspfile.txt"
    generateheatmaps(file_path)
