import math
import random

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import numpy as np
import scipy.stats as sp
from phoneLine import PhoneLine

number_of_lines = 50
predicted_traffic = [10, 50, 100, 500, 1000, 2500, 5000]
#predicted_traffic = [10, 50]


call_holding_distributions = ['gamma', 'exponential', 'erlang', 'flat']
simulation_runs = 1000

def main():

    results = []

    number_of_loops = 0

    for distribution in call_holding_distributions:

        actual_gos_array = np.empty(len(predicted_traffic))
        predicted_gos_array = np.empty(len(predicted_traffic))

        current_traffic_value = 0

        for traffic in predicted_traffic:

            actual_gos = 0
            predicted_gos = 0

            for run in range(0, simulation_runs):

                call_length = 0

                if distribution == 'gamma':
                    call_length = np.random.standard_gamma(10, size=traffic)
                elif distribution == 'exponential':
                    call_length = np.random.exponential(10, size=traffic)
                elif distribution == 'erlang':
                    call_length = sp.erlang.rvs(1, size=traffic, scale=10)
                elif distribution == 'flat':
                    call_length = []
                    for i in range(0, traffic):
                        call_length.append(random.randint(1, 60))

                call_times = sorted(np.random.uniform(0, 60, traffic))
                av_call_length = 0
                no_of_calls = 0

                for length in call_length:
                    no_of_calls += 1
                    av_call_length += length

                av_call_length = av_call_length / no_of_calls

                phone_lines = []

                for i in range(0, number_of_lines - 1):
                    phone_lines.append(PhoneLine(0, 0))

                calls_accepted = 0
                calls_rejected = 0

                for i in range(0, traffic):
                    call_accepted = False
                    current_call_start = call_times[i]
                    current_call_end = (call_times[i] + call_length[i])
                    current_call_duration = call_length[i]

                    line_number = 0

                    for line in phone_lines:
                        line_number += 1
                        number_of_loops += 1

                        if line.call_end <= current_call_start:
                            line.call_start = current_call_start
                            line.call_end = current_call_end
                            call_accepted = True
                            break

                    if call_accepted:
                        calls_accepted += 1
                    else:
                        calls_rejected += 1

                actual_gos += float(calls_rejected) / float(traffic)
                predicted_gos += erlang_b(traffic * (av_call_length / 60), number_of_lines)

            actual_gos = actual_gos / simulation_runs
            predicted_gos = predicted_gos / simulation_runs

            summary = "\n------------\n" + \
                "Distribution: " + str(distribution) + \
                "\nNumber of calls: " + str(traffic) + \
                "\nNumber of lines: " + str(number_of_lines) + \
                "\nPredicted GOS: " + str(predicted_gos) + \
                "\nActual GOS: " + str(actual_gos) + \
                "\n------------\n"

            results.append(summary)

            actual_gos_array[current_traffic_value] = actual_gos
            predicted_gos_array[current_traffic_value] = predicted_gos

            current_traffic_value += 1

        print(actual_gos_array)
        print(predicted_gos_array)

        plt.plot(predicted_traffic, actual_gos_array, 'r')
        plt.plot(predicted_traffic, predicted_gos_array, 'b')
        plt.suptitle("GOS vs. No. of Calls for " + distribution + " call holding distribution")
        plt.xlabel("No. of Calls")
        plt.ylabel("GOS")

        red_patch = mpatches.Patch(color='red', label='Actual GOS')
        blue_patch = mpatches.Patch(color='blue', label='Predicted GOS')
        plt.legend(handles=[red_patch, blue_patch])

        plt.show()

    print("\n\n---Summary---\n Full results of all simulations:")

    for result in results:
        print(result)

    print(number_of_loops)


def erlang_b(E, m):
    denom = 0

    for j in range(1, m + 1):
        denom += (E ** j)/(math.factorial(j))
    return ((E**m)/math.factorial(m))/denom


if __name__ == '__main__':
    main()

