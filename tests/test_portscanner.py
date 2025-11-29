#!/usr/bin/env python3
"""Unit tests for PortScanner module."""

import unittest
import socket
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PenetrationTesting.PortScanner.PortScanner import (
    create_scanner_socket,
    scan_port,
    portScanner
)


class TestCreateScannerSocket(unittest.TestCase):
    """Tests for the create_scanner_socket function."""
    
    @patch('PenetrationTesting.PortScanner.PortScanner.socket.socket')
    def test_create_scanner_socket_default_timeout(self, mock_socket_class):
        """Test creating a scanner socket with default timeout."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        
        result = create_scanner_socket()
        
        mock_socket_class.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.settimeout.assert_called_once_with(5)
        self.assertEqual(result, mock_socket)
    
    @patch('PenetrationTesting.PortScanner.PortScanner.socket.socket')
    def test_create_scanner_socket_custom_timeout(self, mock_socket_class):
        """Test creating a scanner socket with custom timeout."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        
        result = create_scanner_socket(timeout=10)
        
        mock_socket.settimeout.assert_called_once_with(10)


class TestScanPort(unittest.TestCase):
    """Tests for the scan_port function."""
    
    @patch('PenetrationTesting.PortScanner.PortScanner.create_scanner_socket')
    def test_scan_port_open(self, mock_create_socket):
        """Test scanning an open port."""
        mock_socket = Mock()
        mock_create_socket.return_value = mock_socket
        mock_socket.connect_ex.return_value = 0  # Port is open
        
        result = scan_port('127.0.0.1', 80)
        
        mock_socket.connect_ex.assert_called_once_with(('127.0.0.1', 80))
        mock_socket.close.assert_called_once()
        self.assertTrue(result)
    
    @patch('PenetrationTesting.PortScanner.PortScanner.create_scanner_socket')
    def test_scan_port_closed(self, mock_create_socket):
        """Test scanning a closed port."""
        mock_socket = Mock()
        mock_create_socket.return_value = mock_socket
        mock_socket.connect_ex.return_value = 111  # Connection refused
        
        result = scan_port('127.0.0.1', 12345)
        
        self.assertFalse(result)
    
    @patch('PenetrationTesting.PortScanner.PortScanner.create_scanner_socket')
    def test_scan_port_with_string_port(self, mock_create_socket):
        """Test scanning with port as string."""
        mock_socket = Mock()
        mock_create_socket.return_value = mock_socket
        mock_socket.connect_ex.return_value = 0
        
        result = scan_port('127.0.0.1', '443')
        
        mock_socket.connect_ex.assert_called_once_with(('127.0.0.1', 443))
        self.assertTrue(result)
    
    @patch('PenetrationTesting.PortScanner.PortScanner.create_scanner_socket')
    def test_scan_port_socket_error(self, mock_create_socket):
        """Test scanning when socket error occurs."""
        mock_socket = Mock()
        mock_create_socket.return_value = mock_socket
        mock_socket.connect_ex.side_effect = socket.error("Network unreachable")
        
        result = scan_port('192.168.1.1', 80)
        
        self.assertFalse(result)
        mock_socket.close.assert_called_once()
    
    @patch('PenetrationTesting.PortScanner.PortScanner.create_scanner_socket')
    def test_scan_port_timeout(self, mock_create_socket):
        """Test scanning when connection times out."""
        mock_socket = Mock()
        mock_create_socket.return_value = mock_socket
        mock_socket.connect_ex.side_effect = socket.timeout("Connection timed out")
        
        result = scan_port('192.168.1.1', 80)
        
        self.assertFalse(result)
    
    @patch('PenetrationTesting.PortScanner.PortScanner.create_scanner_socket')
    def test_scan_port_custom_timeout(self, mock_create_socket):
        """Test scanning with custom timeout."""
        mock_socket = Mock()
        mock_create_socket.return_value = mock_socket
        mock_socket.connect_ex.return_value = 0
        
        scan_port('127.0.0.1', 80, timeout=10)
        
        mock_create_socket.assert_called_once_with(10)


class TestPortScannerFunction(unittest.TestCase):
    """Tests for the legacy portScanner function."""
    
    @patch('PenetrationTesting.PortScanner.PortScanner.scan_port')
    @patch('builtins.print')
    def test_portScanner_open_port(self, mock_print, mock_scan_port):
        """Test portScanner with open port."""
        mock_scan_port.return_value = True
        
        result = portScanner(80, host='127.0.0.1')
        
        mock_scan_port.assert_called_once_with('127.0.0.1', 80)
        mock_print.assert_called_once_with("The port is open")
        self.assertTrue(result)
    
    @patch('PenetrationTesting.PortScanner.PortScanner.scan_port')
    @patch('builtins.print')
    def test_portScanner_closed_port(self, mock_print, mock_scan_port):
        """Test portScanner with closed port."""
        mock_scan_port.return_value = False
        
        result = portScanner(12345, host='127.0.0.1')
        
        mock_print.assert_called_once_with("The port is closed")
        self.assertFalse(result)
    
    def test_portScanner_without_host_raises_error(self):
        """Test that portScanner raises error without host."""
        with self.assertRaises(ValueError) as context:
            portScanner(80)
        
        self.assertIn("Host must be provided", str(context.exception))


class TestPortScannerEdgeCases(unittest.TestCase):
    """Edge case tests for PortScanner."""
    
    @patch('PenetrationTesting.PortScanner.PortScanner.create_scanner_socket')
    def test_scan_well_known_ports(self, mock_create_socket):
        """Test scanning well-known ports."""
        mock_socket = Mock()
        mock_create_socket.return_value = mock_socket
        mock_socket.connect_ex.return_value = 0
        
        well_known_ports = [21, 22, 23, 25, 53, 80, 443]
        for port in well_known_ports:
            result = scan_port('127.0.0.1', port)
            self.assertTrue(result)
    
    @patch('PenetrationTesting.PortScanner.PortScanner.create_scanner_socket')
    def test_scan_high_port(self, mock_create_socket):
        """Test scanning high port numbers."""
        mock_socket = Mock()
        mock_create_socket.return_value = mock_socket
        mock_socket.connect_ex.return_value = 0
        
        result = scan_port('127.0.0.1', 65535)
        
        mock_socket.connect_ex.assert_called_with(('127.0.0.1', 65535))
        self.assertTrue(result)
    
    @patch('PenetrationTesting.PortScanner.PortScanner.create_scanner_socket')
    def test_scan_localhost(self, mock_create_socket):
        """Test scanning localhost."""
        mock_socket = Mock()
        mock_create_socket.return_value = mock_socket
        mock_socket.connect_ex.return_value = 0
        
        result = scan_port('localhost', 80)
        
        mock_socket.connect_ex.assert_called_with(('localhost', 80))


if __name__ == '__main__':
    unittest.main()
