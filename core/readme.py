import os
import re
from datetime import datetime
from templates.templates import (
    README_TEMPLATE,
    TABLE_TEMPLATE,
    INITIAL_TABLE_TEMPLATE
)

def update_readme(rating, pid, api_accepted, problems_info, base_dir) :
    '''
    final readme construct, building and insert the fetched data into the table
    based on the data that have been sorted in readme_construct module
    This module would make the folder based on the rating e.g 800, 900, 1000
    and the structure would be

    problems/
    └── codeforces/
        └── by_rating/
            ├── 800/
            │   └── README.md
            ├── 900/
            │   └── README.md
            ├── 1200/
            │   └── README.md

    '''

    #build the directory path
    dir_path = os.path.join(
        base_dir, 
        "problems", 
        "codeforces", 
        "by_rating", 
        str(rating)
    )
    
    os.makedirs(dir_path, exist_ok=True)
    readme_path = os.path.join(dir_path, "README.md")

    #sort problem id or pid
    sorted_pid = sorted(
        pid, 
        key=lambda p: -api_accepted[p]['creationTimeSeconds']
    )

    #generating rows table
    lines = [f"# Codeforces Rating {rating}\n", "| # | Title | Solution | Tags | Submitted |", "| - | ----- | -------- | ---- | --------- |"]
    for p in sorted_pid :
    
        sub = api_accepted[p]
        info = problems_info[p]
    
        date_str = datetime.fromtimestamp(
            sub['creationTimeSeconds']
        ).strftime('%b/%d/%Y %I:%M %p')
        
        prob_url = f"https://codeforces.com/problemset/problem/{sub['problem']['contestId']}/{sub['problem']['index']}"
        
        sub_url = f"https://codeforces.com/contest/{sub['problem']['contestId']}/submission/{sub['id']}"
    
        lines.append(f"| {p} | [{info['name']}]({prob_url}) | [Submission]({sub_url}) | {info['tags']} | {date_str} |")

    #write the result
    with open(readme_path, 'w', encoding='utf-8') as f :
        f.write('\n'.join(lines) + '\n')


def construct_readme(readme_path, all_pid, api_accepted, problems_info) :
    #step 3
    '''
    based on my case, i already have readme.md file before, so this code will reconstruct the previous readme
    but in some case the user doesn't have the readme before, then make the new readme file 
    '''
    if not os.path.exists(readme_path) :
        
        with open(readme_path, 'w', encoding='utf-8') as f :
            f.write(README_TEMPLATE)

    with open(readme_path, 'r', encoding='utf-8') as f :
        lines = f.read().split('\n')
    
    '''
    this section will count number of problem and sort based on the rating (ascending order) and
    submission time (descending)

    why ? just to make the table looks organized and easy to read, if the user want to see the specific rating thay can easliy find them 
    rather than not sorted
    '''
    cf_count = len(all_pid)
    sorted_pid = sorted(
        all_pid, 
        key=lambda p: (problems_info[p]['rating'], 
                       -api_accepted[p]['creationTimeSeconds']
                    )
    )

    out_line = []
    skip_table = False
    detail_found = False
    
    #table construct by parse the old readme (if exist) or the new and some generating logic to make sure the table look magnificient XD
    for line in lines :
        
        if skip_table :
            
            if line.strip() == '' or line.strip().startswith('|') :
                continue
            skip_table = False
        
        if "## Submission Table" in line :
            
            out_line.append(line)
            out_line.append("")
            out_line.append(TABLE_TEMPLATE)
            
            for p in sorted_pid :
                sub = api_accepted[p]
                info = problems_info[p]
            
                date_str = datetime.fromtimestamp(
                    sub['creationTimeSeconds']
                ).strftime('%b/%d/%Y %I:%M %p')
                
                prob_url = f"https://codeforces.com/problemset/problem/{sub['problem']['contestId']}/{sub['problem']['index']}"
                
                sub_url = f"https://codeforces.com/contest/{sub['problem']['contestId']}/submission/{sub['id']}"
                
                out_line.append(f"| {p} | [{info['name']}]({prob_url}) | {info['rating']} | {info['tags']} | [{date_str}]({sub_url}) |")
            
            out_line.append("")
            skip_table = True
            detail_found = True
            
            continue

        if re.match(r'^\|\s*Codeforces\s*\|', line.strip()) :
            
            out_line.append(f"| Codeforces | {cf_count} |")
            continue

        if re.match(r'^\|\s*\*\*Total\*\*\s*\|', line.strip()) :
            
            m = re.search(r'\|\s*\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|', line)
            
            if m :
                out_line.append(f"| **Total** | **{cf_count}** |")
            else :
                out_line.append(line)
            
            continue
        out_line.append(line)

    if not detail_found :
        
        if out_line and out_line[-1].strip() != '' :
        
            out_line.append('')
            out_line.append(INITIAL_TABLE_TEMPLATE)
        
            for p in sorted_pid :
                
                sub = api_accepted[p]
                info = problems_info[p]
        
                date_str = datetime.fromtimestamp(
                    sub['creationTimeSeconds']
                ).strftime('%b/%d/%Y %I:%M %p')
                
                prob_url = f"https://codeforces.com/problemset/problem/{sub['problem']['contestId']}/{sub['problem']['index']}"
                
                sub_url = f"https://codeforces.com/contest/{sub['problem']['contestId']}/submission/{sub['id']}"
        
                out_line.append(f"| {p} | [{info['name']}]({prob_url}) | {info['rating']} | {info['tags']} | [{date_str}]({sub_url}) |")

    #apply and write into the readme
    with open(readme_path, 'w', encoding='utf-8') as f :
        f.write('\n'.join(out_line).rstrip() + '\n')  
