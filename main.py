import os 
import sys 
import argparse 
import logging
import subprocess  
from core.fetcher import (
    fetch_data,
    save_fetch_problem
)

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
        "handle", 
        help="your codeforces handle :"
    )

    parser.add_argument(
        "--fast",
        action="store_true"
    )

    args = parser.parse_args()

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )
    
    ensure_git_repo(base_dir)

    readme_path = os.path.join(base_dir, "CF_STATS.md")

    try :
        api_accepted, problems_info, fetch_pid = fetch_data(args.handle, base_dir)
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
        
        #sub = api_accepted[pid]
        pinfo = problems_info[pid]
        rating = pinfo['rating']

        '''
        logging.info(
            f"process {pid} rating : {rating}"
        )
        '''

        pid_by_rating.setdefault(
            rating, 
            []
        ).append(pid)

    for rating in pid_by_rating :
        
        pid_by_rating[rating].sort(
            key=lambda p:
            -api_accepted[p]['creationTimeSeconds']
        )

        #bakal ngungsi


    for rating, pids in pid_by_rating.items() :
      update_readme(
          rating, 
          pid_by_rating[rating], 
          api_accepted, 
          problems_info, 
          base_dir
      )

    construct_readme(
        readme_path, 
        new_pid, 
        api_accepted, 
        problems_info
    )

    if args.fast : 
        '''        
        subprocess.run(
            ["git", "add", "."],
            cwd = base_dir,
            check=True
        )
        
        subprocess.run(
            ["git", "commit", "-m", f"add {len(new_pid)} problem"],
            cwd=base_dir,
            check=True
        )
        '''

    else :
        
      for pid in time_new_pid:
          
          sub = api_accepted[pid]
          pinfo = problems_info[pid]
          rating = pinfo["rating"]

          commit_problem(
              pid, 
              pinfo, 
              sub, 
              base_dir, 
              rating
          )

    fetch_pid.update(new_pid)

    save_fetch_problem(
        base_dir, fetch_pid
    )  
          
    logging.info(
        f"success to fetch {len(time_new_pid)} problems"
    )

if __name__ == "__main__" :
    main()
