#!/usr/bin/env python3
"""Unit tests for BannerGrabber module."""

import unittest
import socket
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PenetrationTesting.BannerGrabber.bannergrabber import grab_banner, banner


class TestGrabBanner(unittest.TestCase):
    """Tests for the grab_banner function."""
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.socket.socket')
    def test_grab_banner_success(self, mock_socket_class):
        """Test successful banner grabbing."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.recv.return_value = b'SSH-2.0-OpenSSH_7.9\r\n'
        
        result = grab_banner('192.168.1.1', 22)
        
        mock_socket.settimeout.assert_called_once_with(5)
        mock_socket.connect.assert_called_once_with(('192.168.1.1', 22))
        mock_socket.recv.assert_called_once_with(1024)
        mock_socket.close.assert_called_once()
        self.assertIn('SSH-2.0-OpenSSH_7.9', result)
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.socket.socket')
    def test_grab_banner_with_string_port(self, mock_socket_class):
        """Test banner grabbing with port as string."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.recv.return_value = b'220 FTP Server ready'
        
        result = grab_banner('192.168.1.1', '21')
        
        mock_socket.connect.assert_called_once_with(('192.168.1.1', 21))
        self.assertIn('FTP Server ready', result)
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.socket.socket')
    def test_grab_banner_custom_timeout(self, mock_socket_class):
        """Test banner grabbing with custom timeout."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.recv.return_value = b'Banner'
        
        grab_banner('192.168.1.1', 80, timeout=10)
        
        mock_socket.settimeout.assert_called_once_with(10)
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.socket.socket')
    def test_grab_banner_connection_refused(self, mock_socket_class):
        """Test banner grabbing when connection is refused."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.connect.side_effect = socket.error("Connection refused")
        
        with self.assertRaises(socket.error):
            grab_banner('192.168.1.1', 12345)
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.socket.socket')
    def test_grab_banner_timeout(self, mock_socket_class):
        """Test banner grabbing when connection times out."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.connect.side_effect = socket.timeout("Connection timed out")
        
        with self.assertRaises(socket.timeout):
            grab_banner('192.168.1.1', 22)


class TestBannerFunction(unittest.TestCase):
    """Tests for the legacy banner function."""
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.grab_banner')
    @patch('builtins.print')
    def test_banner_prints_result(self, mock_print, mock_grab_banner):
        """Test that banner function prints the grabbed banner."""
        mock_grab_banner.return_value = 'SSH-2.0-OpenSSH'
        
        banner('192.168.1.1', 22)
        
        mock_grab_banner.assert_called_once_with('192.168.1.1', 22)
        mock_print.assert_called_once_with('SSH-2.0-OpenSSH')


class TestBannerGrabberEdgeCases(unittest.TestCase):
    """Edge case tests for BannerGrabber."""
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.socket.socket')
    def test_grab_banner_empty_response(self, mock_socket_class):
        """Test handling of empty banner response."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.recv.return_value = b''
        
        result = grab_banner('192.168.1.1', 80)
        
        # str(b'') returns "b''" which stripped becomes "''"
        self.assertEqual(result, "''")
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.socket.socket')
    def test_grab_banner_with_special_characters(self, mock_socket_class):
        """Test handling of banners with special characters."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.recv.return_value = b'Apache/2.4.41 (Ubuntu)\r\n'
        
        result = grab_banner('192.168.1.1', 80)
        
        self.assertIn('Apache', result)
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.socket.socket')
    def test_grab_banner_ipv4_address(self, mock_socket_class):
        """Test with valid IPv4 address."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.recv.return_value = b'test'
        
        grab_banner('10.0.0.1', 80)
        
        mock_socket.connect.assert_called_once_with(('10.0.0.1', 80))


class TestInputValidation(unittest.TestCase):
    """Tests for input validation."""
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.socket.socket')
    def test_grab_banner_port_as_int(self, mock_socket_class):
        """Test that port can be passed as integer."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.recv.return_value = b'test'
        
        grab_banner('127.0.0.1', 80)
        
        mock_socket.connect.assert_called_with(('127.0.0.1', 80))
    
    @patch('PenetrationTesting.BannerGrabber.bannergrabber.socket.socket')
    def test_grab_banner_port_as_string(self, mock_socket_class):
        """Test that port can be passed as string."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.recv.return_value = b'test'
        
        grab_banner('127.0.0.1', '443')
        
        mock_socket.connect.assert_called_with(('127.0.0.1', 443))


if __name__ == '__main__':
    unittest.main()
