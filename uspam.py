import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import seaborn as sns

def generatecombinedamenitiesheatmap(file_path):
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()
    unique_types = data['type'].unique()
    colors = sns.color_palette("husl", len(unique_types))
    color_map = {amenity: color for amenity, color in zip(unique_types, colors)}
    x = data['x']
    y = data['y']
    grid_x, grid_y = np.mgrid[0:x.max():100j, 0:y.max():100j]

    
    combined_grid = np.zeros_like(grid_x, dtype=float)
    plt.figure(figsize=(12, 10))

    
    for amenity_type in unique_types:
        
        subset = data[data['type'] == amenity_type]

        
        if len(subset['x'].unique()) < 2 or len(subset['y'].unique()) < 2:
            print(f"Skipping interpolation for {amenity_type} due to insufficient spatial variance.")
            continue

        
        density_values = np.ones(len(subset))
        grid_values = griddata((subset['x'], subset['y']), density_values, (grid_x, grid_y), method='cubic')

        
        normalized_grid = np.nan_to_num(grid_values / np.nanmax(grid_values))
        combined_grid += normalized_grid * (unique_types.tolist().index(amenity_type) + 1)

        
        plt.contour(grid_x, grid_y, normalized_grid, levels=5, colors=[color_map[amenity_type]], alpha=0.8, linewidths=1)

    
    plt.contourf(grid_x, grid_y, combined_grid, cmap='rainbow', levels=50)
    plt.colorbar(label='Amenity Density (Gradient)')
    plt.title('Spatial Gradient Heatmap of Amenities')
    plt.xlabel('X Coordinates')
    plt.ylabel('Y Coordinates')
    plt.tight_layout()
    plt.savefig('combined_amenities_heatmap.png')
    plt.show()

if __name__ == "__main__":
    file_path = "ammap.txt" 
    generatecombinedamenitiesheatmap(file_path)
