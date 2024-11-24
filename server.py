import socket
import xml.etree.ElementTree as ET
import csv

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

# Load the employee dataset
def load_dataset(file_path="directory.csv"):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

# Process the client query
def process_query(query_xml, dataset):
    root = ET.fromstring(query_xml)
    filters = []

    # Validate columns in the dataset
    valid_columns = set(dataset[0].keys()) if dataset else {"name", "title", "email"}

    # Extract and validate conditions
    for condition in root.findall('condition'):
        column = condition.find('column').text.strip()
        value = condition.find('value').text.strip()
        if column not in valid_columns:  # Invalid column check
            response = ET.Element('result')
            status = ET.SubElement(response, 'status')
            status.text = 'fail'
            return ET.tostring(response, encoding='unicode')
        filters.append((column, value))

    # Filter the dataset
    filtered_data = dataset
    for column, value in filters:
        filtered_data = [row for row in filtered_data if row.get(column, '').strip() == value]

    # Generate the response
    response = ET.Element('result')
    status = ET.SubElement(response, 'status')

    if filtered_data:  # Valid query and data exists
        status.text = 'success'
        data = ET.SubElement(response, 'data')
        for row in filtered_data:
            row_element = ET.SubElement(data, 'row')
            for key, value in row.items():
                key_element = ET.SubElement(row_element, key.lower())
                key_element.text = value
    else:  # Valid query but no matching records
        status.text = 'success'

    return ET.tostring(response, encoding='unicode')

# Start the server
def start_server():
    dataset = load_dataset()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server is listening on {HOST}:{PORT}...")
        
        while True:  # Allow multiple connections
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                query_xml = conn.recv(1024).decode('utf-8')
                print("Received query:", query_xml)
                response_xml = process_query(query_xml, dataset)
                conn.sendall(response_xml.encode('utf-8'))
                print("Response sent.")

if __name__ == "__main__":
    start_server()
