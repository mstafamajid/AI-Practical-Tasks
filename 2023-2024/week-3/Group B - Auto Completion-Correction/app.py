from world_list import Words
import queue


class Project3:
    def __init__(self, input_str):
        self.input = input_str

    def run_app(self):
        words_count = 0
        word_match_most = queue.PriorityQueue()
        words = Words.word_list()

        while words_count < len( words ):
            matrix = [[0] * (len( words[words_count] ) + 1) for _ in range(len(self.input) + 1)]

            row = 1
            # while row < len(matrix):
            #     column = 1
            #     while column < len(matrix[1]):

            #         if self.input[row-1] == words[words_count][column-1]:
            #             matrix[row][column] = 1 + matrix[row-1][column-1]
            #         else:
            #             matrix[row][column] = Project3.maximum( matrix[row-1][column], matrix[row][column-1] )
            #         column+=1
            #     row+=1
            for row in range(1, len(matrix)):
                for column in range(1, len(matrix[1])):
                    if self.input[row - 1] == words[words_count][column - 1]:
                        matrix[row][column] = 1 + matrix[row - 1][column - 1]
                    else:
                        matrix[row][column] = max(matrix[row - 1][column], matrix[row][column - 1])



            #get the letters inside the match_letter array
            # match_letters = []
            # # start from last index to get the sequence of letters that match
            # row = len(matrix) - 1
            # column = len(matrix[1]) - 1

            # while row > 0:
            
            #     while column > 0:

            #         if matrix[row-1][column] == matrix[row][column-1] and self.input[row-1] == words[words_count][column-1]:

            #             match_letters.append( self.input[row-1] )
            #             row-=1
            #             column-=1
            #         else:
            #             if matrix[row-1][column] >  matrix[row][column-1]:
            #                 row-=1
            #             else:
            #                 column-=1

            #     if matrix[row][column] == 0:
            #             break
            match_letters = []
            row, column = len(matrix) - 1, len(matrix[1]) - 1

            while row > 0 and column > 0:
                if matrix[row - 1][column] == matrix[row][column - 1] and self.input[row - 1] == words[words_count][column - 1]:
                    match_letters.append(self.input[row - 1])
                    row -= 1
                    column -= 1
                elif matrix[row - 1][column] > matrix[row][column - 1]:
                    row -= 1
                else:
                    column -= 1

                # Check if the loop exited due to matrix[row][column] == 0
                if matrix[row][column] == 0:
                    break

            
            error_rate = len(words[words_count]) - len(match_letters)

            # add a value here indicating error rate according to the value you put in(second parameter)
            word_match_most.put(  ( -(max(max(matrix))), error_rate, words[words_count], matrix, match_letters ))
                
            words_count+=1

        return word_match_most
        
    def maximum(num1, num2):
        if num1 > num2:
            return num1
        else:
            return num2
        
    def get_most(self, number):

        pqueue = self.run_app()

        most_matched_values = []
        while not pqueue.empty() and number >0:
            most_matched_values.append( pqueue.get() )
            number-=1

        return most_matched_values
