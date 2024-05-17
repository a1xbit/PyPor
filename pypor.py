import datetime
import socket
import pyfiglet

ascii_banner = pyfiglet.figlet_format("PyPor")
print(ascii_banner)


def verify_interface(node, port):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        c.settimeout(1)  # Setting a timeout for the connection attempt
        c.connect((node, port))
        c.close()
        return True, None
    except socket.error as e:
        return False, str(e)


output_file_name = "ScanOutcome.txt"

# Seek user input
node = input("Enter a host to scan: ")

# Get current time
begin_time = datetime.datetime.now()

# Verify the validity of the IP address
try:
    node_ip_address = socket.gethostbyname(node)
    print("The IP Address is accurate.\n")
except socket.error:
    print("The IP Address is inaccurate.")
    exit()

try:
    with open(output_file_name, "w") as output_file:
        output_file.write(f"Scan for {node_ip_address} began at {begin_time}\n")

        open_ports = []
        closed_ports = []
        exceptions = []
        for port in range(1, 65536):
            result, error_msg = verify_interface(node_ip_address, port)
            if result:
                open_ports.append(port)
                output_file.write(f"Port {port} is open\n")
            else:
                closed_ports.append(port)
                if error_msg and "Errno 61" in error_msg:  # Check for Errno 61 specifically
                    exceptions.append(f"Port {port}: Connection refused\n")
                else:
                    exceptions.append(f"Port {port}: {error_msg}\n")

        finish_time = datetime.datetime.now()
        duration = finish_time - begin_time

        output_file.write(f"Scan concluded at {finish_time}\n")
        output_file.write(f"Duration of scan: {duration.total_seconds()} seconds\n")

        if open_ports:
            output_file.write(f"Open ports found: {', '.join(map(str, open_ports))}\n")

        if closed_ports:
            output_file.write(f"Closed ports found: {', '.join(map(str, closed_ports))}\n")

        if exceptions:
            output_file.write("\nExceptions:\n")
            for exc in exceptions:
                output_file.write(exc)

    print("Operation finished. The chosen interfaces have been analyzed.")
    print("Scan concluded at:", finish_time)
    print("Duration of scan:", duration, "secs.")

except IOError as e:
    print(f"Error: {e}")
