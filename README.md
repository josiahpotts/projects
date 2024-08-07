# projects

4/7/2023 - EarlyCPP directory added
The files within EarlyCPP are individual games that include checkers, text surgeon, and twentyone.
Use:
  - Download file into desired directory
  - Compile using line 'g++ filename.cpp -o filename'
  - Run using './filename'

4/9/2023 - Traceroute directory added
The file within Traceroute is icmpHelperLibrary.py and uses socket programming to run a traceroute.
Use:
  - Download file into desired directory
  - At the bottom of the file, uncomment whatever websites for desired trace, OR
  - Choose your own Ping or Trace by typing in icmpHelperPing.sendPing(#DESIRED PING DESTINATION), or icmpHelperPing.traceRoute(#DESIRED PING DESTINATION)

4/10/2023 - LCS-EditDistance added
The files within LCS-EdiDistance run a couple popular algorithmic problems known as Longest Common Segment and Edit Distance. These are completed with dynamic programming. The text files used for examples are COVID data files.
Use:
  - Download all files into desired directory.
  - In terminal type 'python3 lcs-editDistance.py COVID-OmicronBA1.txt COVID-RefDec19.txt'
  - Results are printed in the console.
  
4/12/2023 - SimpleClientServerChat added
There are two files within this directory, client.py and server.py, and they use sockets for a simple chatting program.
Use:
  - Download both files into the same desired directory.
  - Run both files (order doesn't matter)
  - Wait for the socket connection to be established (shouldn't take long)
  - Once the client is connected to the server (localhost), the client will be prompted to begin the chat. 
  - Alternate from the client terminal and the server terminal to chat.
  
4/13/2023 - BasicReactWebApp directory added
These files will run a basic web application, utilizing React, on your localhost.
Use:
  - Must have Node installed.
  - Download the full directory (recommended)
  - Open terminal and follow these steps:
```bash
$> cd BasicReactWebApp
$> npm install
$> npm start
```
      
4/16/2023 - MaxSubarray directory added
These directories and files run different algorithmic approaches to the maximum subarray problem.
Use:
  - Download desired directory including the .py file and all .txt files.
  - Using the terminal within the chosen directory:
      1. Type: python max_subarray_algs.py filename.txt (Note: enumeration and iteration will take a significant amount of time to complete - O(n^3))
      2. Example usage: python max_subarray_algs.py num_array_500.txt
      
4/17/2023 - HuffmanCode directory added
Implemented Huffman Code using the Gettysburg Address as an example.
Use:
  - Download the directory
  - Run huffman.py
  - Note: if desiring to encode a different text document, simply add it to the directory and replace the file being read within the python file.
  - Note: Cost is indicated as TODO. Will not calculate the cost of the code at this time.
  
4/19/2023 - CoffeeStoreDatabaseProject directory added
Portfolio project from CS340 with help of co-author, Tyler Eto.
Use:
```bash
# express rest api
$> cd rest
$> nvm use v14.17.6
$> npm install
$> node app.js
```
```bash
# react ui
$> cd ui
$> nvm use v14.17.6
$> npm install
$> npm start
```
  - Note: phpMyAdmin database no longer accessable on school servers. Will edit to new database in upcoming versons.
  
4/20/2023 - MinHeap directory added
This is a portfolio project from CS261 Data Structures -- Test code was provided by instructor.
Use:
  - Download directory.
  - Run min_heap.py (test cases already established in the file)
  
4/23/2023 - Trees directory added
This holds files with AVL and BST data structures, as well as a queue and stack file for use within those trees.
Use:
  - Download directory.
  - Run either avl.py or bst.py individually (test cases already established in the file)
  
4/26/2023 - HashMap directory added
This is a portfolio project from CS261 Data Structures -- Test code was provided by instructor.
Use:
  - Download directory.
  - Run hash_map_oa.py to see Open Addressing approach tests.
  - Run hash_map_sc.py to see Linked List approach tests.
  
4/29/2023 - RDT directory added
This is a portfolio project from Networking class -- Reliable Data Transfer
Use:
  - Download directory.
  - "dataToSend" in rdt_main.py variable set to Gettysburg Address, comment out and put whatever string you want, or run as is.
  - Run rdt_main.py
  - Notes: segment.py and unreliable.py represent simulated packet segments and an unreliable network channel.(Provided by instructor)

6/26/2024 - SmallShell directory added
This is a portfolio project from Operating Systems II -- I am the author of entire code.
Use: 
  - Download directory.
  - Run these commands:
      `gcc -o smallsh smallsh.c`
      `./smallsh`
What can I do with this small shell?
    1. The `cd`, `exit`, and `status` commands (status will show the status code of the last command).
    2. All other linux commands will be run through the bash shell.
