import socket
import threading
import customtkinter as ctk
from tkinter import messagebox

# Global variables for server and clients
server = None
server_running = False
clients = []  # List to store active client sockets


# Function to handle client connection
def handle_client(client_socket, label):
    global clients
    clients.append(client_socket)  # Add the client to the list of active clients
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Print the received message in the CTkLabel
            message = data.decode('utf-8')
            update_label(label, f"Received message: {message}")

            # Echo the message back to the client
            client_socket.send(data)
    except ConnectionResetError:
        pass
    finally:
        # Safely remove the client from the list and close the connection
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()
        update_label(label, "[*] Client disconnected.")


# Function to update the CTkLabel with new text
def update_label(label, text):
    current_text = label.cget("text")  # Get the current text
    new_text = current_text + "\n" + text  # Append the new message
    label.configure(text=new_text)  # Update the label text


# Function to start the server
def start_server(label):
    global server, server_running
    if server_running:
        messagebox.showinfo("Server Status", "The server is already running!")
        return

    # Create and bind the socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the same port
    server.bind(('0.0.0.0', 5555))
    server.listen(5)

    server_running = True
    update_label(label, "[*] Server listening on port 5555")

    while server_running:
        try:
            # Accept new client connections
            client, addr = server.accept()
            if not server_running:  # Break the loop if server is stopped
                break

            update_label(label, f"[*] Accepted connection from {addr[0]}:{addr[1]}")

            # Start a new thread to handle the client
            client_handler = threading.Thread(target=handle_client, args=(client, label))
            client_handler.start()
        except socket.error:
            break

    update_label(label, "[*] Server stopped.")  # Notify that the server has stopped


# Function to stop the server
def stop_server(label):
    global server, server_running, clients
    if server_running:
        server_running = False  # Stop the server loop
        server.close()  # Close the server socket to stop listening

        # Disconnect all clients
        for client in clients:
            try:
                client.close()
            except Exception:
                pass
        clients.clear()  # Clear the client list

        update_label(label, "[*] Server has stopped listening and all clients disconnected.")
    else:
        messagebox.showinfo("Server Status", "The server is not running!")


# Function to cut connections with all clients
def cut_connections(label):
    global clients
    if clients:
        for client in clients:
            try:
                client.close()  # Close each client socket
            except Exception:
                pass
        clients.clear()  # Clear the client list
        update_label(label, "[*] All client connections have been cut.")
    else:
        update_label(label, "[*] No active client connections to cut.")


# GUI setup
root = ctk.CTk()
root.geometry("400x400")
root.resizable(False, False)
root.title("Script")
root.iconbitmap("D:\\My Projects\\Pycharm\\script_chat\\images\\icon_app.ico")

# Create a CTkLabel to display messages
label = ctk.CTkLabel(master=root, text="Typing", fg_color="black", text_color="green", width=400, height=300,
                     corner_radius=5)
label.place(anchor="w",rely=0.8)

# Create a button to start the connection
Button_start = ctk.CTkButton(master=root, bg_color='transparent', text="Start Connection", fg_color="green",
                             text_color="black", corner_radius=3,
                             command=lambda: threading.Thread(target=start_server, args=(label,)).start())
Button_start.place(anchor="w",relx=0.3,rely=0.1)

# Create a button to close the server
Button_close = ctk.CTkButton(master=root, bg_color='transparent', text="Close Server", fg_color="red",
                             text_color="black", corner_radius=3, command=lambda: stop_server(label))
Button_close.place(anchor="w",relx=0.3,rely=0.2)

# Create a button to cut all client connections
Button_cut = ctk.CTkButton(master=root, bg_color='transparent', text="Cut Connections", fg_color="orange",
                           text_color="black", corner_radius=3, command=lambda: cut_connections(label))
Button_cut.place(anchor="w",relx=0.3,rely=0.3)

# Run the Tkinter event loop
root.mainloop()
