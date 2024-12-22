from flask import Flask, render_template, request, redirect, url_for, flash
import networkx as nx
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = 'secret_key_for_flash_messages'

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

def build_huffman_tree(char_freq):
    nodes = [Node(char, freq) for char, freq in char_freq.items()]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = Node(None, left.freq + right.freq, left, right)
        nodes.append(merged)
    return nodes[0]

def generate_huffman_codes(root, current_code="", codes={}):
    if root is None:
        return
    if root.char is not None:
        codes[root.char] = current_code
    generate_huffman_codes(root.left, current_code + "0", codes)
    generate_huffman_codes(root.right, current_code + "1", codes)
    return codes

def encode(text, codes):
    try:
        return ''.join([codes[char] for char in text])
    except KeyError:
        return "Error: Invalid character in input."

def decode(encoded_text, root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = root
    return decoded_text

def plot_huffman_tree(node, graph=None, pos=None, x=0, y=0, layer=1):
    if graph is None:
        graph = nx.DiGraph()
        pos = {}
    if node:
        label = f'{node.char}:{node.freq:.2f}' if node.char else f'{node.freq:.2f}'
        graph.add_node(str(id(node)), label=label)
        pos[str(id(node))] = (x, y)
        if node.left:
            graph.add_edge(str(id(node)), str(id(node.left)))
            plot_huffman_tree(node.left, graph, pos, x - 1/layer, y - 1, layer + 1)
        if node.right:
            graph.add_edge(str(id(node)), str(id(node.right)))
            plot_huffman_tree(node.right, graph, pos, x + 1/layer, y - 1, layer + 1)
    return graph, pos

@app.route('/', methods=['GET', 'POST'])
def index():
    huffman_codes = {}
    encoded_text = ""
    decoded_text = ""
    char_freq = {}

    if request.method == 'POST':
        try:
            freq_input = request.form['char_freq'].strip().split(',')
            char_freq = {pair.split(':')[0].strip().upper(): float(pair.split(':')[1].strip()) for pair in freq_input}

            huffman_tree = build_huffman_tree(char_freq)
            huffman_codes = generate_huffman_codes(huffman_tree)

            action = request.form['action']
            input_text = request.form['input_text'].strip().upper()

            if action == 'encode':
                encoded_text = encode(input_text, huffman_codes)
            elif action == 'decode':
                decoded_text = decode(input_text, huffman_tree)

            graph, pos = plot_huffman_tree(huffman_tree)
            labels = nx.get_node_attributes(graph, 'label')
            plt.figure(figsize=(8, 6))
            nx.draw(graph, pos, with_labels=False, node_size=2000, node_color="lightblue", font_size=10, font_weight='bold', arrows=False)
            nx.draw_networkx_labels(graph, pos, labels)
            plt.title("Huffman Tree")
            plt.savefig('static/huffman_tree.png')
            plt.close()

        except Exception as e:
            flash(f"Error: {e}. Please enter valid input.")
            return redirect(url_for('index'))

    return render_template('index.html', huffman_codes=huffman_codes, encoded_text=encoded_text, decoded_text=decoded_text)

if __name__ == '__main__':
    app.run(debug=True)