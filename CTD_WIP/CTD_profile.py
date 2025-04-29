import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date, DateFormatter
import scipy.io as sio
import datetime
import argparse
from cmocean import cm as cmo  # for cmocean colormaps

def daily_profiles(data2plot, first_day, last_day, depths, axis=None, cscale=None):
    """
    Plots a profile given start, end, and depths.

    Args:
        data2plot (str): "temperature", "potential temperature", "density",
                       "potential density", or "salinity".
        first_day (datetime.datetime): Start time limit of the profile.
        last_day (datetime.datetime): End time limit of the profile.
        depths (list or tuple): [shallowest, deepest] depth limits.
        axis (matplotlib.axes._subplots.AxesSubplot, optional): Axis to plot on.
                                                        If None, creates a new figure.
        cscale (list or tuple, optional): [lowest value, highest value] for color scale.
                                    Defaults to 'auto'.
    """

    # Load data
    data = sio.loadmat("MLD.mat")
    MLD = data["MLD"]
    grad_MLD = data["grad_MLD"]

    data_profiles = sio.loadmat("data_profiles.mat")
    conductivity = data_profiles["conductivity"]
    density = data_profiles["density"]
    depth = data_profiles["depth"].flatten()  # Flatten depth to 1D array
    latitude = data_profiles["latitude"]
    longitude = data_profiles["longitude"]
    pdens = data_profiles["pdens"]
    ptemp = data_profiles["ptemp"]
    salinity = data_profiles["salinity"]
    temperature = data_profiles["temperature"]
    time = data_profiles["time"].flatten()  # Flatten time to 1D array

    dates = [num2date(t) for t in time]  # Convert datenum to datetime

    # Find the closest depth indices
    closestIdxmax = np.argmin(np.abs(depth + depths[1]))
    closestIdxmin = np.argmin(np.abs(depth + depths[0]))

    # Define the new depth array
    s_depth = -depth[closestIdxmin:closestIdxmax + 1]  # Invert depth

    # Find the closest time indices
    time_diff_start = [abs(d - first_day) for d in dates]
    idxStart = np.argmin(time_diff_start)
    time_diff_end = [abs(d - last_day) for d in dates]
    idxEnd = np.argmin(time_diff_end)
    s_time = time[idxStart:idxEnd + 1]
    s_dates = dates[idxStart:idxEnd + 1]  # Corresponding datetime objects

    # Select data to plot
    if data2plot == "temperature":
        s_data = temperature[idxStart:idxEnd + 1, closestIdxmin:closestIdxmax + 1].T
        s_MLD = MLD[idxStart:idxEnd + 1, :]
        colorbar_label = "Temperature (°C)"
        cmap = cmo.thermal
    elif data2plot == "potential temperature":
        s_data = ptemp[idxStart:idxEnd + 1, closestIdxmin:closestIdxmax + 1].T
        s_MLD = MLD[idxStart:idxEnd + 1, :]
        colorbar_label = "Potential temperature (°C)"
        cmap = cmo.thermal
    elif data2plot == "density":
        s_data = density[idxStart:idxEnd + 1, closestIdxmin:closestIdxmax + 1].T
        s_MLD = MLD[idxStart:idxEnd + 1, :]
        colorbar_label = "Density (kg/m³)"  # Changed unit
        cmap = cmo.dense
    elif data2plot == "potential density":
        s_data = pdens[idxStart:idxEnd + 1, closestIdxmin:closestIdxmax + 1].T
        s_MLD = MLD[idxStart:idxEnd + 1, :]
        colorbar_label = "Potential density (kg/m³)"  # Changed unit
        cmap = cmo.dense
    elif data2plot == "salinity":
        s_data = salinity[idxStart:idxEnd + 1, closestIdxmin:closestIdxmax + 1].T
        s_MLD = MLD[idxStart:idxEnd + 1, :]
        colorbar_label = "Salinity (psu)"
        cmap = cmo.haline
    else:
        raise ValueError(f"Invalid data2plot: {data2plot}")

    # Plotting
    if axis is None:
        fig, ax = plt.subplots(figsize=(10, 6))  # Create a new figure
    else:
        ax = axis

    c1 = ax.contourf(s_dates, s_depth, s_data, 300, cmap=cmap)  # Use s_dates
    ax.plot(s_dates, -MLD[idxStart:idxEnd + 1, 0], "k-", linewidth=1)  # Use s_dates
    ax.xaxis.set_major_locator(plt.MaxNLocator(7))
    ax.xaxis.set_major_formatter(DateFormatter('%m/%d %H:%M'))
    plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
    ax.set_ylabel("Depth (m)")
    cbar = plt.colorbar(c1, ax=ax)
    cbar.set_label(colorbar_label)

    if depths[1] <= 2.5:
        ax.set_ylim([-depths[1], 0])
    else:
        ax.set_ylim([-depths[1], -depths[0]])
    ax.set_xlim([s_dates[0], s_dates[-1]])  # Use s_dates
    ax.grid(True)
    if cscale:
        c1.set_clim(cscale)

    title_str = f"{data2plot.title()} profile between {s_dates[0].strftime('%d/%m/%Y %H:%M:%S')} and {s_dates[-1].strftime('%d/%m/%Y %H:%M:%S')} within {depths[0]}-{depths[1]} m"
    ax.set_title(title_str)

    # Contour overlay (simplified)
    contour_values = input("Enter contour values (comma-separated) or press Enter for none: ")
    if contour_values:
        contour_values = [float(v.strip()) for v in contour_values.split(",")]
        cbar.set_label(f"{colorbar_label}\nValues for contours: {', '.join(map(str, contour_values))}")
        ax.contour(s_dates, s_depth, s_data, levels=contour_values, colors='k', linestyles='--')

    if axis is None:
        plt.show()  # Show the plot if a new figure was created


if __name__ == '__main__':
    # Example Usage
    parser = argparse.ArgumentParser(description="Plot CTD_WIP profiles")
    parser.add_argument("data2plot", type=str, choices=["temperature", "potential temperature", "density", "potential density", "salinity"], help="Data type to plot")
    parser.add_argument("first_day", type=lambda s: datetime.datetime.strptime(s, "%d-%b-%Y %H:%M:%S"), help="Start date (e.g., 24-Sep-2022 00:00:00)")
    parser.add_argument("last_day", type=lambda s: datetime.datetime.strptime(s, "%d-%b-%Y %H:%M:%S"), help="End date (e.g., 24-Sep-2022 23:59:00)")
    parser.add_argument("depths", type=float, nargs=2, help="Depth limits (e.g., 0 200)")
    parser.add_argument("--cscale", type=float, nargs=2, help="Color scale limits", default=None)
    args = parser.parse_args()

    daily_profiles(args.data2plot, args.first_day, args.last_day, args.depths, cscale=args.cscale)