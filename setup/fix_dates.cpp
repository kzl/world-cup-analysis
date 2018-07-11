#include <cstdio>
#include <fstream>
#include <iostream>
#include <regex>
using namespace std;

int main() {
	ifstream fin;
	fin.open("../world-cup-data/WorldCupMatches.csv");

	ofstream fout;
	fout.open("../world-cup-data/WorldCupMatchesFixed.csv");

	string line;
	regex june("June");
	regex july("July");
	while (getline(fin, line)) {
		line = regex_replace(line, june, "Jun");
		line = regex_replace(line, july, "Jul");
		fout << line << "\n";
	}

	fclose(stdin);
	fclose(stdout);
}
