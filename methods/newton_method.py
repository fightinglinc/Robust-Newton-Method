import math

import numpy as np


def calculate_k(p, p_z, x0):
    for i in range(1, len(p) + 1):
        k = np.polyder(p_z, i)(x0)
        if k != 0:
            break
    return i


def factorial(num):
    start = 1

    if num == 0:
        end = 1
    else:
        for i in range(1, num + 1):
            start = start * i
        end = start
    return end


def calculate_theta(ck, gamma, delta, k):
    theta = 0
    if ck == abs(gamma) and gamma < 0:
        theta = 0
    elif ck == abs(gamma) and gamma > 0:
        theta = math.pi / k
    elif ck == abs(delta) and delta < 0:
        theta = math.pi / (2 * k)
    elif ck == abs(delta) and delta > 0:
        theta = 3 * math.pi / (2 * k)
    return theta


def calculate_A(p, p_z, x0):
    maximum = 0
    for j in range(len(p) + 2):
        inner = abs(np.polyder(p_z, j)(x0)) / factorial(j)
        if maximum < inner:
            maximum = inner
    return maximum


def calculate_ei(theta):
    ei = complex(math.cos(theta) + math.sin(theta))
    return ei


def main(coefficients, real_part, imagine_part):
    result = {}
    flag = False
    print("please input the coefficients of the polynomial: ")
    # p = list(map(int, input().split()))
    p = list(map(int, coefficients.split()))
    p_z = np.poly1d(p)
    print(p_z)

    print("Input the real part of start point x0: ")
    # x = float(input())
    x = float(real_part)
    print("Input the imagine part of start point x0: ")
    # y = float(input())
    y = float(imagine_part)
    x = complex(x, y)

    x0 = x
    print("the start point is:", x0)

    if x0.imag == 0j:
        result['start_point'] = x0.real
    else:
        result['start_point'] = str(x0).replace("j", "i")

    error = 10 ** 8
    iteration = 0
    while error > 10 ** -6:
        p_z0 = np.polyder(p_z, 0)(x0)
        # print("p_z0", p_z0)
        p_d_z0 = np.polyder(p_z, 1)(x0)
        # print("p_d_z0", p_d_z0)
        x1 = x0 - p_z0 / p_d_z0
        print("x1", x1)

        p_z1 = np.polyder(p_z, 0)(x1)

        if abs(p_z1) < abs(p_z0):
            error = abs((x1 - x0).real)
            x0 = x1
        # use robust newton
        else:
            flag = True
            k = calculate_k(p, p_z, x0)

            p_z0 = np.polyder(p_z, 0)(x0)
            p_k_z0_trans = np.polyder(p_z, k)(x0).conjugate()
            uk = 1 / factorial(k) * p_z0 * p_k_z0_trans

            gamma = 2 * (uk ** (k - 1)).real
            delta = -2 * (uk ** (k - 1)).imag
            ck = max(abs(gamma), abs(delta))

            theta = calculate_theta(ck, gamma, delta, k)

            A = calculate_A(p, p_z, x0)

            Ck = ck * (abs(uk) ** (2 - k)) / (6 * A ** 2)

            ei = calculate_ei(theta)

            if abs(uk) == 0:
                Np_x0 = x0
                break
            else:
                Np_x0 = x0 + Ck / 3 * uk / abs(uk) * ei

            error = abs((Np_x0 - x0).real)
            x0 = Np_x0
            print("in this iteration we use robust Newton's Method")

        iteration += 1
        print("the error after {} iterations is: {}".format(iteration, error))

    print("\nSo after {} iterations, we get the final result of polynomial: \n\n {} \n\nis: {}".format(iteration, p_z,
                                                                                                       x0))
    result['iteration'] = iteration
    result['flag'] = flag
    # result['error'] = error

    if round(x0.imag, 2) * 1j == 0j:
        result['root'] = round(x0.real, 2)
    else:
        result['root'] = str(round(x0.real, 4) + round(x0.imag, 4) * 1j).replace("j", "i")

    return result


if __name__ == '__main__':
    coefficients = input()
    real = input()
    imagine = input()
    main(coefficients, real, imagine)
