import json
import random
import csv
import time
import puzzle


def write_to_log(line):
    """Write line (array) to csv log file"""
    with open('log.csv', 'a', newline='') as csvfile:
        log = csv.writer(csvfile, delimiter=';',
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
        log.writerow(line)


def write_test_cases_to_file(test_cases_list):
    """Saves generated text files in a JSON file"""
    with open("test_cases.json", "w") as test_case_file:
        json.dump(test_cases_list, test_case_file)


def load_test_cases_from_file():
    """Loads previously generated text files from a JSON file"""
    with open("test_cases.json", "r") as test_case_file:
        test_cases = json.load(test_case_file)
        return test_cases


def generate_test_cases(n):
    """Generates n test cases for the puzzle"""
    test_cases = []
    while n > 0:
        test_cases.append(generate_test_case())
        n = n - 1
    return test_cases


def generate_test_case():
    """Generates a test case for the puzzle"""
    base_puzzle = list(range(9))
    while True:
        random.shuffle(base_puzzle)
        if puzzle.is_solvable(puzzle.list_to_matrix(base_puzzle)):
            return base_puzzle


def run_all_test_cases(test_list, heuristic):
    """Runs all puzzle test cases"""
    print("------------ Running puzzle test cases ----------------------------------")
    for test_case in test_list:
        run_test_case(test_case, heuristic)


def run_test_case(test_case, heuristic):
    """Runs the puzzle test case"""
    test_puzzle = puzzle.Puzzle(heuristic)
    test_matrix = puzzle.list_to_matrix(test_case)
    print("Running test case: ", test_matrix, "with heuristic: ", heuristic.__name__)
    start_time = time.time()
    test_puzzle.find_solution(test_matrix, puzzle.GOAL)
    end_time = time.time()
    log_entry = [str(test_matrix), start_time, end_time, end_time - start_time, test_puzzle.nodes_explored,
                 test_puzzle.nodes_in_solution, heuristic.__name__]
    write_to_log(log_entry)
    print("-------------------------------------------------------------------------")


def main():
    """Main function"""
    test_case_list = load_test_cases_from_file()

    run_all_test_cases(test_case_list, puzzle.h_manhattan)
    run_all_test_cases(test_case_list, puzzle.h_hamming)

if __name__ == '__main__':
    main()
