from math import factorial


number_of_lines = 500
predicted_traffic = [1, 250, 500, 1000]


def main():
    print("Define predicted GOS")

    for traffic in predicted_traffic:
        print("Traffic:", traffic)
        print("No. of lines", number_of_lines)
        print("Predicted GOS:", erlang_b(traffic, number_of_lines))
        print("\n-----\n")

def erlang_b(E, m):
    InvB = 1.0
    for j in range(1, m + 1):
        InvB = 1.0 + InvB * (j / E)
    return (1.0 / InvB)

if __name__ == '__main__':
    main()

