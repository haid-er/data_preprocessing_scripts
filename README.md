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

    - standardize subject name
    - standardize activity names
    - Delete Last Row
    - Structured Data Code
    - sync
    - upstair downstair issue resolution
    - convert to atomic
    - rename files
    - final fixed 4 second atomic activity

Note: Other files are just used for verification of data. Each file accept the path till base folder which have three devices folders.

## standard activity names

    - bending
    - walking
    - standing_up_from_sitting
    - sitting_down_from_standing
    - slow_walk
    - squatting
    - open_door
    - close_door
    - quick_walk
    - sitting
    - put_on_floor
    - pick_from_floor
    - laying_down_from_sitting
    - standing_up_from_laying
    - typing
    - jogging
    - clean_the_table
    - open_bag
    - open_big_box
    - reading
    - close_lid_by_rotation
    - plugin
    - throw_out
    - laying
    - eat_small_things
    - talk_using_phone
    - standing
    - upstairs
    - downstairs
    - drink_water
    - fall_forward
    - fall_right
    - fall_backward
    - fall_left
    - fall_forward_when_trying_to_sit_down
    - fall_backward_while_trying_to_sit_down
    - fall_forward_while_trying_to_stand_up
    - fall_backward_while_trying_to_stand_up

### Three Minute activities

    - quick_walk
    - jogging
    - laying
    - reading
    - sitting
    - slow_walk
    - standing
    - talk_using_phone
    - typing
    - walking
    - clean_the_table
