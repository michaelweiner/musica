import numpy as np
import scipy.io


def corr2_coeff(A, B):
    # https://stackoverflow.com/questions/30143417/computing-the-correlation-coefficient-between-two-multi-dimensional-arrays/30143754#30143754
    # Rowwise mean of input arrays & subtract from input arrays themeselves
    A_mA = A - A.mean(1)[:, None]
    B_mB = B - B.mean(1)[:, None]

    # Sum of squares across rows
    ssA = (A_mA**2).sum(1)
    ssB = (B_mB**2).sum(1)

    # Finally get corr coeff
    return np.dot(A_mA, B_mB.T)/np.sqrt(np.dot(ssA[:, None], ssB[None]))


def corr2_big(window_rolling, ref_rolling, max_window_size=5000):
    ref_rolling_matrix = ref_rolling.reshape(ref_rolling.shape[-1], 1)
    correlations = np.zeros(window_rolling.shape[-1]-ref_rolling.shape[-1]+1)
    for subsubwindow in range(0,
                              window_rolling.shape[-1]-ref_rolling.shape[-1]+1,
                              max_window_size):
        subwindow_rolling = window_rolling[subsubwindow:subsubwindow
                                           + max_window_size
                                           + ref_rolling.shape[-1]-1]
        sliding_window_matrix = np.lib.stride_tricks.sliding_window_view(
            subwindow_rolling, ref_rolling.shape[-1])
        sliding_correlation = corr2_coeff(ref_rolling_matrix.T,
                                          sliding_window_matrix)[0]
        correlations[subsubwindow:subsubwindow +
                     sliding_correlation.shape[-1]] = sliding_correlation
    return correlations


def load_single_trace(filename, varname="trace"):
    if filename.endswith(".mat"):
        matfile = scipy.io.loadmat(filename)
        trace = matfile[varname].flatten()
    else:
        trace = np.load(filename)
    return trace
