#!/usr/bin/env python3
"""Unit tests for TCPClient module."""

import unittest
import socket
import ssl
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PenetrationTesting.TCPSocket.TCPClient import (
    create_client_socket,
    connect_to_server,
    send_command,
    receive_response
)


class TestCreateClientSocket(unittest.TestCase):
    """Tests for the create_client_socket function."""
    
    @patch('PenetrationTesting.TCPSocket.TCPClient.ssl.create_default_context')
    @patch('PenetrationTesting.TCPSocket.TCPClient.socket.socket')
    def test_create_client_socket_with_ssl(self, mock_socket_class, mock_ssl_context):
        """Test creating a client socket with SSL enabled."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_context = Mock()
        mock_ssl_context.return_value = mock_context
        mock_wrapped_socket = Mock()
        mock_context.wrap_socket.return_value = mock_wrapped_socket
        
        result = create_client_socket('localhost', 8000, use_ssl=True)
        
        mock_socket_class.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_ssl_context.assert_called_once()
        self.assertFalse(mock_context.check_hostname)
        self.assertEqual(mock_context.verify_mode, ssl.CERT_NONE)
        mock_context.wrap_socket.assert_called_once_with(mock_socket, server_hostname='localhost')
        self.assertEqual(result, mock_wrapped_socket)
    
    @patch('PenetrationTesting.TCPSocket.TCPClient.socket.socket')
    def test_create_client_socket_without_ssl(self, mock_socket_class):
        """Test creating a client socket without SSL."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        
        result = create_client_socket('localhost', 8000, use_ssl=False)
        
        mock_socket_class.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        self.assertEqual(result, mock_socket)


class TestConnectToServer(unittest.TestCase):
    """Tests for the connect_to_server function."""
    
    def test_connect_to_server(self):
        """Test connecting to a server."""
        mock_socket = Mock()
        
        connect_to_server(mock_socket, '127.0.0.1', 8000)
        
        mock_socket.connect.assert_called_once_with(('127.0.0.1', 8000))
    
    def test_connect_to_server_different_port(self):
        """Test connecting to a server on a different port."""
        mock_socket = Mock()
        
        connect_to_server(mock_socket, 'example.com', 443)
        
        mock_socket.connect.assert_called_once_with(('example.com', 443))


class TestSendCommand(unittest.TestCase):
    """Tests for the send_command function."""
    
    def test_send_command(self):
        """Test sending a command."""
        mock_socket = Mock()
        
        send_command(mock_socket, 'ls -la')
        
        mock_socket.send.assert_called_once_with(b'ls -la')
    
    def test_send_empty_command(self):
        """Test sending an empty command."""
        mock_socket = Mock()
        
        send_command(mock_socket, '')
        
        mock_socket.send.assert_called_once_with(b'')
    
    def test_send_special_characters(self):
        """Test sending a command with special characters."""
        mock_socket = Mock()
        
        send_command(mock_socket, 'echo "hello world"')
        
        mock_socket.send.assert_called_once_with(b'echo "hello world"')


class TestReceiveResponse(unittest.TestCase):
    """Tests for the receive_response function."""
    
    def test_receive_response(self):
        """Test receiving a response."""
        mock_socket = Mock()
        mock_socket.recv.return_value = b'file1.txt\nfile2.txt'
        
        result = receive_response(mock_socket)
        
        mock_socket.recv.assert_called_once_with(4096)
        self.assertEqual(result, 'file1.txt\nfile2.txt')
    
    def test_receive_response_custom_buffer_size(self):
        """Test receiving a response with custom buffer size."""
        mock_socket = Mock()
        mock_socket.recv.return_value = b'data'
        
        result = receive_response(mock_socket, buffer_size=1024)
        
        mock_socket.recv.assert_called_once_with(1024)
        self.assertEqual(result, 'data')
    
    def test_receive_empty_response(self):
        """Test receiving an empty response."""
        mock_socket = Mock()
        mock_socket.recv.return_value = b''
        
        result = receive_response(mock_socket)
        
        self.assertEqual(result, '')


class TestClientIntegration(unittest.TestCase):
    """Integration tests for client functionality."""
    
    def test_send_and_receive_workflow(self):
        """Test the typical send command and receive response workflow."""
        mock_socket = Mock()
        mock_socket.recv.return_value = b'command output'
        
        # Send a command
        send_command(mock_socket, 'whoami')
        mock_socket.send.assert_called_with(b'whoami')
        
        # Receive response
        response = receive_response(mock_socket)
        self.assertEqual(response, 'command output')


if __name__ == '__main__':
    unittest.main()
