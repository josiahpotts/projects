#include <iostream>
#include <cstdlib>
#include <cmath>
#include <ctime>

using namespace std;

/******************************************************************************************
 * Title: Assignment 2 "TwentyOne"							  *
 * Author: Josiah Potts									  *
 * Date: 4/23/2021 									  *
 * Description: This is a game for 1-4 players to try to beat the dealer in a game of 21. *
 * Input: Integers									  *
 * Output: Integers									  *
 * ****************************************************************************************/

//Function to accept only 1-4 players that will play the game.
int num_of_players() {

   int numPlayers = 0;
   do {
      	cout << "How many players for this game? (1-4): ";
	cin >> numPlayers;
		if (!(numPlayers >= 1 && numPlayers <=4)) {
	   cout << "You entered an incorrect number of players." << endl;
		}
   } while (!(numPlayers >= 1 && numPlayers <= 4));

   return numPlayers;
}
//The dealer, if called forth, will automatically try to beat the player, or bust while trying.
int dealer_turn(int playerTotal, int playerBet) {

   srand(time(NULL));
   int dealerCard, dealerTotal = 0;
   	cout << "It is the dealer's turn." << endl;
   do {

      dealerCard = (rand()%11) + 1;
      	cout << "The dealer gets: " << dealerCard << endl;
	dealerTotal = dealerTotal + dealerCard;
		if (dealerTotal == playerTotal) {
		   cout << "The dealer's total is " << dealerTotal << " , therefore it's a tie! You don't lose your bet." << endl;
		   playerBet = 0;
		}
		else if (dealerTotal == 21) {
		   cout << "The dealer got 21. The dealer wins." << endl;
		   cout << "Sorry, you lose $" << playerBet << endl;
		   playerBet = playerBet *-1;
		}
		else if (dealerTotal > 21) {
		   cout << "The dealer's total is " << dealerTotal << ". The dealer busts!!!" << endl;
		   playerBet = playerBet;
		   cout << "You win this hand!!! You have won $" << playerBet << endl;
		}
		else if (dealerTotal > playerTotal && dealerTotal < 21) {
		   cout << "The dealer's total is " << dealerTotal << ". Sorry, that means the dealer wins this hand." << endl;
		   cout << "You lost your bet of $" << playerBet << endl;
		   playerBet = playerBet * -1;
		}
		else {
		   cout << "The dealer is dealt another card..." << endl;
		}
   } while (dealerTotal < playerTotal);
   
   return playerBet;
}

//This is the function that runs the player's turn, starting with how much they would like to bet.
int player_turn(int player, int playerBank) {
  
   srand(time(NULL));
   int bet = 0, betResult, cardDecision = 3, newBet = 0;
   int randomCard, cardTotal = 0;
   	cout << "It is Player " << player << "'s turn." << endl;
   	cout << "Player " << player << ", you have $" << playerBank << " to bet from." << endl;
   	cout << "How much would you like to bet for this turn?: $";
   do {
      cin >> bet;
	if (bet > playerBank) {
	   cout << "You haven't won that much money quite yet, bub. Please bet only what you have: $";
	}
	else if (bet == 0) {
	   cout << "We aren't just playing for fun here. Please place a bet: $";
	}
	else if (bet < 0) {
	   cout << "Is that some sort of joke? We can't just give you money, you have to win it. Please place a real bet: $";
	}
   } while (bet <= 0 || bet > playerBank);
   cout << "Your bet is $" << bet << endl;

//Player is given an initial card, and gets to choose if they would like another one.
//They will continue to be asked as long as their total cards are less than 21.
   do {

   randomCard = (rand()%11) + 1;
   cout << "The dealer has dealt you: " << randomCard << endl;
   cardTotal = cardTotal + randomCard;
   	if(cardTotal == 21) {
	   	cout << "TWENTY ONE!!! Congratulations, you win this hand! Your earnings are doubled!" << endl;
		betResult = bet * 2;
		cout << "You win $" << betResult << endl;
		playerBank = playerBank + betResult;
		cout << "You now have $" << playerBank << " to play with." << endl;
		break;
	}
	else if(cardTotal > 21) {
	   	cout << "BUST!!! Sorry, the dealer wins this hand." << endl;
		cout << "You lose $" << bet << endl;
		playerBank = playerBank - bet;
		cout << "You now have $" << playerBank << " to play with." << endl;
		break;
	}
	else {
   		cout << "Your cards total to: " << cardTotal << endl;
   		do {
   			cout << "Would you like another card?(1-yes, 0-no): ";
   			cin >> cardDecision;
				if (cardDecision < 0 || cardDecision > 1) {
				   cout << "Invalid entry." << endl;
				}
		} while (cardDecision < 0 || cardDecision > 1);
	} 
   } while (cardDecision == 1);
   	if (cardDecision == 0) {
	  newBet = dealer_turn(cardTotal, bet);
	  playerBank = playerBank + newBet;
	  cout << "You now have $" << playerBank << " to play with." << endl;
	}

   return playerBank;
}

int main() {

   int playAgain;

   do {
   	cout << "Welcome to the table." << endl;
	cout << "Let's play Twenty-One!" << endl;
	cout << "------------------------" << endl;
   	
 	int numPlayers = num_of_players();
	cout << numPlayers << " players will be playing at the table today." << endl;

//Time to put some money in the bank for the players participating.
	int bank1, bank2, bank3, bank4;
	int totalBank;
	for (int i = 0; i < numPlayers; i++) {
	   cout << "Player " << i+1 << ": How much money would you like to put into your bank?: $";
	   if (i == 0) {
	      do {
	     	cin >> bank1;
	      	        if (bank1 <= 0) {
		   	   cout << "You can't bet money you don't have. Invalid amount. Please enter a positive dollar amount: $";
		      } 
	      }while (bank1 <= 0);
	   }
	   else if (i == 1) {
	      do {
	      	cin >> bank2;
			if (bank2 <= 0) {
			   cout << "You can't bet money you don't have. Invalid amount. Please enter a positive dollar amount: $";
			}
	      } while (bank2 <= 0);
	   }
	   else if (i == 2) {
	      do {
	      	cin >> bank3;
			if (bank3 <= 0) {
			   cout << "You can't bet money you don't have. Invalid amount. Please enter a positive dollar amount: $";
			}
	      } while (bank3 <= 0);
	   }
	   else {
	      do {
	      	cin >> bank4;
			if (bank4 <= 0) {
			   cout << "You can't bet money you don't have. Invalid amount. Please enter a positive dollar amount: $";
			}
	      } while (bank4 <= 0);
	   }
	}

//Now it's time to call each player's turn if they have money in the bank.
//Each player can decide if they would like to play this hand.	
	int handDecision;

	do {

		if (bank1 > 0)	{
		   do {
		   	cout << "Player 1, would you like to play this hand?(1-yes,0-no): ";
		   	cin >> handDecision;
				if (handDecision < 0 || handDecision > 1) {
				   cout << "Invalid entry." << endl;
				}
		   } while (handDecision < 0 || handDecision > 1);
		   	if (handDecision == 1) {
				bank1 = player_turn(1, bank1);
				if (bank1 == 0) { 
					cout << "Player 1, you have lost all of your money." << endl;
				}
			}
			else {
			   	cout << "Player 1 has chosen to pass." << endl;
			}
		}
		if (bank2 > 0) {
		   do {
		   	cout << "Player 2, would you like to play this hand?(1-yes,0-no): ";
		   	cin >> handDecision;
				if (handDecision < 0 || handDecision > 1) {
				   cout << "Invalid entry." << endl;
				}
		   } while (handDecision < 0 || handDecision > 1);
		   	if (handDecision == 1) {
	   			bank2 = player_turn(2, bank2);
	   			if (bank2 == 0) {
		   			cout << "Player 2, you have lost all of your money." << endl;
				}
			}
			else {
			   	cout << "Player 2 has chosen to pass." << endl;
			}
		}
		if (bank3 > 0) {
		   do {
		   	cout << "Player 3, would you like to play this hand?(1-yes,0-no): ";
		   	cin >> handDecision;
				if (handDecision < 0 || handDecision > 1) {
				   cout << "Invalid entry." << endl;
				}
		   } while (handDecision < 0 || handDecision > 1);
		   	if (handDecision == 1) {
	   			bank3 = player_turn(3, bank3);
	   			if (bank3 == 0) {
		   			cout << "Player 3, you have lost all of your money." << endl;
				}
			}
			else {
			   	cout << "Player 3 has chosen to pass." << endl;
			}
		}	
		if (bank4 > 0) {
		   do {
		   	cout << "Player 4, would you like to play this hand?(1-yes,0-no): ";
		   	cin >> handDecision;
				if (handDecision < 0 || handDecision > 1) {
				   cout << "Invalid entry." << endl;
				}
		   } while (handDecision < 0 || handDecision > 1);
		   	if (handDecision == 1) {
	   			bank4 = player_turn(4, bank4);
	  			if (bank4 == 0) {
	      				cout << "Player 4, you have lost all of your money." << endl;
				}
			}
			else {
			   	cout << "Player 4 has chosen to pass." << endl;
			}
		}

		cout << "The round is over, the current amount of money each player has is: " << endl;
		if (numPlayers > 0) {
			cout << "Player 1: $" << bank1 << endl;
		}
		if (numPlayers > 1) {
			cout << "Player 2: $" << bank2 << endl;
		}
		if (numPlayers > 2) {
			cout << "Player 3: $" << bank3 << endl;
		}
		if (numPlayers > 3) {
			cout << "Player 4: $" << bank4 << endl;
		}
		totalBank = bank1 + bank2 + bank3 + bank4;
			if (totalBank == 0) {
			   cout << "There is no more money to bet from any player, sorry. Game over." << endl;
			   break;
			}
		do {
			cout << "Would you like start another hand?(1-yes,0-no): ";
			cin >> handDecision;
				if (handDecision < 0 || handDecision > 1) {
				   cout << "Invalid entry." << endl;
				}
		} while (handDecision < 0 || handDecision > 1);
//Choice to play more or end the game.
	} while (handDecision == 1);

	cout << "This game session has ended. Thank you for playing!" << endl;
	
//Choice to restart the game.
	do {
		cout << "Do you want to restart a new game?(1-yes, 0-no): ";
		cin >> playAgain;
			if (playAgain < 0 || playAgain > 1) {
			   cout << "Invalid entry." << endl;
			}
	} while (playAgain < 0 || playAgain > 1);

   }

   while (playAgain == 1);	

	cout << "Thank you and have a wonderful day." << endl;

return 0;

}
