Setup Instructions :
STEP 1 : Clone the repository: git clone https://github.com/your-repo.git

STEP 2 : Create a .env file manually : 
Add the following configuration variables to your .env file:
SECRET_KEY=supersecretkey
MONGO_URI=mongodb+srv://your_username:your_password@cluster0.mongodb.net/flask_db?retryWrites=true&w=majority&appName=Cluster0
AUTH_TOKEN=<your_auth_token_here>  
SESSION_TOKEN=<your_session_token_here>   

STEP 3 : Install dependencies: pip install -r requirements.txt
STEP 4 : Run the application: python server.py
