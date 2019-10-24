//C++ version of wordplayer program
// Copyright Leah Pillsbury 2018 leahp@bu.edu

// This program receives a list of possible words as input.
// Then the user enters in the command line the letters that can be used
// and the number of letters that should be used in the words.

// Based on the number of letters that should be used, the word list
// should only be searched for words that are that length.

#include <math.h>
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <map>
#include <algorithm>

using std::cin;
using std::string;
using std::cout;
using std::vector;
using std::ifstream;
using std::map;
using std::sort;


void PrintOutput(vector <string> wordlist);
long LCN (int L, int N);
long factorial(int n);
vector <string> letter_method(string letterchoices, vector <string> possible_words, int wordsize); 
//vector <string> anagram_method();


void PrintOutput(vector <string> wordlist){
    // Print out all possible words, one per line, followed by a period
    int len=wordlist.size();
    for(int i=0; i<len; i++){
        cout<<wordlist[i]<<'\n';
    }
    cout<<"."<<'\n';
}

// The factorial and LCN functions work but are only useful for choosing 
// between the anagram method and the letter method.
// I ran out of time and chose letter method only.
// I left these functions here in case I have time to add the anagram method 
// to this function later

/*long factorial(int n){
    int k=1;
    for (int i=1; i<=n;i++){
        k=k*i;
    }
    return k;
}

long LCN(int L, int N){
    // Compute n choose r and return the result
    long numer, denom=1, k;
    numer=factorial(L);
    denom = factorial(N)*factorial(L-N);
    return numer/denom;
}*/

vector <string> letter_method(string letterchoices, vector <string> possible_words, int wordsize){
    // Only check the size words I want for the letters I have."
    // If there are a lot of number combinations, then look to see if the words match the letters.
    // In the dictionary with the key that has the right number of words all_words[N]
    // Loop through each word
    // Compare the letters in the word I'm going for to the letters I have. 
    // If all the letters in the dictionary word are in my letter set, then put the word in answer_words
    vector <string> answer_words={};
    int numpw=possible_words.size(), numlet=letterchoices.size();
    char letter;
    int findletter;
    string local_letters;
    for(int i=0; i<numpw; i++){      // loop through each word in possible_words array
        int counter=0;
        local_letters=letterchoices;
        string checkword=possible_words[i];
        for(int j=0; j<wordsize;j++){  // loop through all the letters in the word
            // If the letter in the word bank is also in the word, continue and
            // remove that letter from the bank.
            findletter=local_letters.find(checkword[j]);
            if(findletter!=string::npos){
                local_letters.erase(findletter,1);
                counter=counter+1;
                continue;
            }
            else{
                break;
            }
        }
        if(counter==wordsize){
            answer_words.push_back(possible_words[i]);
        }
    }
    // Need to sort answer_words in alphabetical order
    sort(std::begin(answer_words), std::end(answer_words));
    return answer_words;
}


  /*  for word in all_words[N]:
        i=0
        local_L=list(L)
        for letter in word:
            if letter in local_L:
                local_L.remove(letter)
                i=i+1
                continue
            else:
                break
        if i==N:
            answer_words.append(word)
    answer_words.sort()
    return answer_words */

int main(int argc, char* argv[]){
    string curr_word, letterchoices;
    map<int,vector<string>> all_words;  // This is for letter way
    map<vector<char>,string> anagram;   // This is for anagram way
    vector <string> s, wordlist;
    int N;
    for(int i=1; i<30; i++){
        all_words[i]=s;
    }

    string filename=argv[1]; //is the file name
    ifstream infile;
    infile.open(filename);
    while (getline(infile,curr_word)) {
        int x=curr_word.length();
        all_words[x].push_back(curr_word);
    }
    infile.close();
    

    while (true){
        cin>>letterchoices;
        cin>>N;
        if(N==0){
            break;
        }
        // Given time constraints in writing code,
        // I decided to just use the letter way since it is faster for
        // more cases anyways
        // I left the other function definitions in case I have time later
        // to add the anagram_method
        // send only the list of words with the right number of letters to the letter_method function
        wordlist=letter_method(letterchoices, all_words[N], N);
        PrintOutput(wordlist);
    }
    return 0;
}



