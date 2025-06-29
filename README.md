# Data Preprocessing Scripts

Here is the complete guide to the files for preprocessing

## Complete Sequence of running scripts for preprocessing (Primary)

    - 1-standardize subject name
    - 2-standardize activity names
    - 3-Delete Last Row
    - 4-Structured Data Code
    - 5-convert to atomic
    - 6-Rename and CSV {Raw Dataset is generated}
    - 7-delete unwanted files  {Final useable dataset for model AF}
    - 8-Fall Segmentation {Final Datasets Fall and ADL} 8-alt just copies the data and not delete from source location.

## Fixing Codes

    - fix upstairs can be used if the upstair and downstair events are recorded for 45 seconds
    - event fixer can be used to fix the event names like event_2_e2.csv or something like e1_e2.csv
    - sync can be used for data syncing {⚠⚠⚠ extreme loss of data}
    - rename activities can be used to rename activities if they have any issue in passing the model {this renaming does not maintain activity naming standard}

## Plot Data

    - plot comparison data can be used to plot data of multiple users with a reference of single user
    - plot multiple events can be used to plot data of users all activities for multiple events
    - plot sensor data can be used to plot single sensor
    - plot subject data can be used to plot a single subject

## Sensor Calculations

    - just a try to calculate the gravity from IMUs

## Verify Data

    - couter can be used to get total sensor rates
    - hierarchy viewer shows all the hierarchy and number of files
    - other verfication files are self explanatory

## standard activity names

### 5 seconds activities

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
