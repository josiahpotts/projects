/*Author: Josiah Potts
 *Project: Project 3
 *Last Modified: 5/24/2023
 *Description: This is a small shell that has most operational capabilities as a bash shell.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <signal.h>
#include <ctype.h>
#include <fcntl.h>

// Constant definitions
#define MAX_COMMAND_LENGTH 2048
#define MAX_ARGS 512

// Global variables
pid_t lastForegroundPid;
pid_t lastBackgroundJobPid;
pid_t childPidArray[100];

int lastForegroundExitStatus = 0;
int lastForegroundTerminatingSignal = 0;

char environmentDirectory[MAX_COMMAND_LENGTH];
char currentDirectory[MAX_COMMAND_LENGTH];

int numChildren = 0;
int foregroundMode = 0; // 0 for normal mode, 1 for foreground mode

/************************************************************************************************************************
 * cdCommand handles the "cd" functionality of a shell. It accepts the command alone, which will change to the directory*
 * that the program was started in, else the path will be considered.							*
 * 															*
 * Parameters: String (path of directory)										*	
 * Returns: Nothing
 * *********************************************************************************************************************/
void cdCommand(const char* path) {

   	// Handle "cd" alone means going to home directory where smallsh.c was run
	if ((path == NULL || strlen(path) == 0) || (strcmp(path, "&") == 0 )) {
		
		getcwd(currentDirectory, MAX_COMMAND_LENGTH);

	   	environmentDirectory[sizeof(environmentDirectory) - 1] = '\0';
		currentDirectory[sizeof(currentDirectory) - 1] = '\0';

	   	if (strcmp(environmentDirectory, currentDirectory) == 0) {
		   	return;
		}
		else if (chdir(environmentDirectory) != 0) {

			write(STDOUT_FILENO, "change to home directory failed\n", 32);
		};	   
	}
	// Handle changing directory using the path
	else {

		if (chdir(path) != 0) {

			write(STDOUT_FILENO, "change to path directory failed\n", 32);
		};
	};
};

/************************************************************************************************************************
 * statusCommand checks the status of last foreground process and prints a message to the console for the user. 	*
 * 															*
 * Parameters: Nothing													*
 * Returns: Nothing													*
 * ******d***************************************************************************************************************/
void statusCommand() {

	if (WIFEXITED (lastForegroundExitStatus)) {
	
	   	int exitStatus = WEXITSTATUS(lastForegroundExitStatus);
		printf("exit value %d\n", exitStatus);
	}
	else {
		
	   	int exitStatus = WIFSIGNALED(lastForegroundExitStatus);
	   	printf("terminated by signal %d\n", exitStatus);
	};
};

/************************************************************************************************************************
 * killChildProcesses helper function mainly for exitCommand(), checking last background job and kills it,		*
 * then waits for the remaining child processes to be killed.								*
 * 															*
 * Parameters: Nothing													*
 * Returns: Nothing 													*
 * *********************************************************************************************************************/
void killChildProcesses() {

   	// Send termination signal to last background job
	if (lastBackgroundJobPid > 0) {

		kill(lastBackgroundJobPid, SIGTERM);
	};
	// Wait for remaining child processes to be terminated
	while (1) {

		pid_t terminatedPid = waitpid(-1, NULL, WNOHANG);

		if (terminatedPid <= 0) {

			break;
		};
		//HERE HANDLE TERMINATION OF CHILD PROCESS IF NEEDED
	};
};

/************************************************************************************************************************
 * exitCommand handles the "exit" command if entered in the command line						*
 * 															*
 * Parameters: Nothing													*
 * Returns: Nothing (kills children processes and exits program)							*
 * *********************************************************************************************************************/
void exitCommand() {

	killChildProcesses();
	exit(0);
};

/************************************************************************************************************************
 * workOnBuiltInCommand handles exit, status, and cd commands manually							*
 * 															*
 * Parameters: Array of command arguments										*
 * Returns: bool Int													*
 * *********************************************************************************************************************/
int workOnBuiltInCommand(char* arguments[]) {

   	int wasBuiltIn = 0;

	// exit
	if ((strcmp(arguments[0], "exit")) == 0 && (arguments[1] == NULL || (strcmp(arguments[1], "&") == 0))) {
		
	   	wasBuiltIn = 1;
		exitCommand();
	}
	// status
	else if ((strcmp(arguments[0], "status")) == 0 && (arguments[1] == NULL || (strcmp(arguments[1], "&") == 0))) {

	   	wasBuiltIn = 1;
		statusCommand();
	}
	// cd (with no args or & as arg)
	else if ((strcmp(arguments[0], "cd")) == 0 && (arguments[1] == NULL || (strcmp(arguments[1], "&") == 0))) {
	      
	   	wasBuiltIn = 1;
		cdCommand(arguments[1]);	
	}
	// cd (with arg)
	else if ((strcmp(arguments[0], "cd")) == 0 && (arguments[1] != NULL && (strcmp(arguments[1], "&") != 0))) {
		
	   	wasBuiltIn = 1;
		cdCommand(arguments[1]);
	};
   	return wasBuiltIn;
};

/************************************************************************************************************************
 * expansionOfVariable handles the variable expansion of the $$ if the user used it in their command input. It will be	*
 * replaced and cat into the memory string in the same position as the smallsh pid.					*
 *															*
 * Parameters: input String												*
 * Returns: Nothing (but memory changed in input)									*
 ***********************************************************************************************************************/
void expansionOfVariable(char* input) {

   	char* variable = "$$";
	char pidString[16];
	snprintf(pidString, sizeof(pidString), "%d", getpid());

	// Search for "$$" variable match in the input
	char* variableMatch = strstr(input, variable);
	while (variableMatch != NULL) {
	   
   		// Get size of memory before and after the expansion	   
	   	size_t variableLength = strlen(variable);
		size_t pidLength = strlen(pidString);
		size_t afterLength = strlen(variableMatch + variableLength);

		// Expand memory in the center by moving the after length to the end of pid
		memmove(variableMatch + pidLength, variableMatch + variableLength, afterLength + 1);
		memcpy(variableMatch, pidString, pidLength);

		variableMatch = strstr(variableMatch + pidLength, variable);
	};
};

/************************************************************************************************************************
 * ignoreLeadingSpaces is a helper function to remove any extraneous spacebar characters at the beginning of a command  *
 * 															*
 * Parameters: string pointer												*
 * Returns: nothing (but modifies data at the pointer address)								*
 ***********************************************************************************************************************/
void ignoreLeadingSpaces(char** str) {

	while(**str && isspace((unsigned char)**str)) {

		(*str)++;
	};
};

/************************************************************************************************************************
 * checkOutputRedirection checks for > and >> in the command and redirects to the file name, creating it if need be     *
 * 															*
 * Parameters: pointer to arguments, int number of args									*
 * Returns: pointer to a file name											*
 ***********************************************************************************************************************/
char* checkOutputRedirection(char* arguments[], int numOfArgs, int background, int newNumOfArgs) {

   	// Check if checkInputRedirection() changed the number of args
	if (numOfArgs != newNumOfArgs) {

		numOfArgs = newNumOfArgs;
	};
   	int index = -1;

	// Find index where symbol was typed
	for (int i = 0; i < numOfArgs; i++) {

		if (strcmp(arguments[i], ">") == 0 || strcmp(arguments[i], ">>") == 0) {
		
		   	index = i;
			break;
		};
	};
	char* outputFile = arguments[index + 1]; // File name
	if (index != -1) {	

		// Handle input redirection
		int fd;
		if (strcmp(arguments[index], ">") == 0) {

			// Truncate file if exists
			fd = open(outputFile, O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IWGRP| S_IXGRP | S_IROTH, 0760);
		}
		else {

			// Append to file if exists, else create it
			int fd = open(outputFile, O_WRONLY | O_CREAT | O_APPEND, S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IWGRP| S_IXGRP | S_IROTH, 0760);
		};
		if (fd == -1) {

		   	perror("error opening output file");
			exit(1);
		};

		// dup2() for redirection
		dup2(fd, STDOUT_FILENO);
	       	close(fd);

		memmove(&arguments[index], &arguments[index + 2], (numOfArgs - index - 1) * sizeof(char*));
		numOfArgs -= 2;	
	}
	// Handle background redirection
	else if (background == 1) {
	   	
	  	int fd = open("/dev/null", O_WRONLY); 
	   	dup2(fd, STDOUT_FILENO);
		close(fd);
	};
	return outputFile;
};

/************************************************************************************************************************
 * checkInputRedirection checks for < in the command and redirects to the file name, creating it if need be  	        *
 * 															*
 * Parameters: pointer to arguments, int number of args									*
 * Returns: pointer to a file name											*
 ***********************************************************************************************************************/
int checkInputRedirection(char* arguments[], int numOfArgs, int background) {
	
   	int index = -1;

	// Find index where symbol was typed
	for (int i = 0; i < numOfArgs; i++) {

		if (strcmp(arguments[i], "<") == 0) {
			
		   	index = i;
			break;
		};
	};
	char* inputFile = arguments[index + 1]; // File name
	if (index != -1) {	

	   	// Handle input redirection
		int fd = open(inputFile, O_RDONLY, S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IWGRP| S_IXGRP | S_IROTH, 0760);
		if (fd == -1) {

			perror("error opening input file");
			exit(1);
		};
		dup2(fd, STDIN_FILENO);
	       	close(fd);

		memmove(&arguments[index], &arguments[index + 2], (numOfArgs - index - 1) * sizeof(char*));
		numOfArgs -= 2;	
		}
	// Handle background redirection
	else if (background == 1) {
		
	   	int fd = open("/dev/null", O_RDONLY); 
	   	dup2(fd, STDIN_FILENO);
		close(fd);
	};
	
	return numOfArgs;
};
 
/************************************************************************************************************************
 * checkBackgroundProcesses loops through the stored child process ID array to see if they are finished  	        *
 * 															*
 * Parameters: Nothing													*
 * Returns: Nothing													*
 ***********************************************************************************************************************/
void checkBackgroundProcesses() {

	int i = 0;
	int status;

	// Find the next PID to start at for checking
	for (int j = 0; j < numChildren; j++) {

		if (childPidArray[j] == 0) {

			i++;
		};
	};
	
	// PROBLEM IM HAVING!!! ALL SIGS ARE TERMINATING 11, BUT I DONT BELIEVE IT!
	for (i; i < numChildren; i++) {

		if (childPidArray > 0) {

		   	// Check process completion
			pid_t result = waitpid(childPidArray[i], &status, WNOHANG);
			if (result == -1) {

			   	return;
			   	//perror("check background process error");
				//exit(1);
			}
			else if (result > 0) {

				// Process was complete
				if (WIFEXITED(status)) {
					
				   	// Normal exit
					int exitStatus = WEXITSTATUS(status);
					printf("background pid %d is done: exit value %d\n", childPidArray[i], exitStatus);
				}
				else if (WIFSIGNALED(status)) {

				   	// Terminated
					int terminationSignal = WTERMSIG(status);
					printf("background pid %d is done: terminated by signal %d\n", childPidArray[i], terminationSignal);
				};
				// Clean up child process
				childPidArray[i] = 0;
			};
		};
	};
};

/************************************************************************************************************************
 * catchSIGINT is called when a SIGINT is caught and handles it in the parent process			   	        *
 * 															*
 * Parameters: Int signal type												*
 * Returns: Nothing													*
 ***********************************************************************************************************************/
void catchSIGINT(int signo) {

	char* message = "Foreground child process terminated by signal: 2\n";
	write(STDOUT_FILENO, message, 50);
};

/************************************************************************************************************************
 * catchSIGTSTP is called when a SIGTSTP is caught and handles it in the parent process			   	        *
 * 															*
 * Parameters: Int signal type												*
 * Returns: Nothing													*
 ***********************************************************************************************************************/
void catchSIGTSTP(int signo) {
	
   	if (foregroundMode == 0) {

		foregroundMode = 1;
		write(STDOUT_FILENO, "\nEntering foreground-only mode (& is now ignored)\n", 49);
	}
	else {

		foregroundMode = 0;
		write(STDOUT_FILENO, "\nExiting foreground-only mode\n", 30);
	}
};

int main() {

   struct sigaction SIGINT_action = {0}, SIGTSTP_action = {0}, ignore_action = {0};

   getcwd(environmentDirectory, MAX_COMMAND_LENGTH);

   // Settin up handler for CTRL+Z to go in and out of foreground only mode
   SIGTSTP_action.sa_handler = catchSIGTSTP;
   sigfillset(&SIGTSTP_action.sa_mask);
   SIGTSTP_action.sa_flags = SA_RESTART;
   sigaction(SIGTSTP, &SIGTSTP_action, NULL);

   // Parent process will ignore the CTRL+C signal
   ignore_action.sa_handler = SIG_IGN;
   sigaction(SIGINT, &ignore_action, NULL);

   // Set up SIGINT handler for child process
   SIGINT_action.sa_handler = catchSIGINT;
   sigfillset(&SIGINT_action.sa_mask);
   SIGINT_action.sa_flags = 0;



   // Small shell command loop
   while(1) {	

      	char prompt[] = ": ";
	char input[MAX_COMMAND_LENGTH];
	char *arguments[MAX_ARGS];
	ssize_t bytesRead;	

	// Periodically check on child processes that may have finished
	checkBackgroundProcesses();

	// Prompt for user to put in command
	write(STDOUT_FILENO, prompt, sizeof(prompt) - 1);	
	bytesRead = read(STDIN_FILENO, input, sizeof(input));

	if (bytesRead == -1) {
		perror("read");
		break;
	};

	// Add null term to end of the user input
	input[bytesRead] = '\0';
	
	// Remove newline if present in the user input
	if (bytesRead > 0 && input[bytesRead - 1] == '\n') {

		input[bytesRead - 1] = '\0';
		bytesRead--;
	};
	
	// Expand the $$ input into the smallsh pid
	expansionOfVariable(input);

	

	// Token the input with spaces
	int numOfArgs = 0;
	char *token = strtok(input, " ");

	while (token != NULL && numOfArgs < MAX_ARGS) {

	   	ignoreLeadingSpaces(&token);
		arguments[numOfArgs++] = token;
		token = strtok(NULL, " ");
	};

	arguments[numOfArgs] = NULL;

	// Check for blank lines and commands
	int commentedBool = 0;
	int i = 0;
	if (numOfArgs == 0 || input[0] == '#') {

		continue;
	} 
	else {
		while (1) {

			if (input[i] == ' ') {

			   	i++;
				continue;
			}
			else if (input[i] == '#') {

				commentedBool = 1;
			};
			break;
		};
		if (commentedBool == 1) {

			continue;
		};
	};
	
	// Check if command is built in, and resolve it if it is
	if (workOnBuiltInCommand(arguments) == 1) {
		
	   	continue;
	};

	// Let's tackle the other commands...
	
	// Check for run in background argument
	int runInBackground = 0;
	if (numOfArgs > 0 && strcmp(arguments[numOfArgs - 1], "&") == 0) {
	
	   	// Check for foreground only mode and if so then ignore running things in background
	   	if (foregroundMode == 0) { 
		
		   	runInBackground = 1;
		};
		int arg;
		for (arg = 0; arguments[arg] != NULL; arg++) {

			if (arguments[arg + 1] == NULL) {
				
				arguments[arg] = NULL;
				numOfArgs -= 1;
				break;
			};
		};
	};
	// Fork the new process
	pid_t spawnPid = -5;
	
	spawnPid = fork();
	int childExitMethod = -5;

	if (spawnPid == -1) {
		
	   	perror("Hull Breach!\n");
		exit(1);
	}
	else if (spawnPid == 0) {
		
	   	// Child process


	   	// Check redirection
	   	int newNumOfArgs = checkInputRedirection(arguments, numOfArgs, runInBackground);
		checkOutputRedirection(arguments, numOfArgs, runInBackground, newNumOfArgs);
		
		// Call execvp()
	   	if (execvp(arguments[0], arguments) == -1) {
 
			perror("Error executing command");
			exit(1);
		};
	}
	else if (spawnPid > 0) {
	
	   	// Parent process
		
	   	// Background
		if (runInBackground == 1) {
		
		   	childPidArray[numChildren] = spawnPid;
			numChildren++;
		}
		// Foreground
		else {

			fflush(stdout);

			waitpid(spawnPid, &lastForegroundExitStatus, 0);
		};
	}
	else {
		
	   	perror("Error in fork() process\n");
		exit(1);
	};
	lastForegroundPid = spawnPid;

	//Clear memory of input
	memset(input, 0, sizeof(input));
    };
   return 0;
};

