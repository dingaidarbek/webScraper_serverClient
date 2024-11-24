import socket
import xml.etree.ElementTree as ET
import os

HOST = '127.0.0.1' 
PORT = 65432      

def read_query_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

def save_response_to_file(response_xml, file_name="server_response.xml"):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(response_xml)
    print(f"Response saved to {file_name}")

def display_response(response_xml):
    root = ET.fromstring(response_xml)
    status = root.find('status').text
    print("Status:", status)

    if status == 'success':
        data = root.find('data')
        for row in data.findall('row'):
            print("Employee:")
            for element in row:
                print(f"  {element.tag.capitalize()}: {element.text}")
    elif status == 'no results':
        message = root.find('message').text if root.find('message') is not None else "No matching records found."
        print(message)
    elif status == 'failure':
        message = root.find('message').text if root.find('message') is not None else "An error occurred."
        print("Error:", message)

def query_server(query_xml, save_to_file=False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(query_xml.encode('utf-8'))
        print("Query sent.")
        response_xml = client_socket.recv(1024).decode('utf-8')
        print("Response received.")

        if save_to_file:
            save_response_to_file(response_xml)

        display_response(response_xml)

def main():
    files = [f for f in os.listdir('.') if f.endswith('.xml')]
    if not files:
        print("No XML files found in the current folder.")
        return
    print("Available XML files:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    file_choice = input("Enter the number of the file to use: ")
    try:
        file_index = int(file_choice) - 1
        if 0 <= file_index < len(files):
             query_xml = read_query_from_file(files[file_index])
             if query_xml:
              query_server(query_xml, save_to_file=True)
        else:
            print("Invalid choice.")
    except ValueError:
            print("Invalid input. Please enter a number.")
if __name__ == "__main__":
    main()
