import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LinearSegmentedColormap
import io
from matplotlib.animation import PillowWriter

import logging

# Set up logging configuration to show only warnings and errors
#logging.basicConfig(level=logging.WARNING)
#logging.getLogger('fiona').setLevel(logging.WARNING)
#logging.getLogger('matplotlib').setLevel(logging.WARNING)

def create_animation(ds, custom_locations):
    lats = ds['lat'].values
    lons = ds['lon'].values
    data = ds['SIS'].values  # Assuming shape is (num_hours, lat, lon)
    times = ds['time'].values

    integer_lats_indices = np.where(np.isclose(lats % 1, 0, atol=0.01))[0]
    integer_lons_indices = np.where(np.isclose(lons % 1, 0, atol=0.01))[0]
    integer_lats = lats[integer_lats_indices]
    integer_lons = lons[integer_lons_indices]

    reference_locations = [
        (52.5200, 13.4050, 'Berlin'),
        (48.1351, 11.5820, 'Munich'),
        (53.5511, 9.9937, 'Hamburg'),
        (50.1109, 8.6821, 'Frankfurt'),
        (48.7758, 9.1829, 'Stuttgart'),
        (49.7913, 9.9534, 'Würzburg'),
        (51.3127, 9.4797, 'Kassel'),
        (50.9375, 6.9603, 'Köln'),   # Cologne
        (51.0504, 13.7373, 'Dresden')   # Dresden
    ]

    colors = [
        (0.0, 'blue'),
        (0.1, 'cyan'),
        (0.3, 'green'),
        (0.5, 'yellow'),
        (0.7, 'orange'),
        (0.9, 'red'),
        (1.0, 'firebrick')
    ]
    cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)

    fig, ax = plt.subplots(figsize=(14, 14), subplot_kw={'projection': ccrs.PlateCarree()})
    extent = [lons.min(), lons.max(), lats.min(), lats.max()]
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    mesh = ax.pcolormesh(lons, lats, data[0], cmap=cmap, shading='auto', vmin=0, vmax=1000)

    ax.add_feature(cfeature.BORDERS, linestyle='-')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    for lat, lon, name in reference_locations:
        ax.plot(lon, lat, marker='*', color='blue', markersize=8, transform=ccrs.PlateCarree())
        ax.text(lon, lat, name, fontsize=8, transform=ccrs.PlateCarree(), verticalalignment='top')

    for loc in custom_locations:
        lat, lon = loc['lat'], loc['lon']
        ax.plot(lon, lat, marker='^', color='red', markersize=8, markeredgecolor='black', transform=ccrs.PlateCarree())

    color_bar = fig.colorbar(mesh, ax=ax, orientation='vertical', pad=0.01,aspect=70, shrink=0.8)
    color_bar.set_label('SIS [W/m2]', fontsize=14)

    ax.set_xlabel('Longitude',fontsize=16)
    ax.set_ylabel('Latitude',fontsize=16)
    ax.set_xticks(integer_lons)
    ax.set_xticklabels(np.round(integer_lons, 2), rotation=45, ha="right")
    ax.set_yticks(integer_lats)
    ax.set_yticklabels(np.round(integer_lats, 2))

    #forecast_hour_title = fig.suptitle('Forecast Hour: 0', fontsize=16, y=0.95)
    fc_const_str = 'Forecast Hour: '
    time_const_str = '    UTC Time: '
    combined_text = fc_const_str + '0' + time_const_str + str(times[0])
    time_title = fig.text(0.65, 0.9, combined_text, ha='right', fontsize=18)

    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_label_position('bottom')

    # Adjust margins to minimize space on the left, right, top, and bottom
    plt.subplots_adjust(left=0.05, top=0.95, right=0.99, bottom=0.01)
    plt.tight_layout()

    def update(hour):
        mesh.set_array(data[hour].ravel())
        #forecast_hour_title.set_text(f'Forecast Hour: {hour}')
        combined_text = fc_const_str + str(hour) + time_const_str + str(times[hour])
        time_title.set_text(combined_text)

    ani = animation.FuncAnimation(fig, update, frames=data.shape[0], interval=2000, repeat=True)

    buffer = io.BytesIO()
    ani.save("forecast_animation.gif", writer=PillowWriter(fps=0.5))
    with open("forecast_animation.gif", "rb") as f:
        buffer.write(f.read())
    buffer.seek(0)

    plt.close(fig)  # Close the figure to free up resources
    return buffer
