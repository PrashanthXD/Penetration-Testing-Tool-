#!/usr/bin/env python3
"""Unit tests for Nmap scanner module."""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Mock the nmap module before importing scanner module
nmap_mock = MagicMock()
sys.modules['nmap'] = nmap_mock

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PenetrationTesting.Nmap.scanner import (
    create_scanner,
    get_nmap_version,
    syn_ack_scan,
    udp_scan,
    comprehensive_scan,
    validate_scan_option
)


class TestCreateScanner(unittest.TestCase):
    """Tests for the create_scanner function."""
    
    @patch('PenetrationTesting.Nmap.scanner.nmap.PortScanner')
    def test_create_scanner(self, mock_port_scanner):
        """Test creating a scanner instance."""
        mock_instance = Mock()
        mock_port_scanner.return_value = mock_instance
        
        result = create_scanner()
        
        mock_port_scanner.assert_called_once()
        self.assertEqual(result, mock_instance)


class TestGetNmapVersion(unittest.TestCase):
    """Tests for the get_nmap_version function."""
    
    def test_get_nmap_version(self):
        """Test getting nmap version."""
        mock_scanner = Mock()
        mock_scanner.nmap_version.return_value = (7, 80)
        
        result = get_nmap_version(mock_scanner)
        
        mock_scanner.nmap_version.assert_called_once()
        self.assertEqual(result, (7, 80))


class TestSynAckScan(unittest.TestCase):
    """Tests for the syn_ack_scan function."""
    
    def test_syn_ack_scan_success(self):
        """Test successful SYN ACK scan."""
        mock_scanner = Mock()
        mock_scanner.scaninfo.return_value = {'tcp': {'method': 'syn'}}
        mock_scanner.__getitem__ = Mock()
        mock_ip_result = Mock()
        mock_ip_result.state.return_value = 'up'
        mock_ip_result.all_protocols.return_value = ['tcp']
        mock_ip_result.__getitem__ = Mock(return_value={22: {'state': 'open'}, 80: {'state': 'open'}})
        mock_scanner.__getitem__.return_value = mock_ip_result
        
        result = syn_ack_scan(mock_scanner, '192.168.1.1')
        
        mock_scanner.scan.assert_called_once_with('192.168.1.1', '1-1024', '-v -sS')
        self.assertEqual(result['state'], 'up')
        self.assertEqual(result['protocols'], ['tcp'])
    
    def test_syn_ack_scan_custom_port_range(self):
        """Test SYN ACK scan with custom port range."""
        mock_scanner = Mock()
        mock_scanner.scaninfo.return_value = {}
        mock_ip_result = Mock()
        mock_ip_result.state.return_value = 'up'
        mock_ip_result.all_protocols.return_value = ['tcp']
        mock_ip_result.__getitem__ = Mock(return_value={})
        mock_scanner.__getitem__ = Mock(return_value=mock_ip_result)
        
        result = syn_ack_scan(mock_scanner, '192.168.1.1', port_range='1-65535')
        
        mock_scanner.scan.assert_called_once_with('192.168.1.1', '1-65535', '-v -sS')
    
    def test_syn_ack_scan_no_open_ports(self):
        """Test SYN ACK scan with no open ports."""
        mock_scanner = Mock()
        mock_scanner.scaninfo.return_value = {}
        mock_ip_result = Mock()
        mock_ip_result.state.return_value = 'up'
        mock_ip_result.all_protocols.return_value = []  # No protocols found
        mock_scanner.__getitem__ = Mock(return_value=mock_ip_result)
        
        result = syn_ack_scan(mock_scanner, '192.168.1.1')
        
        self.assertEqual(result['open_ports'], [])


class TestUdpScan(unittest.TestCase):
    """Tests for the udp_scan function."""
    
    def test_udp_scan_success(self):
        """Test successful UDP scan."""
        mock_scanner = Mock()
        mock_scanner.scaninfo.return_value = {'udp': {'method': 'udp'}}
        mock_ip_result = Mock()
        mock_ip_result.state.return_value = 'up'
        mock_ip_result.all_protocols.return_value = ['udp']
        mock_ip_result.__getitem__ = Mock(return_value={53: {'state': 'open'}, 123: {'state': 'open'}})
        mock_scanner.__getitem__ = Mock(return_value=mock_ip_result)
        
        result = udp_scan(mock_scanner, '192.168.1.1')
        
        mock_scanner.scan.assert_called_once_with('192.168.1.1', '1-1024', '-v -sU')
        self.assertEqual(result['state'], 'up')
        self.assertEqual(result['protocols'], ['udp'])
    
    def test_udp_scan_no_open_ports(self):
        """Test UDP scan with no open ports."""
        mock_scanner = Mock()
        mock_scanner.scaninfo.return_value = {}
        mock_ip_result = Mock()
        mock_ip_result.state.return_value = 'up'
        mock_ip_result.all_protocols.return_value = []
        mock_scanner.__getitem__ = Mock(return_value=mock_ip_result)
        
        result = udp_scan(mock_scanner, '192.168.1.1')
        
        self.assertEqual(result['open_ports'], [])


class TestComprehensiveScan(unittest.TestCase):
    """Tests for the comprehensive_scan function."""
    
    def test_comprehensive_scan_success(self):
        """Test successful comprehensive scan."""
        mock_scanner = Mock()
        mock_scanner.scaninfo.return_value = {'tcp': {'method': 'syn'}}
        mock_ip_result = Mock()
        mock_ip_result.state.return_value = 'up'
        mock_ip_result.all_protocols.return_value = ['tcp']
        mock_ip_result.__getitem__ = Mock(return_value={22: {'state': 'open'}, 80: {'state': 'open'}})
        mock_scanner.__getitem__ = Mock(return_value=mock_ip_result)
        
        result = comprehensive_scan(mock_scanner, '192.168.1.1')
        
        mock_scanner.scan.assert_called_once_with('192.168.1.1', '1-1024', '-v -sS -sV -A -O')
        self.assertEqual(result['state'], 'up')
    
    def test_comprehensive_scan_custom_port_range(self):
        """Test comprehensive scan with custom port range."""
        mock_scanner = Mock()
        mock_scanner.scaninfo.return_value = {}
        mock_ip_result = Mock()
        mock_ip_result.state.return_value = 'up'
        mock_ip_result.all_protocols.return_value = ['tcp']
        mock_ip_result.__getitem__ = Mock(return_value={})
        mock_scanner.__getitem__ = Mock(return_value=mock_ip_result)
        
        result = comprehensive_scan(mock_scanner, '192.168.1.1', port_range='80-443')
        
        mock_scanner.scan.assert_called_once_with('192.168.1.1', '80-443', '-v -sS -sV -A -O')


class TestValidateScanOption(unittest.TestCase):
    """Tests for the validate_scan_option function."""
    
    def test_validate_option_1(self):
        """Test validation of option 1."""
        self.assertTrue(validate_scan_option('1'))
    
    def test_validate_option_2(self):
        """Test validation of option 2."""
        self.assertTrue(validate_scan_option('2'))
    
    def test_validate_option_3(self):
        """Test validation of option 3."""
        self.assertTrue(validate_scan_option('3'))
    
    def test_validate_invalid_option(self):
        """Test validation of invalid option."""
        self.assertFalse(validate_scan_option('4'))
        self.assertFalse(validate_scan_option('0'))
        self.assertFalse(validate_scan_option(''))
        self.assertFalse(validate_scan_option('invalid'))


class TestScannerEdgeCases(unittest.TestCase):
    """Edge case tests for the scanner module."""
    
    def test_scan_with_various_ip_formats(self):
        """Test scanning with various IP address formats."""
        mock_scanner = Mock()
        mock_scanner.scaninfo.return_value = {}
        mock_ip_result = Mock()
        mock_ip_result.state.return_value = 'up'
        mock_ip_result.all_protocols.return_value = []
        mock_scanner.__getitem__ = Mock(return_value=mock_ip_result)
        
        # Test with different IP formats
        ip_addresses = ['192.168.1.1', '10.0.0.1', '127.0.0.1']
        for ip in ip_addresses:
            result = syn_ack_scan(mock_scanner, ip)
            self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
