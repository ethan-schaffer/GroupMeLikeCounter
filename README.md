# GroupMeLikeCounter

Overview
---

This Program Counts the number of likes each person in a groupme chat has recieved. 

It does this using the [Groupy API Wrapper](https://pypi.org/project/GroupyAPI/), which wraps GroupMe's official API. 

Once completed, the data is stored in a Google Doc. This is done to make it accessible (but view only) to any member of the chat. 

Problems
---

While at some point every message will need to be processed, an obvious implementation would need to look through every message each time one is sent in order to update things. 

One issue with this is that in some cases, groupme chats can have tens or even hundreds of thousands of messages. 

Going over the same messages over and over is a waste of time, so instead we can store a current count for each user, along with what the id of the most recent message read.

Google Sheets
---

The output of this program can be found at a Google Sheet. This is accomplished using the [Google Sheets API](https://developers.google.com/sheets/api).

Pipeline
---

The overall pipeline of tasks is that the data must be loaded. Then, an update option exists, before the data is sent to the google sheet.

The first function that is run is [data_load](https://github.com/ethan-schaffer/GroupMeLikeCounter/blob/main/data_load.py).  `data_load` reads through the whole chatlog, in order to get a preliminary count. 

The second function is [data_update](https://github.com/ethan-schaffer/GroupMeLikeCounter/blob/main/data_update.py), which updates the running totals of likes and counts for each user. 

The final function is [data_to_google_sheet](https://github.com/ethan-schaffer/GroupMeLikeCounter/blob/main/data_to_google_sheet.py), which does what would be expected. 

To do this, I used the Google Sheets API, along with sort functions and a map operation to best prepare the data.

Future Improvements
---

Currently, a "like" a user awards their own message will be counted. 

However, this might not be how some people want to be counted, and a potential improvement would be to ignore self-likes. 
