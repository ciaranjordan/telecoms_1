import math

import numpy as np
from phoneLine import PhoneLine

number_of_lines = 50
predicted_traffic = [10, 50, 100, 1000]


def main():

    results = []

    for traffic in predicted_traffic:
        print("Traffic:", traffic)
        print("No. of lines", number_of_lines)

        call_times = sorted(np.random.uniform(0, 60, traffic))
        call_length = np.random.standard_gamma(10, size=traffic)
        av_call_length = 0

        for length in call_length:
            av_call_length += length

        print("Predicted GOS:", erlang_b((traffic * (av_call_length / 60)), number_of_lines))

        phone_lines = []

        for i in range(0, number_of_lines - 1):
            phone_lines.append(PhoneLine(0, 0))

        calls_accepted = 0
        calls_rejected = 0

        for i in range(0, traffic):
            print("\nStarting simulation on call", i)
            call_accepted = False
            current_call_start = call_times[i]
            current_call_end = (call_times[i] + call_length[i])
            current_call_duration = call_length[i]

            print("Call details:")
            print("Call start time:", current_call_start)
            print("Call end time:", current_call_end)
            print("Call duration:", current_call_duration)

            line_number = 0

            for line in phone_lines:
                line_number += 1

                print("Checking line", line_number)
                print("Line status:")
                print("Line call start time:", line.call_start)
                print("Line call end time:", line.call_end)

                if line.call_end <= current_call_start:
                    line.call_start = current_call_start
                    line.call_end = current_call_end
                    call_accepted = True
                    print("Call accepted on line", line_number)
                    break
                else:
                    print("Line", line_number, "is busy.")

            if call_accepted:
                print("Call accepted.")
                calls_accepted += 1
            else:
                print("Call rejected")
                calls_rejected += 1

        print("\n\nCalls accepted:", calls_accepted)
        print("Calls rejected:", calls_rejected)

        actual_gos = float(calls_rejected) / float(traffic)

        summary = "\n\n---Summary---\n" + \
            "Number of calls: " + str(traffic) + \
            "\nNumber of lines: " + str(number_of_lines) + \
            "\nPredicted GOS: " + str(erlang_b(traffic, number_of_lines)) + \
            "\nActual GOS: " + str(actual_gos) + \
            "\n------------\n"

        print(summary)

        results.append(summary)

    print("Full results of all simulations:")

    for result in results:
        print(result)


def erlang_b(E, m):
    denom = 0

    for j in range(1, m + 1):
        denom += (E ** j)/(math.factorial(j))
    return ((E**m)/math.factorial(m))/denom


if __name__ == '__main__':
    main()

