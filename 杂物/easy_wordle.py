from fileinput import filename
import socketserver
import signal
import random
import os


class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'[-] '):
        self.send(prompt, newline=False)
        return self._recvall()

    def wordle_game(self, word_list):
        target = random.choice(word_list)
        attempts = 6

        self.send("欢迎来到Wordle!".encode())
        self.send("你有6次机会猜出一个5个字母的单词。".encode())

        while attempts > 0:
            guess = self.recv(f"尝试{7 - attempts}: ".encode())
            guess = guess.decode().lower()
            if len(guess) != 5:
                self.send("请输入一个5个字母的单词!")
                continue

            feedback = self.get_feedback(target, guess)
            feedback = " ".join(feedback)
            feedback = feedback.encode()
            self.send(feedback)

            if guess == target:
                self.send("恭喜你猜对了!".encode())
                return True
            else:
                attempts -= 1

        print(f"很遗憾，你没有猜出来。正确答案是{target}。")
        
        return False
        
    
    def get_feedback(self, target, guess):
        feedback = []
        for t, g in zip(target, guess):
            if t == g:
                feedback.append('绿')
            elif g in target:
                feedback.append('黄')
            else:
                feedback.append('灰')
        return feedback

    def handle(self):
        signal.alarm(60) # type: ignore
        if not self.wordle_game(word_list):
            self.send(b'[!] Wrong!')
            return

        self.send(b'here is your flag')
        self.send(flag)


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):# type: ignore
    pass


if __name__ == "__main__":
    flag = bytes(os.getenv("FLAG"),"utf-8")
    # flag = b'flagis123'
    with open('wordlist.txt', 'r') as file:
        word_list = [line.strip() for line in file]
    HOST, PORT = '0.0.0.0', 10001
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    print(HOST, PORT)
    server.serve_forever()
