import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# Constants
q = 1.602176634e-19   # Elementary charge (C)
k = 1.380649e-23      # Boltzmann constant (J/K)
T = 298.15             # Room temperature (K)
V_T = k * T / q        # Thermal voltage (~25.7 mV)


def diode_equation(V, I_0, n):
    """Shockley diode equation: I = I_0 * (exp(qV / nkT) - 1)"""
    return I_0 * (np.exp(V / (n * V_T)) - 1)


def load_csv(filepath):
    """Load voltage and current data from a WaveForms CSV file."""
    voltage = []
    current = []

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comment/header lines
            if line.startswith('#') or line == '':
                continue
            # Skip column header line
            if line.startswith('V'):
                continue
            parts = line.split(',')
            voltage.append(float(parts[0]))
            current.append(float(parts[1]))

    return np.array(voltage), np.array(current)


def main():
    filename = input("Enter the CSV filename (in csv_data/): ").strip()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "csv_data", filename)

    if not os.path.isfile(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    V_data, I_data = load_csv(filepath)

    # Use only forward-bias data (V > 0) for fitting since the exponential
    # behavior of the diode equation is dominant there.
    mask = V_data > 0
    V_fit = V_data[mask]
    I_fit = I_data[mask]

    if len(V_fit) < 2:
        print("Not enough forward-bias data points for fitting.")
        return

    # Initial guesses: I_0 ~ small leakage current, n ~ 1-2
    p0 = [1e-12, 1.5]

    try:
        popt, pcov = curve_fit(
            diode_equation, V_fit, I_fit,
            p0=p0,
            bounds=([0, 0.1], [1e-3, 10]),
            maxfev=10000
        )
    except RuntimeError as e:
        print(f"Curve fitting failed: {e}")
        return

    I_0_fit, n_fit = popt
    perr = np.sqrt(np.diag(pcov))

    print(f"\nFitted Parameters:")
    print(f"  I_0 = {I_0_fit:.4e} A  (± {perr[0]:.4e})")
    print(f"  n   = {n_fit:.4f}      (± {perr[1]:.4f})")

    # Generate smooth curve for plotting
    V_smooth = np.linspace(V_fit.min(), V_fit.max(), 500)
    I_smooth = diode_equation(V_smooth, I_0_fit, n_fit)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(V_data, I_data, s=8, color='steelblue', alpha=0.7, label='Measured Data')
    ax.plot(V_smooth, I_smooth, 'r-', linewidth=2, label='Fitted Curve')

    # Build equation and parameter text
    eq_text = r"$I = I_0 \left( e^{\frac{qV}{nkT}} - 1 \right)$"
    param_text = (
        f"$I_0$ = {I_0_fit:.4e} A\n"
        f"$n$   = {n_fit:.4f}\n"
        f"$T$   = {T} K"
    )

    ax.text(
        0.05, 0.95, eq_text + "\n\n" + param_text,
        transform=ax.transAxes, fontsize=11,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    )

    ax.set_xlabel('Voltage (V)', fontsize=12)
    ax.set_ylabel('Current (A)', fontsize=12)
    ax.set_title(f'Diode I-V Curve Fit — {filename}', fontsize=14)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
