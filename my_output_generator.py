#!/usr/bin/env python3

from common import format_tour, read_input

import my_solver

CHALLENGES = 7


def generate_output():
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        for solver, name in [(my_solver, 'output')]:
            answer = solver.solve(cities)
            tour = answer[0] #[1,4,2,6,...]

            with open(f'{name}_{i}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')
            
            print(answer[1])
    


if __name__ == '__main__':
    generate_output()