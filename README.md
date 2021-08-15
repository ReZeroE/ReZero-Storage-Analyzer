# ReZero-Storage-Analyzer
Light-weight program that tracks and identifies the storage size change of a target directory overtime.

## Initialization 
To initialize the data required for comparison, first run the program without providing any arguments.
The program will automatically analyze the given directory and records the data in a log file based on the date and time of the run.

Example record filename: `2020-05-14_log.tsv`

## Disk Space Change Analysis
To obtain the storage size change of a target directory, run the program with argument one as the log file's name to compare to.

For example, if I would like to compare the current directory size with a record from April 4th, 2021, the following command would be executed:

```cmd
py -3.x main.py 2021-04-04_log.tsv
python3 main.py 2021-04-04_log.tsv
```

## Output
The output result will be stored in a file named `result.tsv`. This file contains the storage size change of the target directory provided from the previous step.

An example output:
```
=======================\ FILES THAT INCREASED IN SIZE /=======================
+ Folder [1] D:\Program Files\ModifiableWindowsApps has a size change of 31.24 MB. (31244288 bytes)
+ Folder [1] D:\Steam\bin has a size change of 0.0 MB. (154 bytes)
+ Folder [1] D:\Steam\dumps has a size change of 0.0 MB. (16 bytes)
+ Folder [1] D:\Steam\logs has a size change of 0.0 MB. (979 bytes)
+ Folder [1] D:\Steam\steamapps has a size change of 16322.02 MB. (16322019840 bytes)
+ Folder [1] D:\VPN\fa has a size change of 0.08 MB. (78823 bytes)
+ Folder [1] D:\VPN\it has a size change of 0.07 MB. (68033 bytes)

=======================\ FILES THAT DECREASED IN SIZE /=======================
- Folder [1] D:\LDPlayer\LDPlayerXuanZhi has a size change of -437184.32 MB. (-437184322634 bytes)
- Folder [1] D:\TIM\I18N has a size change of -53270.92 MB. (-53270921482 bytes)

=====================\ FILES THAT DID NOT CHANGE IN SIZE /=====================
= Folder [1] D:\Call of Duty\Battle.net has a size change of 0.0 MB. (0 bytes)
= Folder [1] D:\Corsair\CORSAIR iCUE Software has a size change of 0.0 MB. (0 bytes)
= Folder [1] D:\CrystalDiskInfo\CdiResource has a size change of 0.0 MB. (0 bytes)
= Folder [1] D:\Discord AI Bot WEP\.idea has a size change of 0.0 MB. (0 bytes)
= Folder [1] D:\Discord AI Bot WEP\__pycache__ has a size change of 0.0 MB. (0 bytes)
...
```
Note that the directory layer of analysis is set to 1 by default. The `x` value in the prefix for each line `Folder [x]` represents the layer of analysis.


