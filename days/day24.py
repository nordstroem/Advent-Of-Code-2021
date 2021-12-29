import util
import pickle


def parse(line):
    instr, *args = line.split(" ")
    args = [int(arg) if arg not in "xyzw" else arg for arg in args]
    return instr, args


instructions = util.read_lines("inputs/day24.txt", parse)


def to_sub_programs(all_instructions):
    sub_programs = []
    program = [all_instructions[0]]
    for instr in all_instructions[1:]:
        if instr[0] == "inp":
            sub_programs.append(program)
            program = [instr]
        else:
            program.append(instr)

    sub_programs.append(program)
    return sub_programs


all_sub_programs = to_sub_programs(instructions)


def extract_parameters():
    parameters = []
    for program in all_sub_programs:
        a = program[4][1][1]
        b = program[5][1][1]
        c = program[15][1][1]
        parameters.append((a, b, c))
    return parameters


def sub_program(w, z, a=26, b=-12, c=14):
    d = z // a
    if (z % 26 + b) == w:
        return d
    else:
        return d * 26 + (w + c)


def generate_possible_z_values(file_path):
    possible_z_values = [set([0])]

    for (a, b, c) in extract_parameters():
        new_possible_z_values = set()
        for i in range(1, 10):
            for z in possible_z_values[-1]:
                new_possible_z_values.add(sub_program(i, z, a, b, c))

        print("Done with sub program", len(new_possible_z_values))
        possible_z_values.append(new_possible_z_values)

    with open(file_path, "wb") as f:
        pickle.dump(possible_z_values, f)


def find_best_digit(results, search_z):
    if len(results) == 0:
        return "0"

    for result in results:
        best_digit = None
        z_to_search = []
        for (digit, z, from_z) in result:
            if z == search_z:
                if best_digit is None or digit < best_digit:
                    best_digit = digit
                    z_to_search = [from_z]
                elif digit == best_digit:
                    z_to_search.append(from_z)

        next_best = max([find_best_digit(results[1:], z) for z in z_to_search], key=int)
        return str(best_digit) + next_best


def part1():
    generate_possible_z_values("test.bin")

    # Run backwards:
    with open('test.bin', 'rb') as f:
        possible_z_values = pickle.load(f)

    params = extract_parameters()
    N = len(all_sub_programs)

    print(len(possible_z_values))
    prev_range = set([0])
    all_results = []
    for n in range(N):
        new_prev_range = set()
        results = []
        for i in range(1, 10):
            for z in possible_z_values[N - n - 1]:
                a, b, c = params[N - n - 1]
                z_out = sub_program(i, z, a, b, c)
                if z_out in prev_range:
                    new_prev_range.add(z)
                    print(f"{i}, {z}, from {z_out}")
                    results.append((i, z, z_out))
        all_results.append(results)
        prev_range = new_prev_range

        print(f"Done with {N - n - 1}", len(prev_range))

    with open("best_digits.bin", "wb") as f:
        pickle.dump(all_results, f)

    with open('best_digits.bin', 'rb') as f:
        all_results = pickle.load(f)

    print(find_best_digit(list(reversed(all_results)), 0)[:-1])
