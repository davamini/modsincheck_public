# ModsInCheck
## Monitor Moderator Activity
![Homepage](/images/homepage.PNG)
### Uses Python Reddit API Wrapper, PRAW, to retrieve moderator data and Google Visualization API to visualize it.
![ModExample](/images/mod_example.PNG)
## To get started:
#### Clone the repository
```bash
git clone https://github.com/davamini/modsincheck_public
```
Create a Reddit account to access Reddit's API    
Make an application at https://www.reddit.com/prefs/apps  
Fill in config_example.json with your client_id, client_secret, user_agent, and username  
Change the name of config_example.json to config.json  
####    Add subreddits to subreddits.json
####    Then run the following:
```bash
pip install -r requirements.txt
```
```bash
python manage.py migrate
```
```bash
python update_database.py
```
```python
python manage.py runserver
```