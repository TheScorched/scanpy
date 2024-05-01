import tkinter as tk
from tkinter import messagebox
import socket
import ssl

public_ips = ['x.x.x.x']  # replace with your list of public IPs
services = {
    '21': 'FTP',
    '25': 'SMTP',
    '80': 'HTTP',
    '443': 'HTTPS'
}

class CheckPortsUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Web Scanner")

        self.public_ips_label = tk.Label(self.root, text="Domain:")
        self.public_ips_label.pack()

        self.public_ips_entry = tk.Text(self.root, height=10, width=50)
        self.public_ips_entry.pack()

        self.service_label = tk.Label(self.root, text="Service:")
        self.service_label.pack()

        self.service_var = tk.StringVar()
        self.service_var.set(list(services.values())[0])
        self.service_optionmenu = tk.OptionMenu(self.root, self.service_var, *list(services.values()))
        self.service_optionmenu.pack()

        self.check_button = tk.Button(self.root, text="Send It!", command=self.check_ports)
        self.check_button.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def check_ports(self):
        public_ips = self.public_ips_entry.get("1.0", tk.END).split("\n")
        public_ips = [ip.strip() for ip in public_ips if ip.strip()]

        service = self.service_var.get()
        if service not in services.values():
            messagebox.showerror("Error", "Invalid service")
            return

        try:
            result = []
            for ip in public_ips:
                port = list(services.values()).index(service)
                port = list(services.keys())[port]
                try:
                    with socket.create_connection((ip, int(port)), timeout=5) as sock:
                        if service == 'HTTP':
                            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                            if b"HTTP" in sock.recv(100):
                                result.append(f'{ip}: Port {port} running HTTP')
                        elif service == 'HTTPS':
                            context = ssl.create_default_context()
                            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                                ssock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                                if b"HTTP" in ssock.recv(100):
                                    result.append(f'{ip}: Port {port} running HTTPS')
                        elif service == 'SMTP':
                            response = sock.recv(100)
                            if b"SMTP" in response or b"220" in response:
                                result.append(f'{ip}: Port {port} running SMTP')
                        elif service == 'FTP':
                            response = sock.recv(100)
                            if b"FTP" in response or b"220" in response:
                                result.append(f'{ip}: Port {port} running FTP')
                            else:
                                result.append(f'{ip}: Port {port} open, service unknown')
                        else:
                            result.append(f'{ip}: Port {port} open, service unknown')
                except (socket.timeout, socket.error, ssl.SSLError) as e:
                    result.append(f'{ip}: Port {port} check failed - {e}')
            self.result_label.config(text="\n".join(result))
        except:
            messagebox.showerror("Error", "Invalid input")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = CheckPortsUI()
    ui.run()
