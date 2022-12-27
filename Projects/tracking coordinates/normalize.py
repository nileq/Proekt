import numpy as np


def comp_distortion(x_dist, rad_dist):
    radius_2 = x_dist[0] ** 2 + x_dist[1] ** 2
    radial_distortion = 1 + (k2 * radius_2)
    radius_2_comp = (x_dist[0] ** 2 + x_dist[1] ** 2) / radial_distortion
    radial_distortion = 1 + (k2 * radius_2_comp)
    x_comp[0] = x_dist[0] / radial_distortion
    x_comp[1] = x_dist[1] / radial_distortion

    return x_comp


def comp_normalize_oulu(x_crd, dist_coeffs):
    if len(dist_coeffs) == 1:
        x_undistorted = comp_distortion(x_crd, dist_coeffs)
    else:
        k1 = dist_coeffs[0]
        k2 = dist_coeffs[1]
        k3 = dist_coeffs[4]
        p1 = dist_coeffs[2]
        p2 = dist_coeffs[3]

        x_undistorted = x_crd.copy()

        for i in range(20):
            r_2 = np.sum(x_crd[0] ** 2 + x_crd[1] ** 2)
            k_radial = 1 + k1 * r_2 + k2 * r_2 ** 2 + k3 * r_2 ** 3
            delta_x = [2 * p1 * x_undistorted[0] * x_undistorted[1] + p2 * (r_2 + 2 * x_undistorted[0] ** 2),
                       p1 * (r_2 + 2 * x_undistorted[1] ** 2) + 2 * p2 * x_undistorted[0] * x_undistorted[1]]
            x_undistorted[0] = (x_crd[0] - delta_x[0]) / k_radial
            x_undistorted[1] = (x_crd[1] - delta_x[1]) / k_radial

        return x_undistorted


def normalize(x_crd, K, dist_coeffs, alpha_c):
    fc = [K[0, 0], K[1, 1]]
    cc = [K[0, 2], K[1, 2]]

    x_distort = [(x_crd[0] - cc[0]) / fc[0], (x_crd[1] - cc[1]) / fc[1]]

    x_distort[0] = x_distort[0] - alpha_c * x_distort[1]

    if np.linalg.norm(dist_coeffs) != 0:
        x_norm = comp_normalize_oulu(x_distort, dist_coeffs)
    else:
        x_norm = x_distort

    return x_norm