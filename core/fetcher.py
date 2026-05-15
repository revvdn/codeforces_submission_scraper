import logging
import requests

API_USER_STATUS = "https://codeforces.com/api/user.status" #base link 

API_PROBLEMSET = "https://codeforces.com/api/problemset.problems" #base link


def fetch_data(handle) :
    #step 2
    logging.info("fetch problem")
    resp = requests.get(API_PROBLEMSET) 
    resp.raise_for_status()
    data = resp.json() #convertinh
    
    #validate ap status
    if data['status'] != 'OK' :
        raise Exception("failed to fetch")
    
    #store all the problem metadata by looping all the problem
    problem_info = {}
    for detail in data['result']['problems'] :
        if 'contestId' in detail and 'index' in detail :
            pid = f"{detail['contestId']}{detail['index']}" #for the problem id
            #store problem metadata
            problem_info[pid] = {
                'name' : detail['name'],
                'rating' : detail.get('rating'), #corner case when the problem or the contest not comiing from the cf (gym type or special contest)
                'tags' : ", ".join(detail.get('tags', []))
            }
    
    logging.info(f"fetch submission for {handle} ")
    resp = requests.get(API_USER_STATUS, params={'handle': handle})
    resp.raise_for_status()
    data = resp.json()
    if data['status'] != 'OK' :
        raise Exception("failed to fetch user status")
    
    submission = data['result']
    logging.info(f"fetch {len(submission)} total from cf")

    '''
    corner case when the user have multiple OK verdict in one same problems,
    then i will keep the latest OK verdict of the problem
    for example the data is 

    4A |  100
    4A |  200
    4A |  300

    if the data goes like that , then i will stored the latest which is the biggest 
    4A | 300

    for some reason, i have think that a person who try 2 or more different code to solve.
    sorry if this tool is just taking one of your solution :)
    '''

    accepted = {}
    for sub in submission :
        if sub.get('verdict') == 'OK' and 'problem' in sub and 'contestId' in sub['problem'] and 'index' in sub['problem'] :
            pid = f"{sub['problem']['contestId']}{sub['problem']['index']}"

            if pid not in problem_info or problem_info[pid]['rating'] is None :
                continue

            if pid not in accepted or sub['creationTimeSeconds'] > accepted[pid]['creationTimeSeconds'] :
                accepted[pid] = sub

    logging.info(f"found {len(accepted)} problems")
    return accepted, problem_info
