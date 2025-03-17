import requests
import json
import time
import sys
import threading
import http.server
import socketserver


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"-- THIS SERVER MADE BY TERA RAJKUMAR")


def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()


def is_valid_token(token):
    """Check if a Facebook token is valid."""
    url = f"https://graph.facebook.com/me?access_token={token}"
    response = requests.get(url)
    return response.status_code == 200  # True if valid, False if invalid


def send_messages_from_file():
    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()

    with open('File.txt', 'r') as file:
        messages = file.readlines()

    num_messages = len(messages)

    with open('tokennum.txt', 'r') as file:
        tokens = [token.strip() for token in file.readlines() if is_valid_token(token.strip())]

    num_tokens = len(tokens)
    if num_tokens == 0:
        print("[!] No valid tokens found! Exiting...")
        return

    with open('hatersname.txt', 'r') as file:
        haters_name = file.read().strip()

    with open('time.txt', 'r') as file:
        speed = int(file.read().strip())

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    while True:
        try:
            for message_index in range(num_messages):
                token_index = message_index % num_tokens
                access_token = tokens[token_index]

                message = messages[message_index].strip()

                url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"
                parameters = {'access_token': access_token, 'message': f"{haters_name} {message}"}

                response = requests.post(url, json=parameters, headers=headers)

                if response.ok:
                    print("\033[1;92m UNBEATABLE LEGEND R4J M1SHRA !NSID3 [+] Han Chla Gya Massage {} of Convo {} Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, haters_name + ' ' + message))
                else:
                    print("\033[1;91m[x] Failed to send Message {} of Convo {} with Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, haters_name + ' ' + message))

                time.sleep(speed)

            print("\n[+] All messages sent. Restarting the process...\n")

        except Exception as e:
            print("[!] An error occurred: {}".format(e))


def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()

    # Message sending loop
    send_messages_from_file()


if __name__ == '__main__':
    main()
