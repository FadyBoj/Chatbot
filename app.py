from main import predict_class   
from keras.models import load_model
model = load_model("chatbot_model.h5")
from flask import Flask , request , jsonify
from waitress import serve
app = Flask(__name__)

@app.route('/send-msg/<msg>',methods=["GET"])
def main(msg):
    if not msg:
        response = jsonify({"msg":"Please provide a msg"})
        response.status_code = 400
        return response

    try:
        chatbot_response = predict_class(msg,model)
    except:
        response = jsonify({"msg":"Something went wrong"})
        response.status_code = 500
        return response
    else:
        response = jsonify({"XFOOD":chatbot_response})
        response.status_code = 200
        return response
   
    



if __name__ == '__main__':
    serve(app,port=3000)
