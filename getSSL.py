import pexpect
import time
from pymongo import MongoClient


uri = "mongodb+srv://Max:AA951753@bat.zcefrvy.mongodb.net/bat?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['cname_ssl']

collection = db['SSLJobs']

# Start the subprocess
child = pexpect.spawn('sudo certbot certonly --email a0958057936@gmail.com -d test.hqsmaxtest.online --agree-tos --manual --staging --config-dir /Users/manias/Desktop/work_space/cname_ssl')

# Wait for password prompt and send password
index = child.expect(['Password:'])
if index == 0:
    child.sendline('951753')
    time.sleep(5)  # Wait for 5 seconds

    child.expect('Press Enter to Continue')
    print(child.before.decode('utf-8'))
    challengeData = child.before.decode('utf-8')
    collection.insert_one({'domain': 'test.hqsmaxtest.online', 'challengeData': challengeData})
    # with open('challenge_info.txt', 'w') as file:
    #     # Write the challenge data and URL to the file
    #     file.write('Challenge data: ' + child.before.decode('utf-8') + '\n')

    index = child.expect(['Press Enter to Continue'])
    if index == 0:
        child.sendline('\n')

