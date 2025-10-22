import re
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

class InfixConverter:
    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def is_operator(self, c):
        return c in self.precedence

    def is_operand(self, c):
        return c.isalnum()

    def infix_to_postfix(self, infix):
        stack = Stack()
        postfix = ''
        for c in infix:
            if c == ' ':
                continue
            if self.is_operand(c):
                postfix += c
            elif c == '(':
                stack.push(c)
            elif c == ')':
                while not stack.is_empty() and stack.peek() != '(':
                    postfix += stack.pop()
                stack.pop()
            elif self.is_operator(c):
                while not stack.is_empty() and stack.peek() != '(' and \
                      self.precedence.get(stack.peek(), 0) >= self.precedence[c]:
                    postfix += stack.pop()
                stack.push(c)
        while not stack.is_empty():
            postfix += stack.pop()
        return postfix

    def infix_to_prefix(self, infix):
        rev = infix[::-1].replace('(', 'temp').replace(')', '(').replace('temp', ')')
        stack = Stack()
        prefix = ''
        for c in rev:
            if c == ' ':
                continue
            if self.is_operand(c):
                prefix += c
            elif c == '(':
                stack.push(c)
            elif c == ')':
                while not stack.is_empty() and stack.peek() != '(':
                    prefix += stack.pop()
                stack.pop()
            elif self.is_operator(c):
                while not stack.is_empty() and stack.peek() != '(' and \
                      self.precedence.get(stack.peek(), 0) > self.precedence[c]:
                    prefix += stack.pop()
                stack.push(c)
        while not stack.is_empty():
            prefix += stack.pop()
        return prefix[::-1]

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        infix = data.get('infix', '')
        conv_type = data.get('type', 'postfix')
        
        converter = InfixConverter()
        
        if conv_type == 'postfix':
            result = converter.infix_to_postfix(infix)
        else:
            result = converter.infix_to_prefix(infix)
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

