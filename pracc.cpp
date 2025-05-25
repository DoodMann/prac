#include <iostream>
using namespace std;

int main() {
    cout << "What day of the week is it? (1-7): ";
    int day;
    cin >> day;
    cin.ignore();

    string days[] = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};

    if (day >= 1 && day <= 7) {
        cout << days[day - 1] << endl;
    } else {
        cout << "Invalid day!" << endl;
    }
}