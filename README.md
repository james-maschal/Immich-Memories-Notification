# Immich-Memories-Notification
This is a Python script that will check Immich's Memories API to see if there are any memories due to show today. Sends a notification if there is, reminding you to look at them.

## Notes:
- I am not a development expert, use at your own risk!
- I developed this for at home use, which is why it uses HTTP instead of HTTPS. If you want to use HTTPS you will have to make changes to the script to support it.
- This was developed for self-hosted notification services like Gotify and ntfy. You will likely have to change the notification function to properly support your notification service of choice.
- Developed with python version 3.12.3 if that means anything to you smart people.
- If there are improvements that could be made, please do feel free to add or comment :)


## How to use this script:
1. I had to create a python venv to avoid issues with my server installing python-dotenv and requests, I would suggest you do the same unless you have a better method (I'm not the python police!)
2. Add the files in this repo to your folder of choice.
3. Edit the .env file, replacing it with your own relevant info.
4. Run the script daily using your task scheduler of choice (such as cron). Make sure to run it with the python in your venv!
5. Enjoy!
