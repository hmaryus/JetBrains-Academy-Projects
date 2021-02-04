import numpy as np


class Menu:
    def __init__(self):
        self.UI_method()

    def UI_method(self):
        print("1. Add matrices\n"
              "2. Multiply matrix by a constant\n"
              "3. Multiply matrices\n"
              "4. Transpose matrix\n"
              "5. Calculate a determinant\n"
              "6. Inverse matrix\n"
              "0. Exit\n")

        my_input = input('Your choice: ')

        self.actions(my_input)

    # BUILDING MATRIX METHOD
    def build_matrix(self):
        matrix = []
        size = list(map(int, input('Enter size of matrix: ').split()))

        print('Enter matrix:')
        for row in range(size[0]):
            matrix.append(list(map(float, input().split())))

        return matrix


    def add_matrices(self):
        # CONSTRUCT FIRST MATRIX
        first_matrix  = []
        first_size = list(map(int, input('Enter size of first matrix: ').split()))

        print('Enter first matrix:')
        for row in range(first_size[0]):
            first_matrix.append(list(map(float, input('> ').split())))

        # CONSTRUCT SECOND MATRIX
        second_matrix = []
        second_size = list(map(int, input('Enter size of second matrix: ').split()))

        # TESTING IF WE CAN ADD MATRICES
        if first_size != second_size:
            print('The operation cannot be performed.\n')
            self.UI_method()

        print('Enter second matrix:')
        for row in range(second_size[0]):
            second_matrix.append(list(map(float, input().split())))

        # CONSTRUCT THE SUM OF MATRICES
        the_sum = [[first_matrix[i][j] + second_matrix[i][j] for j in range(len(first_matrix[0]))] for i in range(len(first_matrix))]

        print('The result is:')
        for row in the_sum:
            print(*row)


    def multiply_by_constant(self):
        matrix = self.build_matrix()

        constant = float(input('Enter constant: '))

        print('The result is:')
        prod = [[constant * matrix[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]
        for row in prod:
            print(*row)


    def multiply_matrices(self):
        # CONSTRUCT FIRST MATRIX
        first_matrix = []
        first_size = list(map(int, input('Enter size of first matrix: ').split()))

        print('Enter first matrix:')
        for row in range(first_size[0]):
            first_matrix.append(list(map(float, input().split())))

        # CONSTRUCT SECOND MATRIX
        second_matrix = []
        second_size = list(map(int, input('Enter size of second matrix: ').split()))

        if first_size[1] != second_size[0]:
            print('The operation cannot be performed.\n')
            self.UI_method()

        print('Enter second matrix:')
        for row in range(second_size[0]):
            second_matrix.append(list(map(float, input().split())))

        prod = [[sum(a * b for a, b in zip(first_matrix_row, second_matrix_col)) for second_matrix_col in
                 zip(*second_matrix)] for first_matrix_row in first_matrix]

        for row in prod:
            print(*row)


    def transpose_matrix(self):
        print("1. Main diagonal\n"
              "2. Side diagonal\n"
              "3. Vertical line\n"
              "4. Horizontal line\n")

        my_input = input('Your choice: ')

        if my_input == '1':
            matrix = self.build_matrix()

            transposed_md = [[matrix[j][i] for j in range(len(matrix[0]))] for i in range(len(matrix))]

            print('The result is:')
            for row in transposed_md:
                print(*row)

        elif my_input == '2':
            matrix = self.build_matrix()
            matrix = matrix[::-1]

            transposed_sd = [[matrix[j][i] for j in range(len(matrix[0]))] for i in range(len(matrix))][::-1]

            print('The result is:')
            for row in transposed_sd:
                print(*row)

        elif my_input == '3':
            matrix = self.build_matrix()

            transposed_vl = [[matrix[i][j] for j in reversed(range(len(matrix[0])))] for i in range(len(matrix))]

            print('The result is:')
            for row in transposed_vl:
                print(*row)

        elif my_input == '4':
            matrix = self.build_matrix()

            transposed_hl = [[matrix[i][j] for j in range(len(matrix[0]))] for i in reversed(range(len(matrix)))]

            print('The result is:')
            for row in transposed_hl:
                print(*row)
        else:
            print('Invalid choice')
            self.transpose_matrix()


    def calculate_determinant(self):
        matrix = self.build_matrix()
        matrix = np.array(matrix)

        print(np.linalg.det(matrix))


    def inverse_matrix(self):
        matrix = self.build_matrix()

        inversed_matrix = np.linalg.inv(matrix)

        print('The result is:')
        for row in inversed_matrix:
            print(*row)


    def actions(self, action):
        if action == '1':
            self.add_matrices()
            self.UI_method()
        elif action == '2':
            self.multiply_by_constant()
            self.UI_method()
        elif action == '3':
            self.multiply_matrices()
            self.UI_method()
        elif action == '4':
            self.transpose_matrix()
            self.UI_method()
        elif action == '5':
            self.calculate_determinant()
            self.UI_method()
        elif action == '6':
            self.inverse_matrix()
            self.UI_method()
        elif action == '0':
            exit()
        else:
            print('Invalid choice')
            self.UI_method()

user = Menu()