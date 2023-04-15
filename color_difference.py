import math

def degrees(n):
    """
    Converts a value in radians to degrees.
    """
    return (n / math.pi) * 180

def radians(n):
    """
    Converts a value in degrees to radians.
    """
    return (n / 180) * math.pi

def atan2_degrees(y, x):
    """
    Calculates the arctangent of y/x, returning the result in degrees.
    """
    return degrees(math.atan2(y, x))

def cos_degrees(n):
    """
    Calculates the cosine of an angle in degrees.
    """
    return math.cos(radians(n))

def sin_degrees(n):
    """
    Calculates the sine of an angle in degrees.
    """
    return math.sin(radians(n))

def hypot(a, b):
    """
    Calculates the hypotenuse of a right-angled triangle with sides a and b.
    """
    return math.sqrt(a**2 + b**2)

def rgb_to_lab(r, g, b):
    # Convert RGB values to XYZ values
    r_n = r / 255
    g_n = g / 255
    b_n = b / 255

    if r_n > 0.04045:
        r_n = ((r_n + 0.055) / 1.055) ** 2.4
    else:
        r_n = r_n / 12.92

    if g_n > 0.04045:
        g_n = ((g_n + 0.055) / 1.055) ** 2.4
    else:
        g_n = g_n / 12.92

    if b_n > 0.04045:
        b_n = ((b_n + 0.055) / 1.055) ** 2.4
    else:
        b_n = b_n / 12.92

    x = r_n * 0.4124 + g_n * 0.3576 + b_n * 0.1805
    y = r_n * 0.2126 + g_n * 0.7152 + b_n * 0.0722
    z = r_n * 0.0193 + g_n * 0.1192 + b_n * 0.9505

    # Convert XYZ values to LAB values
    x_n = x / 0.95047
    y_n = y / 1.00000
    z_n = z / 1.08883

    if x_n > 0.008856:
        x_n = x_n ** (1/3)
    else:
        x_n = (7.787 * x_n) + (16 / 116)

    if y_n > 0.008856:
        y_n = y_n ** (1/3)
    else:
        y_n = (7.787 * y_n) + (16 / 116)

    if z_n > 0.008856:
        z_n = z_n ** (1/3)
    else:
        z_n = (7.787 * z_n) + (16 / 116)

    l = (116 * y_n) - 16
    a = 500 * (x_n - y_n)
    b = 200 * (y_n - z_n)

    return (l, a, b)


def ciede2000_color_difference(rgb1, rgb2):

    """
    Calculates the CIEDE2000 color difference between two LAB colors.
    """
    R1, G1, B1 = rgb1
    R2, G2, B2 = rgb2

    L1, a1, b1 = rgb_to_lab(R1, G1, B1)
    L2, a2, b2 = rgb_to_lab(R2, G2, B2)

    # Calculate the chroma and hue differences
    C1 = hypot(a1, b1)
    C2 = hypot(a2, b2)
    C_avg = (C1 + C2) / 2

    G = 0.5 * (1 - math.sqrt((C_avg**7) / ((C_avg**7) + (25**7))))

    a1_p = (1 + G) * a1
    a2_p = (1 + G) * a2

    C1_p = hypot(a1_p, b1)
    C2_p = hypot(a2_p, b2)

    h1_p = atan2_degrees(b1, a1_p)
    h2_p = atan2_degrees(b2, a2_p)

    delta_L_p = L2 - L1
    delta_C_p = C2_p - C1_p

    h_diff_p = h2_p - h1_p

    if C1_p * C2_p == 0:
        h_diff_p = 0
    elif abs(h_diff_p) <= 180:
        pass
    elif h_diff_p > 180:
        h_diff_p -= 360
    else:
        h_diff_p += 360

    delta_H_p = 2 * math.sqrt(C1_p * C2_p) * sin_degrees(h_diff_p / 2)

    L_avg_p = (L1 + L2) / 2
    C_avg_p = (C1_p + C2_p) / 2

    h_avg_p = 0
    if C1_p * C2_p != 0:
        if abs(h_diff_p) <= 180:
            h_avg_p = (h1_p + h2_p) / 2
        elif h1_p + h2_p < 360:
            h_avg_p = (h1_p + h2_p + 360) / 2
        else:
            h_avg_p = (h1_p + h2_p - 360) / 2

    T = 1 - 0.17 * cos_degrees(h_avg_p - 30) + 0.24 * cos_degrees(2 * h_avg_p) + 0.32 * cos_degrees(3 * h_avg_p + 6) - 0.2 * cos_degrees(4 * h_avg_p - 63)

    delta_theta_p = 30 * math.exp(-((h_avg_p - 275) / 25)**2)

    R_C = 2 * math.sqrt((C_avg_p**7) / ((C_avg_p**7) + (25**7)))

    S_L = 1 + (0.015 * (L_avg_p - 50)**2) / math.sqrt(20 + (L_avg_p - 50)**2)
    S_C = 1 + 0.045 * C_avg_p
    S_H = 1 + 0.015 * C_avg_p * T

    R_T = -sin_degrees(2 * delta_theta_p) * R_C

    # Calculate the final CIEDE2000 delta E value
    delta_L_p = delta_L_p / S_L
    delta_C_p = delta_C_p / S_C
    delta_H_p = delta_H_p / S_H

    delta_E_p = hypot(delta_L_p, delta_C_p)

    h_diff_p = abs(h_diff_p)
    if C1_p * C2_p != 0:
        if h_diff_p <= 180:
            delta_H_p = delta_H_p
        elif h_diff_p > 180 and h_avg_p <= 360:
            delta_H_p = delta_H_p - 360
        elif h_diff_p > 180 and h_avg_p > 360:
            delta_H_p = delta_H_p + 360

    delta_H_p = 2 * math.sqrt(C1_p * C2_p) * sin_degrees(delta_H_p / 2)

    delta_E_p = math.sqrt(delta_L_p**2 + delta_C_p**2 + delta_H_p**2 + R_T * delta_C_p * delta_H_p)

    return delta_E_p

if __name__ == '__main__':
    color1 = (255, 255, 255)
    color2 = (255, 114, 100)

    print(color1)
    print(color2)
    print(ciede2000_color_difference(color1, color2))


