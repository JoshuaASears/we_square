
# import smtplib
import socket
import webbrowser

def get_email_body(ledger_json):
    # socket connection
    HOST = 'localhost'
    PORT = 65432
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Connected to server: {HOST}:{PORT}...")

    # application handshake (client message length verification)
    message_length = str(len(ledger_json))
    print(f"\n\tSending message length {message_length}...")
    client_socket.send(message_length.encode())
    print(f"\tReceiving length confirmation....")
    length_verification = client_socket.recv(1024).decode()
    print(f"\tReceived message length {length_verification}...")

    # application message transmission and service reception
    html_doc =''
    if length_verification == message_length:
        print(f"\n\tVerification successful, sending Ledger to server.")
        client_socket.send(ledger_json.encode())
        print("\tSent Ledger to server successfully.")
        while True:
            print("\tReceiving...")
            response = client_socket.recv(1024).decode()
            html_doc += response

            if not response:
                print(f'\nFinished receiving, closing socket.')
                break
    else:
        print(f"\n\tVerification unsuccessful. Closing connection")
    client_socket.close()
    return html_doc

def temp_web_handler(file):
    """Temp web handler in place of full email protocol."""
    webbrowser.open(file)


#TODO: Actual email protocol.
# Modify with GOOGLE API or spike other options.
# Starter code below

# def send_email(body, outgoing_address):
#
#     from_address = ""     # needs email address
#     to_address = ""       # needs email address
#     subject = "We_Square ledger receipt!"
#     message = "From: %s\r\n" % from_address \
#             + "To: %s\r\n" % to_address \
#             + "Subject: %s\r\n" % subject \
#             + "Bcc: %s\r\n" % outgoing_address \
#             + "\r\n" \
#             + "%s" % body
#
#
#     try:
#         send_server = smtplib.SMTP(
#             host='localhost',
#             timeout=10
#         )
#         send_server.set_debuglevel(1)
#         send_server.sendmail(from_address, to_address, message)
#         send_server.quit()
#         return True
#     except TimeoutError:
#         return False
