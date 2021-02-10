# portfolio_risk_management

Please edit ticker, weight, and initial investment in US_EQUITY_INI_PORTFOLIO.py file to generate portfolio. (Alternative: edit US_EQUITY_input.csv manually.)

Run service to generate VAR data (VCA and HSA are available at the moment).

1 day to 2 week VAR at 95, 99, 99.1 confidence level will be saved as charts (e.g. VAR(XXX).jpg).

Folder "normality check charts" will have charts for individual stocks in the portfolio to check whether they were normally distributed. 

TO DO:

1. Use json file as input

2. Implement other VAR methods (complete monte carlo and variants of HS)

3. Work on CVAR, ES, etc.

4. Add portfolio optimization

5. Switch to APIs that don't require a token

6. Integrate with my other project, portfolio_tracking

*requires a token from Tradier Developer (Sandbox): https://developer.tradier.com/user/sign_up . Save as tradier_token.txt
