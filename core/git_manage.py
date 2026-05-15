import os
import logging
import subprocess
from datetime import datetime

def ensure_git_repo(base_dir) :

    git_dir = os.path.join(
        base_dir, ".git"
    )

    if not os.path.exists(git_dir) :

        logging.info(
            "git repo not found. initialize git repo ..."
        )

        subprocess.run(
            ["git", "init"], 
            cwd=base_dir, check=True
        )

        logging.info(
            "git repo was initialized"
        )


def commit_problem(pid, pinfo, sub, base_dir, rating) :
    '''
    i have been thinking that it's possible for someone who want to push the problem into github, but
    all of the submission have their own date right, to overcome this i would set the git timestamp based on the real submission time in codeforces
    '''
    submission_date = datetime.fromtimestamp(sub['creationTimeSeconds']).isoformat()

    env = os.environ.copy()
    
    env["GIT_AUTHOR_DATE"] = submission_date
    env["GIT_COMMITTER_DATE"] = submission_date

    by_rating = f"problems/codeforces/by_rating/{rating}/README.md"
    subprocess.run(
        ["git", "add", "README.md", by_rating], cwd = base_dir, check=True
    )

    msg = f"add codeforces {pid} - {pinfo['name']}"
    subprocess.run(
        ["git", "commit", "-m", msg], cwd=base_dir, env=env, check=True
    )
    logging.info(
        f"committed {pid} with timestamp {submission_date}"
    )
