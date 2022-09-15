#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <regex>

using namespace std;

int main()
{
    string row;
    ifstream file;

    int filerowcount = 0;
    file.open("json.csv");
    while (file.is_open())
    {
        // complete file row
        while (getline(file, row))
        {
            // file >> row;
            stringstream sstream(row);
            string column;
            string tweet = "Arutz7: Watch: CCTV Shows The Moment Powerful Earthquake Struck in Chile: Officer workers scatter as 8... http://t.co/6XMwL5hSuL #israel";
            cout << "tweet" << tweet << endl
                 << endl;
            int count = 0;
            // each csv unit
            while (!sstream.eof())
            {

                // if (count >= 28)
                // {
                //     getline(sstream, column, ',');
                // }
                // if (sstream.peek() == '"')
                // {
                //     // https://stackoverflow.com/questions/35639083/c-csv-row-with-commas-and-strings-within-double-quotes
                //     sstream >> quoted(column);
                //     string discard;
                //     getline(sstream, discard, ',');
                // }
                // else
                // {
                getline(sstream, column, ',');
                // }

                // the start of the json
                // if (count >= 30)
                //{
                // cout << column << endl;
                size_t endOffsetNum, startOffsetNum;
                regex reg("[^a-zA-Z0-9:]");
                //  stringstream result;
                // cout << "column " << column << endl;
                if (column.find("endOffset") != string::npos)
                {
                    cout << "endOffset = ";

                    if (column.find("annotation") != string::npos)
                    {
                        string s = column.substr(column.length() / 1.4);
                        // cout << s << endl;
                        column = s;
                    }

                    string endOffsetOutput = regex_replace(column, regex("[^0-9]*([0-9]+).*"), string("$1"));
                    // cout << endOffsetOutput << endl;
                    stringstream ss(endOffsetOutput);
                    ss >> endOffsetNum;
                    cout << endOffsetNum << endl;
                }
                else if (column.find("label") != string::npos)
                {
                    cout << "label found = " << column << endl;
                }
                else if (column.find("startOffset") != string::npos)
                {
                    cout << "startOffset = ";

                    string startOffsetOutput = regex_replace(column, regex("[^0-9]*([0-9]+).*"), string("$1"));
                    // cout << startOffsetOutput << endl;

                    stringstream ss(startOffsetOutput);
                    ss >> startOffsetNum;
                    cout << startOffsetNum << endl;

                    string str = tweet.substr(startOffsetNum, endOffsetNum - startOffsetNum);
                    cout << str << endl
                         << endl;
                    ;
                }
                //}
                count++;
            }
            cout << "column count = " << count << endl;
            return 0;
        }
    }
}