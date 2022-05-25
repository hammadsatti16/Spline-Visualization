import scipy.interpolate as si
import cv2
import numpy as np

def get_tck_param(annotation):
    for key, values in annotation.items():
            if key =="t":
                t = values
            elif key == "c":
                c = values
            elif key == "k":
                k = values
    return t,c,k

def calculate_spine_params(c,degree,n=100):
    ci = np.asarray(c)
    count = ci.shape[0]
    degree = np.clip(degree,1,count-1)
    # Knot vector
    knot_v = np.array([0]*degree + list(range(count-degree+1)) + [count-degree]*degree,dtype='int')
    # Query range
    query_r = np.linspace(0,(count-degree),n)
    return np.array(si.splev(query_r, (knot_v,ci.T,degree))).T
    
def image_spline(c,degree,img):
    points = np.array(c, np.int32)
    for pt in points:
        cv2.circle(img,(pt[0],pt[1]), 5, (0,255,0), -1)
    points = points.reshape((-1, 1, 2))
    color = (255, 0, 0)
    thickness = 1
    cv2.polylines(img, [points],False, color, thickness,lineType = cv2.LINE_AA)
    p = calculate_spine_params(points,degree)[:,0,:]    
    color = (0, 0, 255)
    thickness = 2
    cv2.polylines(img, [p.astype(np.int32)],False, color, thickness,  lineType = cv2.LINE_AA)
    return img