# flask project

# tastytable 
is based off flasrk (flask.palletsprojects.com)

# changes
- moved imports, as a result we need to import some things earlier in __init__.py
(redirect, url_for) - change from using blueprints
- start command is python -m flask --app tastytable --run debug (virtual env "flaskenv" was made with 3.7 -- possibly this is an issue)
- schema references recipes instead of posts
- user table schema references salts in addition to username, password hash