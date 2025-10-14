#!/usr/bin/env python3

import socket

SECRET_WORD = "banana"


def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 9999))
    print("Server is running on 127.0.0.1:9999")
    print("Secret word is ready.")

    while True:
        data, addr = sock.recvfrom(1024)
        text = data.decode().strip().lower()
        print("Server got:", text, "from", addr)

        if text.lower() == "quit":
            sock.sendto(b"Goodbye!", addr)
            break

        if len(text) != len(SECRET_WORD):
            reply = "Your guess must be " + str(len(SECRET_WORD)) + " letters."
            sock.sendto(reply.encode(), addr)
            continue

        if text == SECRET_WORD:
            sock.sendto(("You found the word: " + SECRET_WORD.upper()).encode(), addr)
            break

        matches = ""
        wrong_place = ""
        for i in range(len(SECRET_WORD)):
            if text[i] == SECRET_WORD[i]:
                matches += text[i].upper()
            else:
                matches += "_"
                if text[i] in SECRET_WORD and text[i] not in wrong_place:
                    wrong_place += text[i]

        if wrong_place == "":
            wrong_place = "none"

        reply = "Matches: " + matches + " | Wrong place: " + wrong_place
        sock.sendto(reply.encode(), addr)

    sock.close()
    print("Server stopped.")


def run_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ("127.0.0.1", 9999)
    print("Client is running. Type messages to send.")
    print(f"Try to guess the {len(SECRET_WORD)} letter word. Type quit to stop.")

    while True:
        message = input("Message (type quit to stop): ")
        sock.sendto(message.encode(), server)

        data, _ = sock.recvfrom(1024)
        print("Server replied:", data.decode())

        if message.lower() == "quit":
            break

        if data.decode().startswith("You found"):
            break

    sock.close()
    print("Client stopped.")


if __name__ == "__main__":
    mode = input("Choose mode (server/client): ").strip().lower()

    if mode == "server":
        run_server()
    elif mode == "client":
        run_client()
    else:
        print("Unknown mode. Please run again and type server or client.")
