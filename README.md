# Penetration Testing Tool

A collection of Python-based penetration testing and security scanning tools.

## Features

- **TCPServer/TCPClient**: SSL/TLS encrypted TCP client-server communication for remote command execution
- **PortScanner**: Simple TCP port scanner to check if ports are open or closed
- **BannerGrabber**: Grab service banners from remote servers
- **Nmap Scanner**: Python wrapper for nmap with support for SYN ACK, UDP, and comprehensive scans

## Project Structure

```
PenetrationTesting/
├── TCPSocket/
│   ├── TCPServer.py    # SSL-enabled TCP server for remote command execution
│   ├── TCPClient.py    # SSL-enabled TCP client
│   ├── server.crt      # SSL certificate
│   └── server.key      # SSL private key
├── PortScanner/
│   └── PortScanner.py  # TCP port scanner
├── BannerGrabber/
│   └── bannergrabber.py # Service banner grabber
├── Nmap/
│   └── scanner.py      # Nmap Python wrapper
└── tests/
    ├── test_tcpserver.py      # Unit tests for TCPServer
    ├── test_tcpclient.py      # Unit tests for TCPClient
    ├── test_portscanner.py    # Unit tests for PortScanner
    ├── test_bannergrabber.py  # Unit tests for BannerGrabber
    └── test_scanner.py        # Unit tests for Nmap scanner
```

## Requirements

- Python 3.6+
- nmap (for Nmap scanner module)
- python-nmap library (for Nmap scanner module)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Penetration-Testing-Tool-.git
cd Penetration-Testing-Tool-
```

2. Install required dependencies (for Nmap scanner):
```bash
pip install python-nmap
```

## Usage

### Port Scanner
```python
from PenetrationTesting.PortScanner.PortScanner import scan_port

# Scan a single port
is_open = scan_port('192.168.1.1', 80)
print("Port 80 is", "open" if is_open else "closed")
```

### Banner Grabber
```python
from PenetrationTesting.BannerGrabber.bannergrabber import grab_banner

# Grab banner from SSH service
banner = grab_banner('192.168.1.1', 22)
print(f"SSH Banner: {banner}")
```

### TCP Server/Client
```bash
# Start the server (requires server.crt and server.key)
cd PenetrationTesting/TCPSocket
python TCPServer.py

# In another terminal, start the client
python TCPClient.py
```

### Nmap Scanner
```python
from PenetrationTesting.Nmap.scanner import create_scanner, syn_ack_scan

scanner = create_scanner()
results = syn_ack_scan(scanner, '192.168.1.1', '1-100')
print(f"Open ports: {results['open_ports']}")
```

## Running Tests

The project includes a comprehensive test suite using Python's `unittest` framework.

### Run All Tests
```bash
# From the project root directory
python -m unittest discover -s tests -v
```

### Run Specific Test Files
```bash
# Run TCPServer tests
python -m unittest tests.test_tcpserver -v

# Run TCPClient tests
python -m unittest tests.test_tcpclient -v

# Run PortScanner tests
python -m unittest tests.test_portscanner -v

# Run BannerGrabber tests
python -m unittest tests.test_bannergrabber -v

# Run Nmap Scanner tests
python -m unittest tests.test_scanner -v
```

### Using pytest (Alternative)
If you have pytest installed:
```bash
pip install pytest
pytest tests/ -v
```

## Test Coverage

The test suite covers:
- **TCPServer Module**:
  - Command translation (Unix to Windows)
  - Command execution
  - Client handling
  - Socket creation with and without SSL

- **TCPClient Module**:
  - Socket creation with and without SSL
  - Server connection
  - Command sending and response receiving

- **PortScanner Module**:
  - Socket creation with configurable timeout
  - Port scanning (open/closed detection)
  - Error handling (timeouts, connection errors)

- **BannerGrabber Module**:
  - Banner grabbing functionality
  - Timeout handling
  - Error handling for connection failures

- **Nmap Scanner Module**:
  - Scanner creation
  - SYN ACK, UDP, and comprehensive scans
  - Input validation

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Disclaimer

This tool is intended for authorized security testing and educational purposes only. Always obtain proper authorization before testing systems you do not own.

## License

This project is open-source. Please use responsibly and ethically.
