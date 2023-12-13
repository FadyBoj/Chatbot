from main import predict_class   
from keras.models import load_model
model = load_model("chatbot_model.h5")
from flask import Flask , request , jsonify
from flask_cors import CORS
from waitress import serve
import os
app = Flask(__name__)
CORS(app)
port = int(os.environ.get("PORT", 5000))

@app.route('/send-msg/<msg>',methods=["GET"])
def main(msg):
    if not msg:
        response = jsonify({"msg":"Please provide a msg"})
        response.status_code = 400
        return response

    try:
        chatbot_response = predict_class(msg,model)
    except Exception as err:
        print(err)
        response = jsonify({"msg":"Something went wrong"})
        response.status_code = 500
        return response
    else:
        response = jsonify({"XFOOD":chatbot_response})
        response.status_code = 200
        return response
   
    
@app.route('/',methods=('GET', 'POST',))
def sec():
    return jsonify({"test":"Hi"})

if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')
