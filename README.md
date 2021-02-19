# Portfolio Risk Management

Please edit ticker, weight/share, and initial investment in ini.json file to generate portfolio. (And use setting.json to control data collection/usage and file/portfolio selection.)

Run service to generate portfolio info and VAR/CVAR data. 

1 day to 2 week VAR/CVAR at 95, 99, 99.1 confidence level will be printed out as a table. Output will be saved in "output" folder.

Folder "normality check charts" will have charts for individual stocks in the portfolio to check whether they were normally distributed.

Folder "cache" will have the WIP csv files.

TO DO:

1. Use json file as input (Completed)

2. Implement other VAR methods

3. Work on CVAR, ES, etc. (Need to double check)

4. Add portfolio optimization

5. Switch to APIs that don't require a token (Completed; switched to yFinance)

6. Integrate with my other project, portfolio_tracking

**yFinance can be unreliable at times. Force restart might be required in certain situations. Random waits (5-10s) are added inbetween data collections to mitigate this issue, which leads to extra waiting time.

Example Output: 
![Alt text](sample_output.txt?raw=True)
