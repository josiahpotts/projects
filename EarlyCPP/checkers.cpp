#include <iostream>
#include <cstring>
#include <string>
#include <cstdlib>

using namespace std;

/****************************************************************************************
 * Title: checkers.cpp									*
 * Author: Josiah Potts									*
 * Date 6/8/2021									*
 * Description: This program performs the game of checkers if 2 players are playing.	*
 * Input: Integers									*
 * Output: 2-D array									*
 * *************************************************************************************/

void print_board(char**board, int r, int c);
void king(char **board, int r, int c);

/********************************************************************************************************
 * Function name: board_inti()										*
 * Description: This function initializes the starting board complete with the checker board		*
 * 		and both player's pieces.								*
 * Parameter: char **board, int r, int c								*
 * Pre-condition: The board has to be from the heap, and the row and column are decided by the user	*
 * 		in the command line or prompted for during runtime.					*
 * Post-condition: Characters populate certain parts of the 2-D array for later use.			*
 * ******************************************************************************************************/
void board_init(char **board, int r, int c) {
   
   for (int i = 0; i < r; ++i) {
        for (int j = 0; j < c; ++j) {
	   if ((j % 2 == 1 && i % 2 == 0) && (i < (r / 2) - 1)) {
	      board[i][j] = 'x';
	   }
	   else if ((j % 2 == 0 && i % 2 == 1) && (i < (r / 2) - 1)) {
	      board[i][j] = 'x';
	   }
	   if ((j % 2 == 1 && i % 2 ==0) && (i >= (r / 2) + 1)) {
	      board[i][j] = 'o';
	   }
	   else if ((j % 2 == 0 && i % 2 == 1) && (i >= (r / 2) + 1)) {
	      board[i][j] = 'o';
	   }
	}
   }
}

/****************************************************************************************************************
 * Function name: player1_turn()										*
 * Description: Player 1 is the 'o' piece and they will be given the opportunity to move 1 piece for their turn.*
 * Parameter: char **board, int r, int c, int player								*
 * Pre-condition: The board must be initialized with rows and columns.						*
 * Post-condition: Edits the contents within the chosen locations of the 2-D array.				*
 * **************************************************************************************************************/
void player1_turn(char **board, int r, int c, int player) {

   int check = 0;
   int row = r, col = c;
   cout << "Player 1, it is your turn." << endl;
   do {
      	check = 0;
   	cout << "Enter the row of the piece to move: ";
   	cin >> r;
   	cout << "Enter the column of the piece to move: ";
   	cin >> c;
 	if ((int)board[r-1][c-1] != 111) {
	 	cout << "You have no piece at " << r << ", " << c << "." << endl;
		check = 1;
	}
   } while (check == 1);
   board[r-1][c-1] = ' ';
   int originR = r, originC = c;
   do { 
      	check = 0;
	cout << "Enter the row where you want to move your piece: ";
	cin >> r;
	cout << "Enter the column you want to move your piece: ";
	cin >> c;
	if ((int)board[r-1][c-1] != 32) {
	   	cout << "You can't move there." << endl;
		check = 1;
	} 
   } while (check == 1);
   board[r-1][c-1] = 'o';
   if (originC > c) {
   	if ((int)board[r][c] == 120) {
	   	board[r][c] = ' ';
	}
   }
   else if (originC < c) {
      	if ((int)board[r][c-2] == 120) {
	   	board[r][c-2] = ' ';
	}
   }
   king(board, row, col);
   print_board(board, row, col);
}
/****************************************************************************************************************
 * Function name: player2_turn()										*
 * Description: Player 2 is the 'x' piece and they will be given the opportunity to move 1 piece for their turn.*
 * Parameter: char **board, int r, int c, int player								*
 * Pre-condition: The board must be initialized with rows and columns.						*
 * Post-condition: Edits the contents within the chosen locations of the 2-D array.				*
 * **************************************************************************************************************/
void player2_turn(char **board, int r, int c, int player) {

   int check = 0;
   int row = r, col = c;
   cout << "Player 2, it is your turn." << endl;
   do {
      	check = 0;
	cout << "Enter the row of the piece to move: ";
	cin >> r;
	cout << "Enter the column of the piece to move: ";
	cin >> c;
	if ((int)board[r-1][c-1] != 120) {
	   	cout << "You have no piece at " << r << ", " << c << "." << endl;
		check = 1;
	}
   } while (check == 1);
   board [r-1][c-1] = ' ';
   int originR = r, originC = c;
   do {
      	check = 0;
	cout << "Enter the row where you want to move your piece: ";
	cin >> r;
	cout << "Enter the column you want to move your piece: ";
	cin >> c;
	if ((int)board[r-1][c-1] != 32) {
	   	cout << "You can't move there." << endl;
		check = 1;
	}
   } while (check == 1);
   board[r-1][c-1] = 'x';
   if (originC < c) {
      if ((int)board[r-2][c-2] == 111) {
	 	board[r-2][c-2] = ' ';
      }
   }
   else if (originC > c) {
      if ((int)board[r-2][c] == 111) {
	 	board[r-2][c] = ' ';
      }
   }

   king(board, row, col);
   print_board(board, row, col);
}
/********************************************************************************
 * Function name: print_board()							*
 * Description: Prints out the 2-D array of board to reveal its contents.	*
 * Parameter: char **board, int r, int c					*
 * Pre-conditions: Must have an initialized board with contents.		*
 * Post-conditions: Does not alter anything, simply prints the board.		*
 * ******************************************************************************/
void print_board(char **board, int r, int c) {

   for (int i = 0; i < c; ++i) {
      if (i >= 10) {
	 cout << " " << i+1;
      }
      else {
	 cout << "  " << i+1;
      }
   }
   cout << endl;
   for (int i = 0; i < r; i++) {
      if (board[i][0]) {
	 if(i >= 9) {
	 cout << i+1;
	 }
      else {
	 cout << i+1 << " ";
      }
   }
   for (int j = 0; j < c; j++) {
      if (i % 2 == 0 && j % 2 == 0) {
	 cout << "\033[30;47m " << board[i][j] << " ";
      }
      else if (i % 2 == 1 && j % 2 == 1) {
	 cout << "\033[30;47m " << board[i][j] << " ";
      }
      else {
	 cout << "\033[0m " << board[i][j] << " ";
      }
      cout << "\033[0m";
   }
   cout << endl;
   }
}

void king(char** board, int r, int c) {

   for (int i = 0; i < c; ++i) {
      if (board[0][i] == 'o') {
	 board[0][i] = 'O';
      }
      if (board[r-1][i] == 'x') {
	 board[r-1][i] = 'X';
      }
   }
}

/********************************************************************************************************
 * Funciton name: determine_winner()									*
 * Description: This function combs through the entire array for each player to see if there are	*
 * 		any remaining pieces of the opponent, and if there aren't it will end the game.		*
 * Parameters: char** board, int r, int c								*
 * Pre-conditions: Requires an initialized board.							*
 * Post-conditions: Outputs an integer value of 1 if there is a winner and 0 if there is no winner yet.	*
 * *****************************************************************************************************/
int determine_winner(char** board, int r, int c) {

   int winner = 1;
   for (int i = 0; i < r; ++i) {
      for (int j = 0; i < r; ++i) {
	 if ((int)board[i][j] == 111) {
	    for (int t = 0; t < r; ++t) {
	       for (int q = 0; q < c; ++q) {
		  if ((int)board[t][q] == 120) {
	       		winner = 0;
		  }
	       }
	    }
	 }
	 else if ((int)board[i][j] == 120) {
	    for (int w = 0; w < r; ++w) {
	       for (int v = 0; v < c; ++v) {
		  if ((int)board[w][v] == 111) {
		     	winner = 0;
		  }
	       }
	    }
	 }
      }
   }
   return winner;
}
/****************************************************************************************************************
 * Function name: main ()											*
 * Description: Handles errors in the Command Line use when running the program and then shuffles through	*
 * 		the different functions to play the game.							*
 * Parameters: int argc, char **argv										*
 * Pre-conditions: Does not have any but it does accept a board size argument.					*
 * Post-conditions: Runs the game and ends when there is a winner.						*
 * **************************************************************************************************************/
int main(int argc, char **argv) {

   //This portion is to determine the board size.
   int rows, cols, player1 = 1, player2 = 2;
   int rows_again = 0;
   char* convert;
   char convert1;
  
   if (argc > 1) {
        convert = argv[1];
   	convert1 = argv[1][1];
   	atoi(convert); 
   }
 
   //If ran with more than the program name and board size it will prompt for board size.
   	if (argc > 2) {
		do {
	   	cout << "Enter size of board (8,12,16): ";
	   	cin >> rows;
			if((rows == 8 || rows == 12) || (rows == 16)) {
			   	rows_again = 1;
				cols = rows;
			}
			else {
			   cout << "Incorrect size." << endl;
			}
		} while (rows_again == 0);
	}
   //If proper argc values input this portion will determine the board size based on the argv value, or reprompt if incorrect.
	while (rows_again == 0) {
		if (argc == 2) {

			if ((int)argv[1][0] == 56) {
	   			rows = 8;
	   			cols = 8;
				rows_again = 1;
			}
			else if ((int)convert1 == 50) {
	   			rows = 12;
	   			cols = 12;
				rows_again = 1;
			}
			else if ((int)convert1 == 54) {
	   			rows = 16;
	   			cols = 16;
				rows_again = 1;
			}
			else
	   			do {
	      				cout << "Enter size of board (8,12,16): ";
	      				cin >> rows;
	      					if((rows == 8 || rows == 12) ||(rows == 16)) {
			   				rows_again = 1;
							cols = rows;
						}
						else {
			   				cout << "Incorrect size." << endl;
						}
	   			} while (rows_again == 0);
		}
		else if (argc == 1) {
		   	do {
			   	cout << "Enter size of board (8,12,16): ";
				cin >> rows;
					if((rows == 8 || rows == 12) ||(rows == 16)) {
					   	rows_again = 1;
						cols = rows;
					}
					else {
					   	cout << "Incorrect size." << endl;
					}
			} while (rows_again == 0);
		}
	}
   //Declaration of the board and allocation to the heap.
   char **board = NULL;
   board = new char* [rows];

   //Creating columns on the heap for 2D array.
   for (int i = 0; i < rows; ++i) {

      	board[i] = new char [cols];
   }
   
   //Initializing the starting values on the board.
   for (int i = 0; i < rows; ++i) {
	for (int j = 0; j < cols; ++j) {

	   	board[i][j] = ' ';
	}
   } 
   board_init(board, rows, cols); 
   print_board(board, rows, cols);
   //Rotating of player turns until there is a winner.
   int winner = 3;
   do {
   	player1_turn(board, rows, cols, player1);
   	player2_turn(board, rows, cols, player2);
	winner = determine_winner(board, rows, cols);
   } while (winner == 0);

   //Deleting heap memory.
   for (int i = 0; i < rows; ++i) {
	delete[] board[i];
   }
   delete[] board;


   return 0;
}
