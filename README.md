# statistical_simulation

investigating various data sources and advanced statistical methods

## NbaComparisonsFy20

**Let's compare the top teams in the league**

### data/basketball
* ***BucksRosterFY20.csv*** - data from [BasketballReference](https://www.basketball-reference.com/) on the Milwaukee Bucks 2019-2020 roster. Downloaded 3 March 2020.
* ***LakersRosterFY20.csv*** - data from [BasketballReference](https://www.basketball-reference.com/) on the Los Angeles Lakers 2019-2020 roster. Downloaded 3 March 2020.

## InvestigateCheXpert

**Let's look at radiology imaging data**

### data

* ***valid.csv*** - This data file comes from the [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/) competition. It serves as metadata for a validation set of chest radiographs
* ***train.csv*** -  This data file comes from the [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/) competition. It serves as metadata for a training set of chest radiographs

These files were processed through `extractingPatientId.py` to create a column for the patient identifier (PID) and study identifier (StudyID). That made it easier to create descriptive statistics of the information.