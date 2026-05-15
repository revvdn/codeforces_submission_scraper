'''
firts thing first, i want to decompose the all of the things needed for this 
To receive all the submission i need to get the json file from the codeforces
that's could be done by using codeforces api to fetch the data 

After searching in google and read from the official (https://codeforces.com/apiHelp/methods) &
(https://codeforces.com/apiHelp/methods), 

i get that to fetch the data is basically just run the https://codeforces.com/api/{methodName}
So what's the methodName??

based on this https://codeforces.com/apiHelp/methods
There's a lot of method that listed, those are :

1. blogEntry.comments 
2. blogEntry.view 
3. contest.hacks 
4. contest.list
5. contest.ratingChanges
6. contets.standings
7. contest.status
8. group.isManager
9. problemset.problems -> i think thsi one have a role in this tool
10. problemset.recentStatus
11. recentActions
12. system.status
13. user.blogEntries
14. user.friends
15. user.info
16. user.ratedList 
17. user.rating
18. user.status -> the last and the main char in this tool XD

after getting the suitable methodname (user.status) and the problemset.problems
How can i get or fetch the data?
luckily, the website come with the way to get the data 

for problemset.problems
will return all the problems from the problemset, that further also can filtered by the tags 
The parameter :
1. tags -> semicolon-separated list of tags
2. problemsetName -> custom problemset's short name
Return value : return two list. List of problem object and list of proble statistic objects
example : https://codeforces.com/api/problemset.problems?tags=implementation

from those link , i can get this data :
{
  "status": "OK",
  "result": {
    "problems": [
      {
        "contestId": 2227,
        "index": "D",
        "name": "Palindromex",
        "type": "PROGRAMMING",
        "tags": [
          "binary search",
          "brute force",
          "constructive algorithms",
          "data structures",
          "greedy",
          "implementation",
          "two pointers"
        ]
      },
      {
        "contestId": 2227,
        "index": "A",
        "name": "Koshary",
        "type": "PROGRAMMING",
        "tags": [
          "implementation",
          "math"
        ]
      },
      .....

those are the example for two problems data that can i get fromm tags : implementation
actually in codeforces there would be more than 20 :( if i wasn't mistaken
and for each tags has more than 1000+ problems X(, i know it sound hyprbolic but trust me it's reasonable
from the biggest CP platform in the world :)

now, move into 

user.status 
it will return the submission of specified user, this is what i have been search, and why this will be the main char in this tool
The parameter's are :
1. handle -> in codeforces user id are defined by handle
2. from -> index of the first submission to return 
3. count -> number of returned submissions
4. includeSources -> specifies wheter source codes should be included in the output
Return value : list of submission objects, sorted in decreasing order of submission id (means that it already sorted form the firts submission
into the last submission of the user)
example : https://codeforces.com/api/user.status?handle={user_handle}&from=1&count=10

From the example, the link is refer to 10 first submission of the user (handle), since this
tool is to fetch all the submission, so i will ignore the from & count & includeSources parameter

so i will use the link : https://codeforces.com/api/user.status?handle={handle}
i try with my own handle : rep_ (please visit haha, but im still an newbie -_)
this the example of the output after send that link 

{
  "status": "OK",
  "result": [
    {
      "id": 373964265,
      "contestId": 276,
      "creationTimeSeconds": 1778291287,
      "relativeTimeSeconds": 2147483647,
      "problem": {
        "contestId": 276,
        "index": "C",
        "name": "Little Girl and Maximum Sum",
        "type": "PROGRAMMING",
        "points": 1500,
        "rating": 1500,
        "tags": [
          "data structures",
          "greedy",
          "implementation",
          "sortings"
        ]
      },
      "author": {
        "contestId": 276,
        "participantId": 201970041,
        "members": [
          {
            "handle": "rep_"
          }
        ],
        "participantType": "PRACTICE",
        "ghost": false,
        "startTimeSeconds": 1361719800
      },
      "programmingLanguage": "C++23 (GCC 14-64, msys2)",
      "verdict": "WRONG_ANSWER", 
      "testset": "TESTS",
      "passedTestCount": 0,
      "timeConsumedMillis": 15,
      "memoryConsumedBytes": 0
    },
    ....

so i will get the problems info's and also the verdict, the language used 
the verdict would be 
"OK" for correct
"WRONG_ANSWER" for not passed all the test cases
"COMPLIATION_ERROR" for the erorr in the code 
"RUNTIME ERORR" usually this caused by the complexity issues in the code (the code runtime passed the given time limit)
"TIME_LIMIT_EXEEDED" the code passed the given time limit 

about the languages, actually codeforces support almost all the languages, you can read from this https://codeforces.com/blog/entry/70771

After searching and defining how i can get the data
next is to defining how i can process the data

based on the data i will get 
1. the problem name 
2. problems tag
3. the verdict 
4. the submission details (date, etc.)

based on the data i will arange that into a table 
the table would look like this 

    #   |     Title      | Rating |      Tags     |  Submission  |
---------------------------------------------------------------
  1995A |    Diagonals   |   800  |  greedy, ...  | Apr/.../2026 |

  
and i will also count the total problems that have been solved (means has the "OK" verdict)

to achieve this i will break into some modules, those are :
1. to prepare the needed before fetching the data (main)
2. to fetching data (fetch_data)
3. to make the base of the readme and table (construct_readme) 
4. update the readme based on the fetched data (update_readme)
5. add the submission time into the readme (commit_problem)

after things get done
TIME TO CODE YEAH :)
'''

import os 
import sys 
import argparse 
import logging  
from core.fetcher import fetch_data
from core.readme import (
    construct_readme,
    update_readme
)
from core.git_manage import (
    ensure_git_repo,
    commit_problem
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def main() :
    '''
    This module will get the user handle by asking them, then try to fetch and get the submission data 
    from the codeforces based on what i have been explain above
    im only build to fetch the "OK" or AC if in the codeforces, because in most of the case 
    the total submission is enourmously high because not every single porblem got AC in the first try,
    and Who's gonna display the non AC submission right :)
    '''
    parser = argparse.ArgumentParser(
        description="codeforces submission scraper"
    )

    parser.add_argument(
        "handle", help="yout codeforces handle :"
    )

    args = parser.parse_args()

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )
    
    ensure_git_repo(base_dir)

    readme_path = os.path.join(base_dir, "README.md")

    try :
        api_accepted, problems_info = fetch_data(args.handle)
    except Exception as e :
        logging.error(f"Error fetching data : {e}")
        sys.exit(1)

    new_pid = set(api_accepted.keys())

    '''
    if not new_pid :
        logging.info("no new problems to fetch")
        sys.exit(0)
    '''#just in case if user had the solution before

    time_new_pid = sorted(
        list(new_pid), 
        key=lambda p: api_accepted[p]['creationTimeSeconds']
    )

    pid_by_rating = {}

    for pid in time_new_pid :
        
        sub = api_accepted[pid]
        pinfo = problems_info[pid]
        rating = pinfo['rating']

        logging.info(
            f"process {pid} rating : {rating}"
        )

        #current_known_pid.add(pid)
        pid_by_rating.setdefault(
            rating, 
            set()
        ).add(pid)

        update_readme(
            rating, 
            pid_by_rating[rating], 
            api_accepted, 
            problems_info, 
            base_dir
        )

        commit_problem(
            pid, 
            pinfo, 
            sub, 
            base_dir, 
            rating
        )

    logging.info(
        f"success to fetch {len(time_new_pid)} problems"
    )

    construct_readme(
        readme_path, 
        new_pid, 
        api_accepted, 
        problems_info
    )


if __name__ == "__main__" :
    main()