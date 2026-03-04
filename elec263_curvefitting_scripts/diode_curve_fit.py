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
    exponent = np.clip(V / (n * V_T), -500, 500)
    return I_0 * (np.exp(exponent) - 1)


def zener_equation(V, I_0, n, I_bv, V_bv, n_bv):
    """Shockley equation with Zener breakdown term.

    I = I_0*(exp(qV/nkT) - 1) - I_bv*exp(-q(V + V_bv)/(n_bv*kT))

    The second term models reverse breakdown: when V approaches -V_bv,
    current surges in the negative direction.
    """
    fwd_exp = np.clip(V / (n * V_T), -500, 500)
    rev_exp = np.clip(-(V + V_bv) / (n_bv * V_T), -500, 500)
    return I_0 * (np.exp(fwd_exp) - 1) - I_bv * np.exp(rev_exp)


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


def detect_zener(V_data, I_data):
    """Detect if the data shows Zener breakdown behavior.

    Breakdown is indicated by large negative currents at negative voltages
    (much larger in magnitude than the small leakage current).
    """
    neg_mask = V_data < -0.1
    if not np.any(neg_mask):
        return False
    I_neg = I_data[neg_mask]
    # Breakdown: current magnitude grows significantly toward more negative V,
    # rather than staying flat like standard reverse saturation.
    # Check if the most-negative current is much larger than the median,
    # or if the data is entirely in the breakdown region (large negative I).
    I_neg_abs = np.abs(I_neg)
    if I_neg_abs.max() > 3 * np.median(I_neg_abs):
        return True
    # All-negative-V data with substantial current suggests breakdown region
    if np.all(V_data < 0) and I_neg_abs.max() > 1e-4:
        return True
    return False


def fit_standard(V_data, I_data):
    """Fit the standard Shockley diode equation."""
    I_0_guess = np.abs(I_data[V_data < 0]).mean() if np.any(V_data < 0) else 1e-12
    p0 = [I_0_guess, 1.5]

    popt, pcov = curve_fit(
        diode_equation, V_data, I_data,
        p0=p0,
        bounds=([0, 0.1], [1e-3, 10]),
        maxfev=10000
    )
    return popt, pcov


def fit_zener(V_data, I_data):
    """Fit the Shockley + breakdown equation for Zener diodes."""
    # Estimate breakdown voltage: where the current magnitude is largest
    # in the negative direction
    idx_min = np.argmin(I_data)
    V_bv_guess = abs(V_data[idx_min])

    # Estimate I_bv scale from breakdown current magnitude
    I_bv_guess = abs(I_data.min()) * 0.01
    # Ensure guess stays within bounds
    I_bv_guess = max(I_bv_guess, 1e-15)

    # V_bv upper bound based on data range
    V_bv_upper = max(abs(V_data.min()), abs(V_data.max())) * 2

    p0 = [1e-12, 1.5, I_bv_guess, V_bv_guess, 5.0]

    popt, pcov = curve_fit(
        zener_equation, V_data, I_data,
        p0=p0,
        bounds=([0, 0.1, 0, 0, 0.1], [1e-1, 50, 1e3, V_bv_upper, 100]),
        maxfev=50000
    )
    return popt, pcov


def main():
    filename = input("Enter the CSV filename (in csv_data/): ").strip()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "csv_data", filename)

    if not os.path.isfile(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    V_data, I_data = load_csv(filepath)

    if len(V_data) < 2:
        print("Not enough data points for fitting.")
        return

    is_zener = detect_zener(V_data, I_data)

    try:
        if is_zener:
            print("Zener breakdown detected — using breakdown model.")
            popt, pcov = fit_zener(V_data, I_data)
            I_0_fit, n_fit, I_bv_fit, V_bv_fit, n_bv_fit = popt
            perr = np.sqrt(np.diag(pcov))

            print(f"\nFitted Parameters:")
            print(f"  I_0   = {I_0_fit:.4e} A   (± {perr[0]:.4e})")
            print(f"  n     = {n_fit:.4f}       (± {perr[1]:.4f})")
            print(f"  I_bv  = {I_bv_fit:.4e} A   (± {perr[2]:.4e})")
            print(f"  V_bv  = {V_bv_fit:.4f} V    (± {perr[3]:.4f})")
            print(f"  n_bv  = {n_bv_fit:.4f}       (± {perr[4]:.4f})")

            fit_func = lambda V: zener_equation(V, *popt)

            eq_text = (
                r"$I = I_0 \left( e^{\frac{qV}{nkT}} - 1 \right)"
                r" - I_{bv}\, e^{\frac{-q(V + V_{bv})}{n_{bv}\,kT}}$"
            )
            param_text = (
                f"$I_0$ = {I_0_fit:.4e} A\n"
                f"$n$ = {n_fit:.4f}\n"
                f"$I_{{bv}}$ = {I_bv_fit:.4e} A\n"
                f"$V_{{bv}}$ = {V_bv_fit:.4f} V\n"
                f"$n_{{bv}}$ = {n_bv_fit:.4f}\n"
                f"$T$ = {T} K"
            )
        else:
            print("Using standard Shockley diode model.")
            popt, pcov = fit_standard(V_data, I_data)
            I_0_fit, n_fit = popt
            perr = np.sqrt(np.diag(pcov))

            print(f"\nFitted Parameters:")
            print(f"  I_0 = {I_0_fit:.4e} A  (± {perr[0]:.4e})")
            print(f"  n   = {n_fit:.4f}      (± {perr[1]:.4f})")

            fit_func = lambda V: diode_equation(V, *popt)

            eq_text = r"$I = I_0 \left( e^{\frac{qV}{nkT}} - 1 \right)$"
            param_text = (
                f"$I_0$ = {I_0_fit:.4e} A\n"
                f"$n$ = {n_fit:.4f}\n"
                f"$T$ = {T} K"
            )
    except RuntimeError as e:
        print(f"Curve fitting failed: {e}")
        return

    # Extend the curve so both forward and reverse regions are visible
    V_min = min(V_data.min(), -0.5)
    V_max = max(V_data.max(), 0.5)
    V_smooth = np.linspace(V_min, V_max, 1000)
    I_smooth = fit_func(V_smooth)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(V_data, I_data, s=8, color='steelblue', alpha=0.7, label='Measured Data')
    ax.plot(V_smooth, I_smooth, 'r-', linewidth=2, label='Fitted Curve')

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
