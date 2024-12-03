import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import seaborn as sns

def generate_combined_amenities_heatmap(file_path):
    # Load data from the input file
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()

    # Extract unique amenity types and assign colors
    unique_types = data['type'].unique()
    colors = sns.color_palette("husl", len(unique_types))
    color_map = {amenity: color for amenity, color in zip(unique_types, colors)}

    # Create a grid for interpolation
    x = data['x']
    y = data['y']
    grid_x, grid_y = np.mgrid[0:x.max():100j, 0:y.max():100j]

    # Initialize a blank grid for combined heatmap
    combined_grid = np.zeros_like(grid_x, dtype=float)

    plt.figure(figsize=(12, 10))

    # Generate and overlay heatmaps for each amenity type
    for amenity_type in unique_types:
        # Subset data for the current amenity type
        subset = data[data['type'] == amenity_type]

        # Check if the subset has enough unique points for interpolation
        if len(subset['x'].unique()) < 2 or len(subset['y'].unique()) < 2:
            print(f"Skipping interpolation for {amenity_type} due to insufficient spatial variance.")
            continue

        # Interpolate density values
        density_values = np.ones(len(subset))
        grid_values = griddata((subset['x'], subset['y']), density_values, (grid_x, grid_y), method='cubic')

        # Normalize the values and overlay them on the combined grid
        normalized_grid = np.nan_to_num(grid_values / np.nanmax(grid_values))
        combined_grid += normalized_grid * (unique_types.tolist().index(amenity_type) + 1)

        # Overlay contours for visual clarity
        plt.contour(grid_x, grid_y, normalized_grid, levels=5, colors=[color_map[amenity_type]], alpha=0.8, linewidths=1)

    # Display the combined grid as a heatmap
    plt.contourf(grid_x, grid_y, combined_grid, cmap='rainbow', levels=50)
    plt.colorbar(label='Amenity Density (Gradient)')
    plt.title('Spatial Gradient Heatmap of Amenities')
    plt.xlabel('X Coordinates')
    plt.ylabel('Y Coordinates')
    plt.tight_layout()

    # Save and show the heatmap
    plt.savefig('combined_amenities_heatmap.png')
    plt.show()

if __name__ == "__main__":
    file_path = "ammap.txt"  # Adjust this filename if needed
    generate_combined_amenities_heatmap(file_path)
