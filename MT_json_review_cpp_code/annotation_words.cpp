// early code for checking annotations values from mechanical turk
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
    // get annotation start and end values from this csv file - only contains one persons tags
    file.open("annotation.csv");
    while (file.is_open())
    {
        // complete file row
        while (getline(file, row))
        {
            // file >> row;
            stringstream sstream(row);
            string column;
            // add the string of the current tweet here
            string tweet = "RT @NVR_Photo: Damage at #NapaPostOffice from #NapaQuake http://t.co/h266KkVExK";
            cout << "tweet" << tweet << endl
                 << endl;
            int count = 0;
            // each csv unit
            while (!sstream.eof())
            {
                getline(sstream, column, ',');

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