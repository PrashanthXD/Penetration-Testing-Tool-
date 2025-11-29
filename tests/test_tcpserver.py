#!/usr/bin/env python3
"""Unit tests for TCPServer module."""

import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PenetrationTesting.TCPSocket.TCPServer import (
    translate_command,
    execute_command,
    handle_client,
    create_server_socket
)


class TestTranslateCommand(unittest.TestCase):
    """Tests for the translate_command function."""
    
    @patch('PenetrationTesting.TCPSocket.TCPServer.os.name', 'nt')
    def test_translate_ls_on_windows(self):
        """Test that 'ls' is translated to 'dir' on Windows."""
        result = translate_command('ls')
        self.assertEqual(result, 'dir')
    
    @patch('PenetrationTesting.TCPSocket.TCPServer.os.name', 'nt')
    def test_translate_pwd_on_windows(self):
        """Test that 'pwd' is translated to 'cd' on Windows."""
        result = translate_command('pwd')
        self.assertEqual(result, 'cd')
    
    @patch('PenetrationTesting.TCPSocket.TCPServer.os.name', 'nt')
    def test_no_translation_needed_on_windows(self):
        """Test that other commands are not translated on Windows."""
        result = translate_command('echo hello')
        self.assertEqual(result, 'echo hello')
    
    @patch('PenetrationTesting.TCPSocket.TCPServer.os.name', 'posix')
    def test_no_translation_on_posix(self):
        """Test that 'ls' is not translated on POSIX systems."""
        result = translate_command('ls')
        self.assertEqual(result, 'ls')
    
    @patch('PenetrationTesting.TCPSocket.TCPServer.os.name', 'posix')
    def test_pwd_not_translated_on_posix(self):
        """Test that 'pwd' is not translated on POSIX systems."""
        result = translate_command('pwd')
        self.assertEqual(result, 'pwd')


class TestExecuteCommand(unittest.TestCase):
    """Tests for the execute_command function."""
    
    @patch('PenetrationTesting.TCPSocket.TCPServer.subprocess.getoutput')
    def test_execute_command_returns_output(self, mock_getoutput):
        """Test that execute_command returns the command output."""
        mock_getoutput.return_value = 'test output'
        result = execute_command('echo test')
        self.assertEqual(result, 'test output')
        mock_getoutput.assert_called_once_with('echo test')
    
    @patch('PenetrationTesting.TCPSocket.TCPServer.subprocess.getoutput')
    def test_execute_command_handles_empty_output(self, mock_getoutput):
        """Test that execute_command handles empty output."""
        mock_getoutput.return_value = ''
        result = execute_command('true')
        self.assertEqual(result, '')


class TestHandleClient(unittest.TestCase):
    """Tests for the handle_client function."""
    
    def test_handle_client_exit_command(self):
        """Test that handle_client closes connection on 'exit' command."""
        mock_socket = Mock()
        mock_socket.recv.return_value = b'exit'
        
        handle_client(mock_socket)
        
        mock_socket.close.assert_called_once()
    
    def test_handle_client_empty_command(self):
        """Test that handle_client closes connection on empty command."""
        mock_socket = Mock()
        mock_socket.recv.return_value = b''
        
        handle_client(mock_socket)
        
        mock_socket.close.assert_called_once()
    
    @patch('PenetrationTesting.TCPSocket.TCPServer.execute_command')
    def test_handle_client_executes_command(self, mock_execute):
        """Test that handle_client executes commands and sends output."""
        mock_socket = Mock()
        mock_socket.recv.side_effect = [b'ls', b'exit']
        mock_execute.return_value = 'file1.txt\nfile2.txt'
        
        handle_client(mock_socket)
        
        mock_execute.assert_called_once_with('ls')
        mock_socket.send.assert_called_once_with(b'file1.txt\nfile2.txt')
    
    def test_handle_client_handles_exception(self):
        """Test that handle_client handles exceptions gracefully."""
        mock_socket = Mock()
        mock_socket.recv.side_effect = Exception("Connection error")
        
        handle_client(mock_socket)
        
        mock_socket.close.assert_called_once()


class TestCreateServerSocket(unittest.TestCase):
    """Tests for the create_server_socket function."""
    
    @patch('PenetrationTesting.TCPSocket.TCPServer.ssl.SSLContext')
    @patch('PenetrationTesting.TCPSocket.TCPServer.socket.socket')
    def test_create_server_socket_with_ssl(self, mock_socket_class, mock_ssl_context):
        """Test creating a server socket with SSL."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_context = Mock()
        mock_ssl_context.return_value = mock_context
        mock_wrapped_socket = Mock()
        mock_context.wrap_socket.return_value = mock_wrapped_socket
        
        result = create_server_socket('127.0.0.1', 8000, 'cert.pem', 'key.pem')
        
        mock_socket.setsockopt.assert_called()
        mock_socket.bind.assert_called_once_with(('127.0.0.1', 8000))
        mock_context.load_cert_chain.assert_called_once_with(certfile='cert.pem', keyfile='key.pem')
        mock_context.wrap_socket.assert_called_once_with(mock_socket, server_side=True)
        self.assertEqual(result, mock_wrapped_socket)
    
    @patch('PenetrationTesting.TCPSocket.TCPServer.socket.socket')
    def test_create_server_socket_without_ssl(self, mock_socket_class):
        """Test creating a server socket without SSL."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        
        result = create_server_socket('127.0.0.1', 8000)
        
        mock_socket.setsockopt.assert_called()
        mock_socket.bind.assert_called_once_with(('127.0.0.1', 8000))
        self.assertEqual(result, mock_socket)


if __name__ == '__main__':
    unittest.main()
