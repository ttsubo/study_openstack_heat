import json
import re
from httplib import HTTPConnection
from base64 import b64encode

url_path = "/api/queues/%2f"
auth = "guest:guest"

header = {
    "Authorization" : "Basic %s" % b64encode(auth),
    "Content-Type": "application/json",
}

session = HTTPConnection("%s:%s" % ("127.0.0.1", 15672))
session.request("GET", url_path, "", header)
response =  session.getresponse()
queues = json.load(response)
for queue in queues:
    if queue["name"] == "engine" or re.match("reply_", queue["name"]):
        print(json.dumps(queue, sort_keys=False, indent=4))
