# Data Preprocessing Scripts

Here is the complete guide to the files for preprocessing

### Count

    This script can be used to count the total number of rows in the files in dataset.

### Hierarchy Viewer

    This script can be used to view hierarchy or struture of the folders.

### Plot Sensor Data

    This script can be used to plot a single file's data.

### Plot Graphs with Dimension

    Notebook to plot sensory data collectively.

### Convert to Atomic

    This file can be used to convert 3 minutes activities to 5 seconds events.

### Delete Last Row

    Script will delete last row from each file to eliminate last incomplete row.

### Final Fixed 4 second

    Notebook can be used to convert events files to json file which can be parsed to ML model for training and testing.

### Structured Data Code

    Can be used to change the hierarchy of the folders from collection structure to required structure or hierarchy for conversion to json.

### Sync

    Sync script can be used to synchronized data of the files according to late start early finish.

### Verify Data Timestamps

    Can be used to verify data timestamps to match events time before syncing and changing hierarchy.

### Verify

    Can be used to verify duration and total values of collected data before syncing and changing hierarchy.

### Verify Timestamps Sync Data

    Can be used to verify data timestamps to match events time after syncing and changing hierarchy.

### Verify Sync Data

    Can be used to verify duration and total values of collected data after syncing and changing hierarchy.

## Complete Sequence of running scripts for preprocessing

    - Delete Last Row
    - Structured Data Code
    - sync
    - convert to atomic
    - final fixed 4 second atomic activity

Other files are just used for verification of data.
