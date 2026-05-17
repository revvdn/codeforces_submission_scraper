# competitive programming submission fetcher

fetch all your submission from competitive programming platform and commit it on github

## highlights

* automated fetch all your submission with minimal setup
* simple and easy to setup and use
* detailed data (e.g ratings, tags, timestamp)
* commit for each submission with the original submit date to make your contribution graph looks magnificien
* automated git push to remote repository **- ongoing feature**

## platforms

This tool currently support only [codeforces](https://codeforces.com/)

**soon :**
* [AtCoder](https://atcoder.jp/home)

integration with other platform are still in consideration. Contribution always welcomed

## instalation

before running the tools, make sure you have installed
- Python 3.10 or newer
- Git installed and avaible in PATH

if you want to make sure, follow the current command to verify :

```bash
python --version
git --version
```

**start the installation**
clone the repository :
```bash
git clone https://github.com/revvdn/codeforces_submission_scraper.git
```

move into the tools directory :
```bash
cd cf_scraper
```

install the required dependencies :
```bash
pip install -r requirements.txt
```

## getting started

after installing, run the following command to start :
```bash
python main.py <your_handle>
```

example :
```bash
python main.py tourist
```

## future work
1. **code complexity** - current code are having worst time complexity, but it can be improved later
2. **more platform support** - this quite complex because each platform has different method and need long time to breakdown
3. **submission analisys** - big feature under progress
4. **adding UI** - im curently work on Terminal UI (TUI)