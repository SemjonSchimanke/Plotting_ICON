import matplotlib.pyplot as plt
import matplotlib.tri as tri
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# --- Load data ---
print("Loading the grid information...")
grid = xr.open_dataset("ICON-DREAM-Global_grid.nc")

# --- Build triangulation ---
# Get coordinates in degrees
print("Compute triangulation...")
lonc = np.rad2deg(grid.clon_vertices.values)
latc = np.rad2deg(grid.clat_vertices.values)

# Build triangulation
# Each cell has 3 vertices, but they are not globally unique — we handle them as independent triangles
ncell = lonc.shape[0]
triangles = np.arange(0, ncell * 3).reshape((ncell, 3))
lon = lonc.flatten()
lat = latc.flatten()

triang = tri.Triangulation(lon, lat, triangles)

# Remove triangles that cross the dateline to avoid artefacts
mask = np.abs(np.diff(lon[triang.triangles], axis=1)).max(axis=1) > 180
triang.set_mask(mask)

# --- Data ---
t2m = ds["t2m"].values - 273.15  #


# --- Plotting ---
print("Start plotting. Global grid.")
fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.triplot(triang, lw=0.2, color="k")

ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS, alpha=0.5)

ax.set_extent([7, 13, 53, 58], crs=ccrs.PlateCarree())
ax.set_title("ICON-DREAM-Global Grid")

fig_name="Global_Grid_example_N_Germany.png"
plt.tight_layout()
plt.savefig(fig_name, dpi=300)
plt.close()  # Close the plot to free memory




# --- Plot T2M ---
INDIR="./"    # Path to your data catalogue
ds = xr.open_dataset(INDIR + "fc_R03B07_rea_ml.2012022302_T2M", engine="cfgrib")

print("Plot temperature.")
fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

# Plot cell-centered field
c = ax.tripcolor(triang, facecolors=t2m, cmap="coolwarm", edgecolors="none", transform=ccrs.PlateCarree(), vmin=0, vmax=10)

# Add coastlines and borders
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS, alpha=0.5)

# Zoom over northern Germany / Denmark
ax.set_extent([7, 13, 53, 58], crs=ccrs.PlateCarree())

# Colorbar
plt.colorbar(c, ax=ax, orientation="vertical", shrink=0.8, label="2 m Temperature [C]")
ax.set_title("T2M, ICON-DREAM-Global Grid")

fig_name="Global_T2M_example_N_Germany.png"
plt.tight_layout()
plt.savefig(fig_name, dpi=300)
plt.close()  # Close the plot to free memory


print("Temperature done.")

