from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sps

from phoneLine import PhoneLine

number_of_lines = 5
predicted_traffic = [10]


def main():
    print("Define predicted GOS:\n\n")

    for traffic in predicted_traffic:
        print("Traffic:", traffic)
        print("No. of lines", number_of_lines)
        print("Predicted GOS:", erlang_b(traffic, number_of_lines))
        print("\n-----\n")

    print("Part 2. Run Simulation")

    for traffic in predicted_traffic:
        print("Traffic:", traffic)

        call_times = sorted(np.random.uniform(0, 60, traffic))
        call_length = np.random.standard_gamma(10, size=traffic)

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
                    print("Line", line_number, "is busy. Trying next line.")

            if call_accepted:
                calls_accepted += 1
            else:
                calls_rejected += 1

        print("Calls accepted:", calls_accepted)
        print("Calls rejected:", calls_rejected)

        print("GOS:", calls_rejected/traffic, "\n\n")






def erlang_b(E, m):
    InvB = 1.0
    for j in range(1, m + 1):
        InvB = 1.0 + InvB * (j / E)
    return (1.0 / InvB)


if __name__ == '__main__':
    main()

