import os
from flask import Flask, request, jsonify, json, Response
import service

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
   content = request.json
   tokens = service.tokenize(content)
   print(content)
   tmp = json.dumps(tokens,ensure_ascii = False)
   response = Response(tmp,content_type="application/json; charset=utf-8" )
   return response

if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))