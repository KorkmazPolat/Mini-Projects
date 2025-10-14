#!/usr/bin/env python3

import socket
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("UDP Guess Game Client")
    font = pygame.font.SysFont(None, 32)
    small_font = pygame.font.SysFont(None, 24)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = ("127.0.0.1", 9999)
    sock.settimeout(2.0)

    input_text = ""
    messages = ["Type your guesses and press Enter.", "Press ESC to quit."]
    running = True

    clock = pygame.time.Clock()

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    guess = input_text.strip()
                    if guess:
                        try:
                            sock.sendto(guess.encode(), server_addr)
                            data, _ = sock.recvfrom(1024)
                            reply = data.decode()
                        except socket.timeout:
                            reply = "No response from server."

                        messages.append("You: " + guess)
                        messages.append("Server: " + reply)
                        if "You found the word" in reply:
                            running = False
                        input_text = ""
                    else:
                        messages.append("Please type something.")
                else:
                    if event.unicode.isprintable():
                        input_text += event.unicode

        screen.fill((30, 30, 30))

        input_surface = font.render("Guess: " + input_text, True, (255, 255, 255))
        screen.blit(input_surface, (20, 340))

        show_messages = messages[-10:]
        y = 20
        for line in show_messages:
            text_surface = small_font.render(line, True, (200, 200, 200))
            screen.blit(text_surface, (20, y))
            y += 30

        pygame.display.flip()

    try:
        sock.sendto(b"quit", server_addr)
    except OSError:
        pass
    sock.close()
    pygame.quit()


if __name__ == "__main__":
    main()
