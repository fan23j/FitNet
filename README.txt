Steps to run:

1. Open your chrome browser and check the major verion of the browser.(Help --> About Google Chrome)
Eg: If the version is 90.X.XXXX.XXX the major version is 90

2. Go to https://chromedriver.chromium.org/downloads and download the chrome browser driver according to the major version.

3. Extract and place the driver inside a folder.

4. Open the .py script and change the parameters DRIVER_PATH, no_of_images, search_terms, save_folder, sleep_between_interactions accordingly. (from line 116 to 130)

5. Install selenium in the python environment using pip or any other method. 

6. Run the script.

7. Results will be saved inside save_folder/search_item for each search_item in search_items list.

8. To check the operation, 1st do a test run with no_of_images variable set to a low number and search_terms list variable set to a few terms.

*****************************************************************************************************************************************
Note: A browser window will automatically open and keep on doing the searches as mentioned in the script. Minimize it if it is disturbing.
*****************************************************************************************************************************************
