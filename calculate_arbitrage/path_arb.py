import numpy as np
import time
from math import sqrt

# [minzzii]
# x->y->x' ; path = [x,y,x']
# (x+0.997dx)(y-dy)=xy
# (y'+0.997dy)(x'-dx')=y'x'
# find optimal dx s.t max(dx'-dx)
# dx'= x'*r*dy / y'+rdy
# => dx' = (Eb*r*dx) / (Ea + rdx), where Ea = r*y*x'/y'+yr, Eb = x*y'/y'+yr
# dx = (sqrt(Ea)sqrt(Eb)sqrt(r)-Ea)/r


# [minzzii]
# token0 -> token1 swap
# R_in : Reserved amount of token0
# R_out : Reserved amount of token1
# d_in : optimal input amount of token0
# (R_in + 0.997*d_in)(R_out-d_out) = R_in*R_out
# => d_out = R_out - ((R_in * R_out) / (R_in + (0.997 * d_in)))
def cp_amm_out(R_in, R_out, d_in):
    return R_out - ((R_in * R_out) / (R_in + (0.997 * d_in)))


def fast_path_two_arb(R_in_0, R_out_0, R_in_1, R_out_1):
    solution1 = 1.00300902708124*(997000000.0*sqrt(R_in_0)*sqrt(R_in_1)*sqrt(R_out_0)*sqrt(R_out_1)*(R_in_1 + 0.997*R_out_0)**2 - 1000.0*R_in_0*R_in_1*(
        1000000.0*R_in_1**2 + 1994000.0*R_in_1*R_out_0 + 994009.0*R_out_0**2))/((1000.0*R_in_1 + 997.0*R_out_0)*(1000000.0*R_in_1**2 + 1994000.0*R_in_1*R_out_0 + 994009.0*R_out_0**2))
    solution2 = -0.00100300902708124*(997000000000.0*sqrt(R_in_0)*sqrt(R_in_1)*sqrt(R_out_0)*sqrt(R_out_1)*(R_in_1 + 0.997*R_out_0)**2 + 1000.0*R_in_0*R_in_1*(
        1000000.0*R_in_1**2 + 1994000.0*R_in_1*R_out_0 + 994009.0*R_out_0**2))/((1000.0*R_in_1 + 997.0*R_out_0)*(1000000.0*R_in_1**2 + 1994000.0*R_in_1*R_out_0 + 994009.0*R_out_0**2))

    d_in_0 = max(solution1, solution2)

    if d_in_0 > 0:
        between_lp_amts = [d_in_0]
        between_lp_amts.append(cp_amm_out(
            R_in_0, R_out_0, between_lp_amts[-1]))
        between_lp_amts.append(cp_amm_out(
            R_in_1, R_out_1, between_lp_amts[-1]))

        profit = max(between_lp_amts[-1] - d_in_0, 0)

        return d_in_0, profit, between_lp_amts
    else:
        return 0, 0, None


def fast_path_three_arb(R_in_0, R_out_0, R_in_1, R_out_1, R_in_2, R_out_2):
    solution1 = 10.0300902708124*(9.95503376689401e+16*sqrt(R_in_0)*sqrt(R_in_1)*sqrt(R_in_2)*sqrt(R_out_0)*sqrt(R_out_1)*sqrt(R_out_2)*(R_in_1*R_in_2 + 0.997*R_in_2*R_out_0 + 0.994009*R_out_0*R_out_1)**2 - 100000.0*R_in_0*R_in_1*R_in_2*(1000000000000.0*R_in_1**2*R_in_2**2 + 1994000000000.0*R_in_1*R_in_2**2*R_out_0 + 1988018000000.0*R_in_1*R_in_2*R_out_0*R_out_1 + 994009000000.0*R_in_2**2*R_out_0**2 + 1982053946000.0 *
                                  R_in_2*R_out_0**2*R_out_1 + 988053892081.0*R_out_0**2*R_out_1**2))/((1000000.0*R_in_1*R_in_2 + 997000.0*R_in_2*R_out_0 + 994009.0*R_out_0*R_out_1)*(1000000000000.0*R_in_1**2*R_in_2**2 + 1994000000000.0*R_in_1*R_in_2**2*R_out_0 + 1988018000000.0*R_in_1*R_in_2*R_out_0*R_out_1 + 994009000000.0*R_in_2**2*R_out_0**2 + 1982053946000.0*R_in_2*R_out_0**2*R_out_1 + 988053892081.0*R_out_0**2*R_out_1**2))

    solution2 = -0.00100300902708124*(9.95503376689401e+20*sqrt(R_in_0)*sqrt(R_in_1)*sqrt(R_in_2)*sqrt(R_out_0)*sqrt(R_out_1)*sqrt(R_out_2)*(R_in_1*R_in_2 + 0.997*R_in_2*R_out_0 + 0.994009*R_out_0*R_out_1)**2 + 1000000000.0*R_in_0*R_in_1*R_in_2*(1000000000000.0*R_in_1**2*R_in_2**2 + 1994000000000.0*R_in_1*R_in_2**2*R_out_0 + 1988018000000.0*R_in_1*R_in_2*R_out_0*R_out_1 + 994009000000.0*R_in_2**2*R_out_0**2 +
                                      1982053946000.0*R_in_2*R_out_0**2*R_out_1 + 988053892081.0*R_out_0**2*R_out_1**2))/((1000000.0*R_in_1*R_in_2 + 997000.0*R_in_2*R_out_0 + 994009.0*R_out_0*R_out_1)*(1000000000000.0*R_in_1**2*R_in_2**2 + 1994000000000.0*R_in_1*R_in_2**2*R_out_0 + 1988018000000.0*R_in_1*R_in_2*R_out_0*R_out_1 + 994009000000.0*R_in_2**2*R_out_0**2 + 1982053946000.0*R_in_2*R_out_0**2*R_out_1 + 988053892081.0*R_out_0**2*R_out_1**2))

    d_in_0 = max(solution1, solution2)

    if d_in_0 > 0:
        between_lp_amts = [d_in_0]
        between_lp_amts.append(cp_amm_out(
            R_in_0, R_out_0, between_lp_amts[-1]))
        between_lp_amts.append(cp_amm_out(
            R_in_1, R_out_1, between_lp_amts[-1]))
        between_lp_amts.append(cp_amm_out(
            R_in_2, R_out_2, between_lp_amts[-1]))

        profit = max(between_lp_amts[-1] - d_in_0, 0)

        return d_in_0, profit, between_lp_amts
    else:
        return 0, 0, None


def fast_path_four_arb(R_in_0, R_out_0, R_in_1, R_out_1, R_in_2, R_out_2, R_in_3, R_out_3):
    solution1 = 1003.00902708124*(9.94009e+23*sqrt(R_in_0)*sqrt(R_in_1)*sqrt(R_in_2)*sqrt(R_in_3)*sqrt(R_out_0)*sqrt(R_out_1)*sqrt(R_out_2)*sqrt(R_out_3)*(R_in_1*R_in_2*R_in_3 + 0.997*R_in_2*R_in_3*R_out_0 + 0.994009*R_in_3*R_out_0*R_out_1 + 0.991026973*R_out_0*R_out_1*R_out_2)**2 - 1000000.0*R_in_0*R_in_1*R_in_2*R_in_3*(1.0e+18*R_in_1**2*R_in_2**2*R_in_3**2 + 1.994e+18*R_in_1*R_in_2**2*R_in_3**2*R_out_0 + 1.988018e+18*R_in_1*R_in_2*R_in_3**2*R_out_0*R_out_1 + 1.982053946e+18*R_in_1*R_in_2*R_in_3*R_out_0*R_out_1*R_out_2 + 9.94009e+17*R_in_2**2*R_in_3**2*R_out_0**2 + 1.982053946e+18*R_in_2*R_in_3**2*R_out_0**2*R_out_1 + 1.976107784162e+18*R_in_2*R_in_3*R_out_0**2*R_out_1*R_out_2 + 9.88053892081e+17*R_in_3**2*R_out_0**2*R_out_1**2 + 1.97017946080951e+18*R_in_3*R_out_0 **
                                  2*R_out_1**2*R_out_2 + 9.82134461213543e+17*R_out_0**2*R_out_1**2*R_out_2**2))/((1000000000.0*R_in_1*R_in_2*R_in_3 + 997000000.0*R_in_2*R_in_3*R_out_0 + 994009000.0*R_in_3*R_out_0*R_out_1 + 991026973.0*R_out_0*R_out_1*R_out_2)*(1.0e+18*R_in_1**2*R_in_2**2*R_in_3**2 + 1.994e+18*R_in_1*R_in_2**2*R_in_3**2*R_out_0 + 1.988018e+18*R_in_1*R_in_2*R_in_3**2*R_out_0*R_out_1 + 1.982053946e+18*R_in_1*R_in_2*R_in_3*R_out_0*R_out_1*R_out_2 + 9.94009e+17*R_in_2**2*R_in_3**2*R_out_0**2 + 1.982053946e+18*R_in_2*R_in_3**2*R_out_0**2*R_out_1 + 1.976107784162e+18*R_in_2*R_in_3*R_out_0**2*R_out_1*R_out_2 + 9.88053892081e+17*R_in_3**2*R_out_0**2*R_out_1**2 + 1.97017946080951e+18*R_in_3*R_out_0**2*R_out_1**2*R_out_2 + 9.82134461213543e+17*R_out_0**2*R_out_1**2*R_out_2**2))

    solution2 = -0.00100300902708124*(9.94009e+29*sqrt(R_in_0)*sqrt(R_in_1)*sqrt(R_in_2)*sqrt(R_in_3)*sqrt(R_out_0)*sqrt(R_out_1)*sqrt(R_out_2)*sqrt(R_out_3)*(R_in_1*R_in_2*R_in_3 + 0.997*R_in_2*R_in_3*R_out_0 + 0.994009*R_in_3*R_out_0*R_out_1 + 0.991026973*R_out_0*R_out_1*R_out_2)**2 + 1000000000000.0*R_in_0*R_in_1*R_in_2*R_in_3*(1.0e+18*R_in_1**2*R_in_2**2*R_in_3**2 + 1.994e+18*R_in_1*R_in_2**2*R_in_3**2*R_out_0 + 1.988018e+18*R_in_1*R_in_2*R_in_3**2*R_out_0*R_out_1 + 1.982053946e+18*R_in_1*R_in_2*R_in_3*R_out_0*R_out_1*R_out_2 + 9.94009e+17*R_in_2**2*R_in_3**2*R_out_0**2 + 1.982053946e+18*R_in_2*R_in_3**2*R_out_0**2*R_out_1 + 1.976107784162e+18*R_in_2*R_in_3*R_out_0**2*R_out_1*R_out_2 + 9.88053892081e+17*R_in_3**2*R_out_0**2*R_out_1**2 + 1.97017946080951e+18*R_in_3 *
                                      R_out_0**2*R_out_1**2*R_out_2 + 9.82134461213543e+17*R_out_0**2*R_out_1**2*R_out_2**2))/((1000000000.0*R_in_1*R_in_2*R_in_3 + 997000000.0*R_in_2*R_in_3*R_out_0 + 994009000.0*R_in_3*R_out_0*R_out_1 + 991026973.0*R_out_0*R_out_1*R_out_2)*(1.0e+18*R_in_1**2*R_in_2**2*R_in_3**2 + 1.994e+18*R_in_1*R_in_2**2*R_in_3**2*R_out_0 + 1.988018e+18*R_in_1*R_in_2*R_in_3**2*R_out_0*R_out_1 + 1.982053946e+18*R_in_1*R_in_2*R_in_3*R_out_0*R_out_1*R_out_2 + 9.94009e+17*R_in_2**2*R_in_3**2*R_out_0**2 + 1.982053946e+18*R_in_2*R_in_3**2*R_out_0**2*R_out_1 + 1.976107784162e+18*R_in_2*R_in_3*R_out_0**2*R_out_1*R_out_2 + 9.88053892081e+17*R_in_3**2*R_out_0**2*R_out_1**2 + 1.97017946080951e+18*R_in_3*R_out_0**2*R_out_1**2*R_out_2 + 9.82134461213543e+17*R_out_0**2*R_out_1**2*R_out_2**2))

    d_in_0 = max(solution1, solution2)

    if d_in_0 > 0:
        between_lp_amts = [d_in_0]
        between_lp_amts.append(cp_amm_out(
            R_in_0, R_out_0, between_lp_amts[-1]))
        between_lp_amts.append(cp_amm_out(
            R_in_1, R_out_1, between_lp_amts[-1]))
        between_lp_amts.append(cp_amm_out(
            R_in_2, R_out_2, between_lp_amts[-1]))
        between_lp_amts.append(cp_amm_out(
            R_in_3, R_out_3, between_lp_amts[-1]))

        profit = max(between_lp_amts[-1] - d_in_0, 0)

        return d_in_0, profit, between_lp_amts
    else:
        return 0, 0, None


def fast_path_five_arb(R_in_0, R_out_0, R_in_1, R_out_1, R_in_2, R_out_2, R_in_3, R_out_3, R_in_4, R_out_4):
    solution1 = 10030.0902708124*(9.92516866559333e+31*sqrt(R_in_0)*sqrt(R_in_1)*sqrt(R_in_2)*sqrt(R_in_3)*sqrt(R_in_4)*sqrt(R_out_0)*sqrt(R_out_1)*sqrt(R_out_2)*sqrt(R_out_3)*sqrt(R_out_4)*(R_in_1*R_in_2*R_in_3*R_in_4 + 0.997*R_in_2*R_in_3*R_in_4*R_out_0 + 0.994009*R_in_3*R_in_4*R_out_0*R_out_1 + 0.991026973*R_in_4*R_out_0*R_out_1*R_out_2 + 0.988053892081*R_out_0*R_out_1*R_out_2*R_out_3)**2 - 100000000.0*R_in_0*R_in_1*R_in_2*R_in_3*R_in_4*(1.0e+24*R_in_1**2*R_in_2**2*R_in_3**2*R_in_4**2 + 1.994e+24*R_in_1*R_in_2**2*R_in_3**2*R_in_4**2*R_out_0 + 1.988018e+24*R_in_1*R_in_2*R_in_3**2*R_in_4**2*R_out_0*R_out_1 + 1.982053946e+24*R_in_1*R_in_2*R_in_3*R_in_4**2*R_out_0*R_out_1*R_out_2 + 1.976107784162e+24*R_in_1*R_in_2*R_in_3*R_in_4*R_out_0*R_out_1*R_out_2*R_out_3 + 9.94009e+23*R_in_2**2*R_in_3**2*R_in_4**2*R_out_0**2 + 1.982053946e+24*R_in_2*R_in_3**2*R_in_4**2*R_out_0**2*R_out_1 + 1.976107784162e+24*R_in_2*R_in_3*R_in_4**2*R_out_0**2*R_out_1*R_out_2 + 1.97017946080951e+24*R_in_2*R_in_3*R_in_4*R_out_0**2*R_out_1*R_out_2*R_out_3 + 9.88053892081e+23*R_in_3**2*R_in_4**2*R_out_0**2*R_out_1**2 + 1.97017946080951e+24*R_in_3*R_in_4**2*R_out_0**2*R_out_1**2*R_out_2 + 1.96426892242709e+24*R_in_3*R_in_4*R_out_0**2*R_out_1**2*R_out_2*R_out_3 + 9.82134461213543e+23*R_in_4**2*R_out_0**2*R_out_1**2*R_out_2**2 + 1.9583761156598e+24*R_in_4*R_out_0 **
                                  2*R_out_1**2*R_out_2**2*R_out_3 + 9.76250493656412e+23*R_out_0**2*R_out_1**2*R_out_2**2*R_out_3**2))/((1000000000000.0*R_in_1*R_in_2*R_in_3*R_in_4 + 997000000000.0*R_in_2*R_in_3*R_in_4*R_out_0 + 994009000000.0*R_in_3*R_in_4*R_out_0*R_out_1 + 991026973000.0*R_in_4*R_out_0*R_out_1*R_out_2 + 988053892081.0*R_out_0*R_out_1*R_out_2*R_out_3)*(1.0e+24*R_in_1**2*R_in_2**2*R_in_3**2*R_in_4**2 + 1.994e+24*R_in_1*R_in_2**2*R_in_3**2*R_in_4**2*R_out_0 + 1.988018e+24*R_in_1*R_in_2*R_in_3**2*R_in_4**2*R_out_0*R_out_1 + 1.982053946e+24*R_in_1*R_in_2*R_in_3*R_in_4**2*R_out_0*R_out_1*R_out_2 + 1.976107784162e+24*R_in_1*R_in_2*R_in_3*R_in_4*R_out_0*R_out_1*R_out_2*R_out_3 + 9.94009e+23*R_in_2**2*R_in_3**2*R_in_4**2*R_out_0**2 + 1.982053946e+24*R_in_2*R_in_3**2*R_in_4**2*R_out_0**2*R_out_1 + 1.976107784162e+24*R_in_2*R_in_3*R_in_4**2*R_out_0**2*R_out_1*R_out_2 + 1.97017946080951e+24*R_in_2*R_in_3*R_in_4*R_out_0**2*R_out_1*R_out_2*R_out_3 + 9.88053892081e+23*R_in_3**2*R_in_4**2*R_out_0**2*R_out_1**2 + 1.97017946080951e+24*R_in_3*R_in_4**2*R_out_0**2*R_out_1**2*R_out_2 + 1.96426892242709e+24*R_in_3*R_in_4*R_out_0**2*R_out_1**2*R_out_2*R_out_3 + 9.82134461213543e+23*R_in_4**2*R_out_0**2*R_out_1**2*R_out_2**2 + 1.9583761156598e+24*R_in_4*R_out_0**2*R_out_1**2*R_out_2**2*R_out_3 + 9.76250493656412e+23*R_out_0**2*R_out_1**2*R_out_2**2*R_out_3**2))

    solution2 = -0.00100300902708124*(9.92516866559333e+38*sqrt(R_in_0)*sqrt(R_in_1)*sqrt(R_in_2)*sqrt(R_in_3)*sqrt(R_in_4)*sqrt(R_out_0)*sqrt(R_out_1)*sqrt(R_out_2)*sqrt(R_out_3)*sqrt(R_out_4)*(R_in_1*R_in_2*R_in_3*R_in_4 + 0.997*R_in_2*R_in_3*R_in_4*R_out_0 + 0.994009*R_in_3*R_in_4*R_out_0*R_out_1 + 0.991026973*R_in_4*R_out_0*R_out_1*R_out_2 + 0.988053892081*R_out_0*R_out_1*R_out_2*R_out_3)**2 + 1.0e+15*R_in_0*R_in_1*R_in_2*R_in_3*R_in_4*(1.0e+24*R_in_1**2*R_in_2**2*R_in_3**2*R_in_4**2 + 1.994e+24*R_in_1*R_in_2**2*R_in_3**2*R_in_4**2*R_out_0 + 1.988018e+24*R_in_1*R_in_2*R_in_3**2*R_in_4**2*R_out_0*R_out_1 + 1.982053946e+24*R_in_1*R_in_2*R_in_3*R_in_4**2*R_out_0*R_out_1*R_out_2 + 1.976107784162e+24*R_in_1*R_in_2*R_in_3*R_in_4*R_out_0*R_out_1*R_out_2*R_out_3 + 9.94009e+23*R_in_2**2*R_in_3**2*R_in_4**2*R_out_0**2 + 1.982053946e+24*R_in_2*R_in_3**2*R_in_4**2*R_out_0**2*R_out_1 + 1.976107784162e+24*R_in_2*R_in_3*R_in_4**2*R_out_0**2*R_out_1*R_out_2 + 1.97017946080951e+24*R_in_2*R_in_3*R_in_4*R_out_0**2*R_out_1*R_out_2*R_out_3 + 9.88053892081e+23*R_in_3**2*R_in_4**2*R_out_0**2*R_out_1**2 + 1.97017946080951e+24*R_in_3*R_in_4**2*R_out_0**2*R_out_1**2*R_out_2 + 1.96426892242709e+24*R_in_3*R_in_4*R_out_0**2*R_out_1**2*R_out_2*R_out_3 + 9.82134461213543e+23*R_in_4**2*R_out_0**2*R_out_1**2*R_out_2**2 + 1.9583761156598e+24*R_in_4*R_out_0 **
                                      2*R_out_1**2*R_out_2**2*R_out_3 + 9.76250493656412e+23*R_out_0**2*R_out_1**2*R_out_2**2*R_out_3**2))/((1000000000000.0*R_in_1*R_in_2*R_in_3*R_in_4 + 997000000000.0*R_in_2*R_in_3*R_in_4*R_out_0 + 994009000000.0*R_in_3*R_in_4*R_out_0*R_out_1 + 991026973000.0*R_in_4*R_out_0*R_out_1*R_out_2 + 988053892081.0*R_out_0*R_out_1*R_out_2*R_out_3)*(1.0e+24*R_in_1**2*R_in_2**2*R_in_3**2*R_in_4**2 + 1.994e+24*R_in_1*R_in_2**2*R_in_3**2*R_in_4**2*R_out_0 + 1.988018e+24*R_in_1*R_in_2*R_in_3**2*R_in_4**2*R_out_0*R_out_1 + 1.982053946e+24*R_in_1*R_in_2*R_in_3*R_in_4**2*R_out_0*R_out_1*R_out_2 + 1.976107784162e+24*R_in_1*R_in_2*R_in_3*R_in_4*R_out_0*R_out_1*R_out_2*R_out_3 + 9.94009e+23*R_in_2**2*R_in_3**2*R_in_4**2*R_out_0**2 + 1.982053946e+24*R_in_2*R_in_3**2*R_in_4**2*R_out_0**2*R_out_1 + 1.976107784162e+24*R_in_2*R_in_3*R_in_4**2*R_out_0**2*R_out_1*R_out_2 + 1.97017946080951e+24*R_in_2*R_in_3*R_in_4*R_out_0**2*R_out_1*R_out_2*R_out_3 + 9.88053892081e+23*R_in_3**2*R_in_4**2*R_out_0**2*R_out_1**2 + 1.97017946080951e+24*R_in_3*R_in_4**2*R_out_0**2*R_out_1**2*R_out_2 + 1.96426892242709e+24*R_in_3*R_in_4*R_out_0**2*R_out_1**2*R_out_2*R_out_3 + 9.82134461213543e+23*R_in_4**2*R_out_0**2*R_out_1**2*R_out_2**2 + 1.9583761156598e+24*R_in_4*R_out_0**2*R_out_1**2*R_out_2**2*R_out_3 + 9.76250493656412e+23*R_out_0**2*R_out_1**2*R_out_2**2*R_out_3**2))

    d_in_0 = max(solution1, solution2)

    if d_in_0 > 0:
        between_lp_amts = [d_in_0]
        between_lp_amts.append(cp_amm_out(
            R_in_0, R_out_0, between_lp_amts[-1]))
        between_lp_amts.append(cp_amm_out(
            R_in_1, R_out_1, between_lp_amts[-1]))
        between_lp_amts.append(cp_amm_out(
            R_in_2, R_out_2, between_lp_amts[-1]))
        between_lp_amts.append(cp_amm_out(
            R_in_3, R_out_3, between_lp_amts[-1]))
        between_lp_amts.append(cp_amm_out(
            R_in_4, R_out_4, between_lp_amts[-1]))

        profit = max(between_lp_amts[-1] - d_in_0, 0)

        return d_in_0, profit, between_lp_amts
    else:
        return 0, 0, None


if __name__ == "__main__":
    start = time.time()
    print(fast_path_two_arb(100, 1000, 1000, 1000))
    print((time.time() - start) * 1000)

    start = time.time()
    print(fast_path_three_arb(100, 1000, 1000, 1000, 1000, 1000))
    print((time.time() - start) * 1000)

    start = time.time()
    print(fast_path_four_arb(100, 1000, 1000, 1000, 1000, 1000, 1000, 1000))
    print((time.time() - start) * 1000)

    start = time.time()
    print(fast_path_five_arb(100, 1000, 1000, 1000,
          1000, 1000, 1000, 1000, 1000, 1000))
    print((time.time() - start) * 1000)
