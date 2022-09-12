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
    file.open("Batch_4820459_batch_results.csv");
    while (file.is_open())
    {
        // complete file row
        while (getline(file, row))
        {
            // file >> row;
            stringstream sstream(row);
            string column;
            string tweet;
            int count = 0;
            // each csv unit
            while (!sstream.eof())
            {
                string csvElement;
                if (count >= 28)
                {
                    getline(sstream, column, ',');
                }
                else if (sstream.peek() == '"')
                {
                    // https://stackoverflow.com/questions/35639083/c-csv-row-with-commas-and-strings-within-double-quotes
                    sstream >> quoted(column);
                    string discard;
                    getline(sstream, discard, ',');
                }
                else
                {
                    getline(sstream, column, ',');
                }

                if (count == 28)
                {
                    tweet = column;
                    cout << "tweet" << tweet << endl
                         << endl;
                }
                // the start of the json
                if (count >= 30)
                {
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

                        string str = tweet.substr(startOffsetNum + 1, endOffsetNum - startOffsetNum + 1);
                        cout << str << endl
                             << endl;
                        ;
                    }
                }
                count++;
            }
            cout << "column count = " << count << endl;

            // cout << row;
            filerowcount++;
            cout << "file row count = " << filerowcount << endl;

            system("pause");

            if (filerowcount == 10)
            {
                return 0;
            }
        }
    }
}