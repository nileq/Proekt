from typing import List, Tuple
import numpy as np
import cv2
from normalize import normalize

def calculate_ball_location_bm(K: List[Tuple], distCoeffs: List[Tuple], f: int, ball_crd: List, edges_crd: List, r_ball: float):
    distCoeffs=np.array(distCoeffs, dtype="double")
    b_array=np.array(ball_crd, dtype="double")
    c_array=np.array(edges_crd, dtype="double")

    #n_b=cv2.undistortPoints(b_array, K, distCoeffs)
    #n_c=cv2.undistortPoints(c_array, K, distCoeffs)
    alpha_c = K[0,1]/K[0,0]
    n_b=normalize(ball_crd, K, distCoeffs, alpha_c)
    n_c=[]
    for pt in edges_crd:
        n_c.append(normalize(pt, K, distCoeffs, alpha_c))
    print(n_b)
    print(n_c[1][1])
    print(n_c[0][1])
    scale=(2*r_ball)/(n_c[1][1]-n_c[0][1])
    print(scale)
    # однородные координаты
    #n_b=ball_crd
    n_b.append(1)
    n_bL=np.array(n_b)*scale

    print(f"Координаты в СК камеры:{n_bL}")
    print(f"Расстояния от центра мяча (мм): {np.linalg.norm(n_bL)}")

if __name__=="__main__":
    Rvec=[]
    Tvec=[]
    #intrinsic params
    K=np.array([[1624.0844036077212, 0.0, 1053.422770793257],
    [0.0, 1619.9896615270884, 749.3158981623625],
    [0.0, 0.0, 1.0]])
    fc=[K[0][0],K[1][1]]
    cc=[K[0][2],K[1][2]]
    alpha_c=K[0][1]/fc[0]
    distCoeffs=[-0.02838259770658771, 0.25180139441913657, -0.0008288106972878879, 0.0028320812997125857, -1.4363561359827697]
    f=28 #mm focal lenght (28mm)

    r_ball=140/(2*3.14)
    d_ball_mm=140/3.14

    #координаты центра мяча
    b=[976,708]
    #координаты крайних точек
    c=[[976,623],[976,778]]

    calculate_ball_location_bm(K, distCoeffs, f, b, c, r_ball)