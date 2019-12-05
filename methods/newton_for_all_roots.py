import math

import numpy as np


def calculate_k(p, p_z, x0):
    for i in range(1, len(p)):
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
    if ck == abs(gamma) and gamma < 0:
        theta = 0.0
    elif ck == abs(gamma) and gamma > 0:
        theta = math.pi / k
    elif ck == abs(delta) and delta < 0:
        theta = math.pi / (2.0 * k)
    elif ck == abs(delta) and delta > 0:
        theta = 3.0 * math.pi / (2.0 * k)
    return theta


def calculate_A(p, p_z, x0):
    maximum = 0.0
    for j in range(len(p) + 2):
        inner = abs(np.polyder(p_z, j)(x0)) / factorial(j)
        if maximum < inner:
            maximum = inner
    return maximum


def calculate_ei(theta):
    ei = complex(math.cos(theta), math.sin(theta))
    return ei


def newton_iteration(p, x, p_z, result):
    x0 = x
    print("the start point is:", x0)
    error = 10 ** 8
    iteration = 0

    while error > 10 ** -6:
        p_z0 = np.polyder(p_z, 0)(x0)
        p_d_z0 = np.polyder(p_z, 1)(x0)
        x1 = x0 - p_z0 / p_d_z0

        p_z1 = np.polyder(p_z, 0)(x1)

        if abs(p_z1) < abs(p_z0):
            # error = abs((x1 - x0))
            error = abs(np.polyder(p_z, 0)(x1) - np.polyder(p_z, 0)(x0))
            x0 = x1
        # use robust newton
        else:
            k = calculate_k(p, p_z, x0)

            p_z0 = np.polyder(p_z, 0)(x0)
            p_k_z0_trans = np.polyder(p_z, k)(x0).conjugate()
            uk = 1.0 / factorial(k) * p_z0 * p_k_z0_trans

            gamma = 2 * (uk ** (k - 1)).real
            delta = -2 * (uk ** (k - 1)).imag
            ck = max(abs(gamma), abs(delta))

            theta = calculate_theta(ck, gamma, delta, k)

            A = calculate_A(p, p_z, x0)

            Ck = ck * (abs(uk) ** (2.0 - k)) / (6.0 * A ** 2)

            ei = calculate_ei(theta)

            if abs(uk) == 0.0:
                Np_x0 = x0
                # break
            else:
                Np_x0 = x0 + Ck / 3.0 * uk / abs(uk) * ei

            # error = abs((Np_x0 - x0))
            error = abs(np.polyder(p_z, 0)(Np_x0) - np.polyder(p_z, 0)(x0))
            x0 = Np_x0
            print("in this iteration we use robust Newton's Method")

        iteration += 1
        result['errors'].append(error)
        print("the error after {} iterations is: {}".format(iteration, error))

    if round(x0.imag, 2) * 1j == 0j:
        result['roots'].append(round(x0.real, 4))
    else:
        result['roots'].append(str(round(x0.real, 4) + round(x0.imag, 4) * 1j).replace("j", "i"))

    print("\nSo after {} iterations, "
          "we get the final result of polynomial: \n\n {} \n\nis: {}".format(iteration, p_z, x0))

    return x0, iteration


def find_all_roots(coefficients, real, imagine):
    print("please input the coefficients of the polynomial: ")
    p = list(map(int, coefficients.split()))
    times = len(p) - 1
    p_z = np.poly1d(p)
    print(p_z)

    print("Input the real part of start point x0: ")
    x = float(real)
    print("Input the imagine part of start point x0: ")
    y = float(imagine)
    point = complex(x, y)
    if x == y:
        y += 0.1
    x = complex(x, y)
    # save result, used for frontend
    result = dict()

    if x.imag == 0j:
        result['start_point'] = x.real
    else:
        result['start_point'] = str(point).replace("j", "i")

    result.update({'roots': []})
    result.update({'steps': []})
    result.update({'errors': []})
    total_iterations = 0

    # 1 -3 3 -3 2 x = 1 + 1i
    while times > 0:
        x0, iteration = newton_iteration(p, x, p_z, result)
        total_iterations += iteration
        p_new = [1, -x0]
        quotient, remainder = np.polydiv(p_z, p_new)
        print(quotient)
        # print(remainder)
        p_z = quotient
        times = times - 1

    result['steps'] = list(range(1, total_iterations + 1))
    result.update({'total_iterations': total_iterations})
    return result


if __name__ == '__main__':
    coefficients = input()
    real = input()
    imagine = input()
    find_all_roots(coefficients, real, imagine)
