#include <iostream>
using namespace std;

const string telPats[4] = {"TTAGGG","GGGATT","AATCCC","CCCTAA"};

int getTelLimit(string frag, string pat){
	if(frag.size() >= pat.size()){
		return((frag.size() - pat.size()) + 2);
	}else{
		return 0;
	}
}

int telSubStr(const string frag,const string pat,const int i){
	if(frag.substr(i,pat.size()) == pat) return true;
	return false;
}

bool isTelomeric(const string frag){
    for(int i = 0; i < sizeof(telPats);i++){
    	int res = frag.find(telPats[i],0);
    	cout << res;
    	if(res != -1){
    		return true; 
    	}
    } 
    return false;
}
		
int main(int argc, char **argv) {
	using namespace std;
	/*
	string pattern = "TTAGGG";
	int count = 1;
	while(count < pattern.size())
		printf("%c",pattern[count++]);
	return 0;*/

	string frag = argv[1];
	isTelomeric(frag);
}

