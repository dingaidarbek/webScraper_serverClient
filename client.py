import socket
import xml.etree.ElementTree as ET
import sys

# Client configuration
HOST = '127.0.0.1' 
PORT = 65432      

# Read an XML query from a file
def read_query_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

# Save the server response to an XML file
def save_response_to_file(response_xml, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(response_xml)
    print(f"Response saved to {file_name}")

# Display the response from the server
def display_response(response_xml):
    root = ET.fromstring(response_xml)
    status = root.find('status').text
    print("Status:", status)

    if status == 'success':
        data = root.find('data')
        if data is not None:  # Check if the data element exists
            for row in data.findall('row'):
                print("Employee:")
                for element in row:
                    print(f"  {element.tag.capitalize()}: {element.text}")
        else:
            print("No matching records found.")
    elif status == 'fail':
        print("Query failed. Invalid column(s) in the request.")

# Send the query to the server and process the response
def query_server(query_xml, response_file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(query_xml.encode('utf-8'))
        print("Query sent.")
        response_xml = client_socket.recv(1024).decode('utf-8')
        print("Response received.")

        save_response_to_file(response_xml, response_file_name)
        display_response(response_xml)

# Main function
def main():
    # Validate command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python client.py <query_file> <response_file>")
        sys.exit(1)

    query_file = sys.argv[1]
    response_file = sys.argv[2]

    # Read query from the specified file
    query_xml = read_query_from_file(query_file)

    # Send the query and save the response
    query_server(query_xml, response_file)

if __name__ == "__main__":
    main()
