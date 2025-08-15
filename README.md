# WiE-Helper-Bot

Bot to help make internal processes easier within the Women in Engineering community!

## 3 features
1. /assign_role - add member to a subteam role
2. /unassign_role - remove member from a subteam role 
3. /subteam_info - view all members + their subteam role
4. /assign_past_directors - Gives everyone with the Director role the Past Director role
5. /year_to_alumni - Give everyone in a specified year role the Alumni role
6. /remove_all_directors - Remove Director role & subroles from everyone with Director role (except execs, faculty & wie reps)

## How To Clone
1. ```git clone``` the repository to your local machine
2. make sure you have python installed
3. Replace the secret key token with the actual token found on Notion (we should really migrate this to use .env, someone do that please)

## How To Run
1. ```python3 -m venv venv```
2. ```source venv/bin/activate```
3. ```pip install -r requirements.txt```
Run either:
```python main.py --token "MY_PROD_TOKEN"``` or
```python main.py``` and place the DISCORD_TOKEN in a .env file
5. when you see ```slash commands are now synced``` in the terminal, it means you can go to the WiE discord and start using the bot

## Hosting
um.. its not

## Example Output
<img width="600" alt="image" src="https://github.com/user-attachments/assets/fff6019f-7a06-4e3f-b8e7-e62796b7e7c6">
