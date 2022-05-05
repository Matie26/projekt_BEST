from flask import Flask, request

app = Flask(__name__)
indices = [22, 26, 48, 59, 62, 65, 68, 79] 
f = open("received.txt", "a")

def byte_to_ascii(byte):
    return chr(int(''.join([str(bit) for bit in byte]), 2))

def get_secret(request):
    bits = []
    user_agent = 'User-Agent: ' + str(request.__dict__['headers']['User-Agent'])
    for index in indices:
        bits.append(user_agent[index])    
    bits = list(map(lambda x: x.replace('l', '0'), bits))
    f.write(byte_to_ascii(bits))

@app.route("/")
def home():
    get_secret(request)
    return 'Hello'
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)