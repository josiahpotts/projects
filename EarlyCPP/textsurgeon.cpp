#include <iostream>
#include <string>
#include <cstring>

using namespace std;

/********************************************************************************************************
 * Title: textsurgeon.cpp										*
 * Author: Josiah Potts											*
 * Date: 5/18/2021											*
 * Description: User types in a sentence or paragraph and gets to choose 3 different ways to edit it	*
 * 		which includes swapping a letter, printing it in reverse, or counting words.		*
 * Input: User will input strings and integers.								*
 * Output: Out put will be strings and integers.							*
 * ******************************************************************************************************/

/************************************************************************************************
 * Function name: purge_string()								*
 * Description: Removes all characters and spaces that are not letters of the english alphabet.	*
 * Parameter: Pointer c-string									*
 * Pre-condition: Must have a stored c-string with any contents.				*
 * Post-condition: Outputs a "purged" version of the input to use for later scanning.		*
 * **********************************************************************************************/
char* purge_string(char* str) {

   	char* purged = new char[strlen(str)+1];
	strcpy(purged, str);
       
		for (int i = 0; i < strlen(purged); ++i) {
	   		if ((purged[i] == ' ') || (purged[i] >= '0' && purged[i] <= '9')) {
					strcpy(&purged[i], &purged[i+1]);
			     		i--;
			}
			if ((int)purged[i] < 65 || (int)purged[i] > 122) {
			   		strcpy(&purged[i], &purged[i+1]);
					i--;
			}
			if ((int)purged[i] > 90 && (int)purged[i] < 97) {
			   		strcpy(&purged[i], &purged[i+1]);
					i--;
			}
		}

	return purged;
}	

/************************************************************************************************************************
 * Function name: replace_letter()											*
 * Description: Allows the user to select a letter to replace with another letter. Only allows for character entries.	*
 * Parameter: Pointer c-string												*
 * Pre-condition: Must have an input string from the user with any contents.						*
 * Post-condition: Will print the string of text with replaced letters.							*
 * **********************************************************************************************************************/
void replace_letter(char* str) {

   char letter, swap;
   int check1 = 1, check2 = 1;

   do {
      	cout << "Select a letter within the text to replace(case sensitive): ";
   	cin >> letter;
		if((int)letter >= 65 && (int)letter <= 90) {
		   	check1 = 0;
		}
		else if((int)letter >= 97 && (int)letter <= 122) {
		   	check1 = 0;
		}
		else
		  	cout << "A letter was not entered, try again." << endl;
   } while (check1 == 1);
   
   do {
      	cout << "Select the letter you would like to replace " << "\'" << letter << "\'" << " with(case sensitive): ";
   	cin >> swap;
		if((int)swap >= 65 && (int)swap <= 90) {
			check2 = 0;
		}
		else if((int)swap >= 97 && (int)swap <= 122) {
		   	check2 = 0;
		}
		else
		   	cout << "A letter was not entered, try again." << endl;
   } while (check2 == 1);

   for(int i = 0; i < strlen(str); ++i) {
      if(str[i] == letter) {
 		str[i] = swap;
      }	
   }      
}

/************************************************************************************************
 * Function name: reverse_text()								*
 * Description: Takes a user string of text and prints it in reverse.				*
 * Parameter: Pointer c-string									*
 * Pre-condition: Input from user in the form of a string.					*
 * Post-condition: Changes the text copy to print in reverse.					*
 * **********************************************************************************************/
void reverse_text(char* str) {

   for(int i = strlen(str); i >= 0; i--) {
	cout << str[i];
   }
   cout << endl;
}
//Function prototype, description later on.
int counting_function(char* str, string words);

/****************************************************************************************************************
 * Function name: word_counter()										*
 * Description: This begins the process of counting the desired words from the user. This will ask for how	*
 * 		many words they want to search for and which words. Stores them in an array.			*	
 * Parameter: Pointer c-string											*
 * Pre-condition: Must have a string of text input to scan through.						*
 * Post-condition: This function prints the counter generated from another function, counting_function.		*
 * **************************************************************************************************************/
void word_counter(char* str) {

   int how_many_words = 0, check = 1;
   int counted = 0;

   do {
      cout << "How many words would you like to count?: ";
      cin >> how_many_words;
      	if(how_many_words < 0) {
	   	check = 0;
		cout << "Not an acceptable value, try again." << endl;
	}
   } while (check == 0);

   string* stored_words = new string[how_many_words];
   
   for (int i = 0; i < how_many_words; ++i) {
      	cin.ignore();
      	cout << "Word to search and count: ";
      	getline(cin, stored_words[i]);
   }

   for (int i = 0; i < how_many_words; ++i) {
      cout << stored_words[i] << ": " << counting_function(str, stored_words[i]) << endl;
   }
   delete[] stored_words;
   stored_words = NULL;
}

/************************************************************************************************************************
 * Function name: counting_function()											*
 * Description: This function is called in the word_count function and uses the array to count how many desired words	*
 * 		occur in the text.											*
 * Parameter: Pointer c-string, string											*
 * Pre-condition: Pass into this function the user's purged text and the array of strings for the words.		*
 * Post-condition: Returns a count for the word it is searching for.							*
 * **********************************************************************************************************************/
int counting_function(char* str, string words) {

   int count = 0, scan = 0;

   for(int i = 0; i < strlen(str); ++i) {
      	if(str[i] == words[scan]) {
	   	scan++;
	}
	else { 
		scan = 0;
	}
	if(scan == words.length()) {
	   	scan = 0;
		count++;
	}
   }
   return count;
}

/************************************************************************************************
 * Function name: main()									*
 * Description: The command center of the entire program. Takes in initial user desire and loops*
 * 		through the processes if the user desires to go through it again.		*
 * Parameter: N/A										*
 * Pre-condition: N/A										*
 * Post-condition: N/A										*
 * **********************************************************************************************/
int main() {

   cout << "THE TEXT SURGEON" << endl;

   char* user_paragraph = new char[1024];
   user_paragraph[1023] = '\0';

   char* copy_paragraph = new char[2024];
   copy_paragraph[1023] = '\0';

   int answer = 0;   

   do {

   cout << "Enter a sentence or paragraph: ";
   cin.getline(user_paragraph, 1023);
	
   	int a = 1;
   	
	do {

	   int check = 1;
	   int selection = 0;

	   do {

	      strcpy(copy_paragraph, user_paragraph);

	   	cout << "1. Letter swap" << endl;
		cout << "2. Text reverse" << endl;
		cout << "3. Word counter" << endl;
		cout << "Select an option, 1, 2 or 3: ";
		cin >> selection;
			if(selection < 1 || selection > 3) {
			   	check = 0;
				cout << "Incorrect selection." << endl;
			}
	   } while (check == 0);
	   
	   if(selection == 1) {
	      	replace_letter(copy_paragraph);
		cout << copy_paragraph << endl;
	   }
	   if(selection == 2) {
	      	reverse_text(copy_paragraph);
	   }
	   if(selection == 3) {
	      	char* purged_para = purge_string(user_paragraph);
	      	word_counter(purged_para);
		delete[] purged_para;
		purged_para = NULL;
	   }
	   
	   do {
	      	check = 1;
	   	cout << "Would you like to choose a different option?(1-yes,0-no): ";
	   	cin >> a;
			if(a != 1 && a != 0) {
			   cout << "Incorrect selection." << endl;
			   check = 0;
			}
	   } while (check == 0);

	} while (a == 1);
		
   cout << "Do you want to use Text Surgeon again?(1-yes, 0-no): ";
   cin >> answer;
	
   cin.ignore();
   cin.clear();

   } while (answer == 1);

   delete[] user_paragraph;
   user_paragraph = NULL;
   delete[] copy_paragraph;
   copy_paragraph = NULL;


return 0;
}
