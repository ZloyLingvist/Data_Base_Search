#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>

using namespace std;

/*double levenshtein(string a,string b){
unsigned int a_len, b_len, x, y, lastdiag, olddiag;
a_len = a.length();
b_len = b.length();

unsigned int column[a_len+1];

for (y = 1; y <= a_len; y++)
column[y] = y;
for (x = 1; x <= b_len; x++) {
column[0] = x;
for (y = 1, lastdiag = x-1; y <= a_len; y++) {
olddiag = column[y];
column[y] = std::min(std::min(column[y] + 1, column[y-1] + 1), lastdiag + (a[y-1] == b[x-1] ? 0 : 1));
lastdiag = olddiag;
}
}

int general_len=a_len+b_len;
double result=(general_len-column[a_len])/(float)general_len;
return result;
}*/


double levenshtein(string source, string target) {

	// Step 1
	//https://www.talkativeman.com/levenshtein-distance-algorithm-string-comparison/
	const int n = source.length();
	const int m = target.length();
	if (n == 0) {
		return m;
	}
	if (m == 0) {
		return n;
	}

	vector<vector<int> > matrix;
	matrix.resize(n + 1);

	for (int i = 0; i <= n; i++) {
		matrix[i].resize(m + 1);
	}

	// Step 2

	for (int i = 0; i <= n; i++) {
		matrix[i][0] = i;
	}

	for (int j = 0; j <= m; j++) {
		matrix[0][j] = j;
	}

	// Step 3

	for (int i = 1; i <= n; i++) {

		const char s_i = source[i - 1];

		// Step 4

		for (int j = 1; j <= m; j++) {

			const char t_j = target[j - 1];

			// Step 5

			int cost;
			if (s_i == t_j) {
				cost = 0;
			}
			else {
				cost = 1;
			}

			// Step 6

			const int above = matrix[i - 1][j];
			const int left = matrix[i][j - 1];
			const int diag = matrix[i - 1][j - 1];
			int cell = std::min(above + 1, std::min(left + 1, diag + cost));

			// Step 6A: Cover transposition, in addition to deletion,
			// insertion and substitution. This step is taken from:
			// Berghel, Hal ; Roach, David : "An Extension of Ukkonen's 
			// Enhanced Dynamic Programming ASM Algorithm"
			// (http://www.acm.org/~hlb/publications/asm/asm.html)

			if (i>2 && j>2) {
				int trans = matrix[i - 2][j - 2] + 1;
				if (source[i - 2] != t_j) trans++;
				if (s_i != target[j - 2]) trans++;
				if (cell>trans) cell = trans;
			}

			matrix[i][j] = cell;
		}
	}

	// Step 7
	double result = (n + m - matrix[n][m]) / (float)(n + m);
	return result;
}


int main() {
	ifstream infile("theorem_list.txt");
	if (infile.is_open()) {
		cout << "open is succesfull";
	}
	else {
		cout << "problem" << endl;
		return 0;
	}

	string str;
	vector<string> myvec;
	vector<double> temp_vector;
	vector<vector<double> > result_vector;

	while (std::getline(infile, str)) {
		if (str.size()>0) {
			myvec.push_back(str);
		}
	}

	infile.close();

	for (size_t i = 0; i<myvec.size(); i++) {
		for (size_t j = 0; j<myvec.size(); j++) {
			temp_vector.push_back(levenshtein(myvec[i], myvec[j]));
		}

		result_vector.push_back(temp_vector);
		temp_vector.clear();
	}


	ofstream outfile("result_list_levenshtein.txt");
	for (size_t i = 0; i<result_vector.size(); i++) {
		for (size_t j = 0; j<result_vector[i].size(); j++) {
			outfile << result_vector[i][j] << " ";
		}

		outfile << endl;
	}

	outfile.close();
	system("pause");
	return 0;
}
