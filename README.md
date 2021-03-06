# statistical_simulation

investigating various data sources and advanced statistical methods

## InvestigateCheXpert

**Let's look at radiology imaging data**

### data/chexpert

* ***valid.csv*** - This data file comes from the [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/) competition. It serves as metadata for a validation set of chest radiographs
* ***train.csv*** -  This data file comes from the [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/) competition. It serves as metadata for a training set of chest radiographs

These files were processed through `extractingPatientId.py` to create a column for the patient identifier (PID) and study identifier (StudyID). That made it easier to create descriptive statistics of the information.

## NbaComparisonsFy20

**Let's compare the top teams in the league**

### data/basketball
* ***BucksRosterFY20.csv*** - data from [BasketballReference](https://www.basketball-reference.com/) on the Milwaukee Bucks 2019-2020 roster. Downloaded 3 March 2020.
* ***LakersRosterFY20.csv*** - data from [BasketballReference](https://www.basketball-reference.com/) on the Los Angeles Lakers 2019-2020 roster. Downloaded 3 March 2020.

## USAU_HistData

**Let's work on acquiring Ultimate Frisbee game data**

### data/ultimate
The data files in this directory were manually collected on 8 April 2020
* ***_tournaments.xlsx*** - combined manually collected data on a collection of ultimate frisbee tournaments 
* ***tournament_results.csv*** - game results for a collection of ultimate frisbee tournaments
* ***tournament_teams.csv*** - teams and seedings for a collection of ultimate frisbee tournaments

#### event subdirectories
These are the output locations for data scraped from the USAU tournament websites with `USAU_HistData.ipynb`. For example, the Florida Warmup tournament play is stored in the following structure:

##### Florida-Warm-Up-2019/schedule/Men/CollegeMen/
* ***bracketplay.csv*** - data scraped from brackets on USAU score reporter
* ***poolplay.csv*** - data scraped from HTML data tables on USAU score reporter
