#include <iostream>
#include <string>
using namespace std;

int main() {
  int age;
  string firstName;
  string lastName;
  string graduated;
  cout << "What's your first name? ";
  getline(cin, firstName);
  cout << "How about your last name? ";
  getline(cin, lastName);
  cout << "How old are you? ";
  cin >> age;
  cin.ignore();
  cout << "Indicate when you have graduated high school. Leave blank if not applicable: ";
  getline(cin, graduated);
  string name = firstName.append(" ").append(lastName);
  cout << "Hello, " << name << "! You're " << age << " years old. "
       << (graduated.empty() ? "You haven't graduated yet. Good luck!" : "You graduated in " + graduated + ". Congratulations!") 
       << endl;


  if (age < 18) {
    cout << "Eligible to vote? No." << endl;
    } else if (age >=18 && age < 21) {
    cout << "Eligible to vote? Yes, but not to drink alcohol." << endl;
  } else {
    cout << "Eligible to vote? Yes, and you can also drink alcohol." << endl; 
    }

  

  cout << "Thank you for your input!" << endl;
}


