# statistical_simulation
investigating methods to simulate data

## data

* ***valid.csv*** - This data file comes from the [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/) competition. It serves as metadata for a validation set of chest radiographs
* ***train.csv*** -  This data file comes from the [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/) competition. It serves as metadata for a training set of chest radiographs

These files were processed through `extractingPatientId.py` to create a column for the patient identifier (PID). That made it easier to create descriptive statistics of the information.