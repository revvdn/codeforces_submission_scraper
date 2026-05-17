import logging
import requests
import os
import json

API_USER_STATUS = "https://codeforces.com/api/user.status"  
API_PROBLEMSET = "https://codeforces.com/api/problemset.problems" 

CACHE_DIR = "storage"
CACHE_FILE = "problem_cache.json"
FETCHED_FILE = "fetch_problem.json"

session = requests.Session()

def fetch_data(handle, base_dir) :

    cached_data = load_prob_cache(base_dir)

    if cached_data :

        logging.info(
            "use cached problem"
        )

        data = cached_data
    else :
        logging.info(
            "fetch problem from cf"
        )

        resp = session.get(API_PROBLEMSET)
        resp.raise_for_status()

        data = resp.json()

        if data["status"] != "OK" :
            raise Exception(
                "fail to fetch problem"
            )
        
        save_problem_cache(base_dir, data)

    problem_info = {}

    for detail in data["result"]["problems"] :

        if "contestId" in detail and "index" in detail :

            pid = (
                f"{detail['contestId']}{detail['index']}"
            )

            problem_info[pid] = {
                "name" : detail["name"],
                "rating" : detail.get("rating"),
                "tags" : ", ".join(
                    detail.get("tags", [])
                )                
            }
    
    logging.info(
        f"fetch submission for {handle}"
    )

    resp = session.get(
        API_USER_STATUS,
        params={"handle": handle}
    )

    resp.raise_for_status()

    data = resp.json()

    if data["status"] != "OK" :
        raise Exception(
            "fail to fetch user prob"
        )
    
    submission = data["result"]

    logging.info(
        f"fetch {len(submission)} total"
    )

    fetch_pid = load_fetch_problem(base_dir)

    accepted = {}

    for sub in submission :

        if (sub.get("verdict") == "OK" and "problem" in sub and "contestId" in sub["problem"] and "index" in sub["problem"]) :

            pid = (
                f"{sub['problem']['contestId']}{sub['problem']['index']}"
            )
            
            '''
            if pid in fetch_pid : 
                continue
            '''

            if (pid not in problem_info or problem_info[pid]["rating"] is None) :
                continue
                
            if (pid not in accepted or sub["creationTimeSeconds"] > accepted[pid]["creationTimeSeconds"]) :
                accepted[pid] = {
                    "id" : sub["id"],
                    "creationTimeSeconds" : sub["creationTimeSeconds"],
                    "contestId" : sub["problem"]["contestId"],
                    "index" : sub["problem"]["index"]
                }
    logging.info(
        f"found {len(accepted)} problems"
    )

    return (
        accepted,
        problem_info,
        fetch_pid
    )

def save_fetch_problem(base_dir, fetch_pid) :

    fetch_path = os.path.join(
        base_dir,
        CACHE_DIR,
        FETCHED_FILE
    )

    with open(fetch_path, "w", encoding="utf-8") as f :
        json.dump(list(fetch_pid), f)

def load_fetch_problem(base_dir) :
    
    fetch_path = os.path.join(
        base_dir,
        CACHE_DIR,
        FETCHED_FILE
    )

    if os.path.exists(fetch_path) :

        with open(fetch_path, "r", encoding="utf-8") as f :
            return set(json.load(f))

    return set()

def save_problem_cache(base_dir, data) :

    storage_dir = os.path.join(base_dir, CACHE_DIR)

    os.makedirs(storage_dir, exist_ok=True)

    cache_path = os.path.join(
        storage_dir,
        CACHE_FILE
    )

    with open(cache_path, "w", encoding="utf-8") as f :
        json.dump(data, f)

def load_prob_cache(base_dir) :

    cache_path = os.path.join(
        base_dir,
        CACHE_DIR,
        CACHE_FILE
    )

    if os.path.exists(cache_path) :
        
        with open(cache_path, "r", encoding="utf-8") as f :
            return json.load(f)
    
    return None

'''
def fetch_data(handle) :

    logging.info("fetch problem")
    #resp = requests.get(API_PROBLEMSET) 
    #resp.raise_for_status()
    #data = resp.json()

    cached_data = load_prob_cache(base_dir)

    if cached_data :
        
        logging.info("use cached prob")
        data = cached_data
    else :

        logging.info("fetch prob from cf")
        resp = session.get(API_PROBLEMSET)
        resp.raise_for_status()
        data = resp.json()

        save_problem_cache(base_dir, data)

    
    #validate status
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
    
    logging.info(
        f"fetch submission for {handle} "
    )

    resp = requests.get(
        API_USER_STATUS, 
        params={'handle': handle}
    )

    resp.raise_for_status()
    data = resp.json()
    if data['status'] != 'OK' :
        raise Exception("failed to fetch user status")
    
    submission = data['result']
    logging.info(f"fetch {len(submission)} total from cf")


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

    accepted = {}
    for sub in submission :
        if sub.get('verdict') == 'OK' and 'problem' in sub and 'contestId' in sub['problem'] and 'index' in sub['problem'] :
    
            pid = f"{sub['problem']['contestId']}{sub['problem']['index']}"

            if pid not in problem_info or problem_info[pid]['rating'] is None :
                continue

            if pid not in accepted or sub['creationTimeSeconds'] > accepted[pid]['creationTimeSeconds'] :
                accepted[pid] = sub

    logging.info(
        f"found {len(accepted)} problems"
    )
    return accepted, problem_info
'''