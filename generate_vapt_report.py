#!/usr/bin/env python3
"""
VAPT Report Generator for Penetration-Testing-Tool- Repository
Generates a professional Vulnerability Assessment and Penetration Testing report in DOCX format.
"""

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import os


def create_vapt_report():
    """Create a comprehensive VAPT report document."""
    doc = Document()
    
    # Set document title
    title = doc.add_heading('Vulnerability Assessment and Penetration Testing (VAPT) Report', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add subtitle with repository info
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('Repository: PrashanthXD/Penetration-Testing-Tool-')
    run.bold = True
    run.font.size = Pt(14)
    
    # Add date
    date_para = doc.add_paragraph()
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    date_para.add_run(f'Report Generated: {datetime.now().strftime("%B %d, %Y")}')
    
    doc.add_paragraph()
    
    # =====================================================
    # Section 1: Project Overview
    # =====================================================
    doc.add_heading('1. Project Overview', level=1)
    
    doc.add_paragraph(
        'This Vulnerability Assessment and Penetration Testing (VAPT) report provides a comprehensive '
        'security analysis of the Penetration-Testing-Tool- repository. The assessment covers source code '
        'review, security vulnerability identification, and recommendations for remediation.'
    )
    
    # Project Details Table
    doc.add_heading('1.1 Project Details', level=2)
    table = doc.add_table(rows=5, cols=2)
    table.style = 'Table Grid'
    
    details = [
        ('Repository Name', 'Penetration-Testing-Tool-'),
        ('Repository Owner', 'PrashanthXD'),
        ('Primary Language', 'Python'),
        ('Latest Observed Activity', 'Commit updates on core files (TCPClient.py and TCPServer.py)'),
        ('Assessment Date', datetime.now().strftime('%B %d, %Y'))
    ]
    
    for i, (key, value) in enumerate(details):
        row = table.rows[i]
        row.cells[0].text = key
        row.cells[1].text = value
        row.cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    
    # Repository Components
    doc.add_heading('1.2 Repository Components', level=2)
    components = [
        'TCPSocket/ - TCP client-server implementation with SSL/TLS support',
        'BannerGrabber/ - Network service banner grabbing utility',
        'Nmap/ - Network scanning wrapper using python-nmap',
        'PortScanner/ - Basic port scanning utility'
    ]
    for comp in components:
        doc.add_paragraph(comp, style='List Bullet')
    
    doc.add_paragraph()
    
    # =====================================================
    # Section 2: Scope of Testing
    # =====================================================
    doc.add_heading('2. Scope of Testing', level=1)
    
    doc.add_paragraph(
        'The security assessment was conducted with the following scope and objectives:'
    )
    
    doc.add_heading('2.1 Assessment Areas', level=2)
    scope_areas = [
        'Source Code Review: Analysis of all Python scripts for security vulnerabilities',
        'Commit History Analysis: Review of recent commit updates to core files',
        'Input Validation: Assessment of user input handling and sanitization',
        'Dependency Inspection: Review of external libraries and potential vulnerabilities',
        'Configuration Review: Analysis of SSL/TLS configuration and certificate handling',
        'Credential Management: Assessment of secrets and key handling practices'
    ]
    for area in scope_areas:
        doc.add_paragraph(area, style='List Bullet')
    
    doc.add_heading('2.2 Testing Methodology', level=2)
    doc.add_paragraph(
        'The assessment followed industry-standard methodologies including OWASP Testing Guide, '
        'SANS Top 25, and manual code review techniques. Static code analysis was performed '
        'to identify potential security weaknesses.'
    )
    
    doc.add_paragraph()
    
    # =====================================================
    # Section 3: Vulnerability Findings and Analysis
    # =====================================================
    doc.add_heading('3. Vulnerability Findings and Analysis', level=1)
    
    doc.add_paragraph(
        'The following security vulnerabilities and risks were identified during the assessment:'
    )
    
    # Vulnerability 1: Command Injection
    doc.add_heading('3.1 Critical: Command Injection Vulnerability', level=2)
    
    vuln_table1 = doc.add_table(rows=5, cols=2)
    vuln_table1.style = 'Table Grid'
    vuln1_data = [
        ('Severity', 'CRITICAL'),
        ('Location', 'PenetrationTesting/TCPSocket/TCPServer.py (Line 21)'),
        ('CWE Reference', 'CWE-78: Improper Neutralization of Special Elements used in an OS Command'),
        ('CVSS Score', '9.8 (Critical)'),
        ('Status', 'Open - Requires Immediate Remediation')
    ]
    for i, (key, value) in enumerate(vuln1_data):
        row = vuln_table1.rows[i]
        row.cells[0].text = key
        row.cells[1].text = value
        row.cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    doc.add_paragraph('Description:', style='Intense Quote')
    doc.add_paragraph(
        'The TCPServer.py file uses subprocess.getoutput() to execute arbitrary commands received '
        'from client connections without any input validation or sanitization. This allows remote '
        'attackers to execute arbitrary system commands with the privileges of the server process.'
    )
    
    doc.add_paragraph('Vulnerable Code:')
    code_para = doc.add_paragraph()
    code_run = code_para.add_run('output = subprocess.getoutput(command)')
    code_run.font.name = 'Courier New'
    code_run.font.size = Pt(10)
    
    doc.add_paragraph()
    
    # Vulnerability 2: SSL Certificate Verification Disabled
    doc.add_heading('3.2 High: SSL Certificate Verification Disabled', level=2)
    
    vuln_table2 = doc.add_table(rows=5, cols=2)
    vuln_table2.style = 'Table Grid'
    vuln2_data = [
        ('Severity', 'HIGH'),
        ('Location', 'PenetrationTesting/TCPSocket/TCPClient.py (Lines 9-10)'),
        ('CWE Reference', 'CWE-295: Improper Certificate Validation'),
        ('CVSS Score', '7.4 (High)'),
        ('Status', 'Open - Requires Remediation')
    ]
    for i, (key, value) in enumerate(vuln2_data):
        row = vuln_table2.rows[i]
        row.cells[0].text = key
        row.cells[1].text = value
        row.cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    doc.add_paragraph('Description:', style='Intense Quote')
    doc.add_paragraph(
        'The TCP client explicitly disables SSL certificate verification by setting '
        'check_hostname=False and verify_mode=ssl.CERT_NONE. This makes the application '
        'vulnerable to man-in-the-middle attacks, as any certificate presented by the server '
        'will be accepted without validation.'
    )
    
    doc.add_paragraph('Vulnerable Code:')
    code_para2 = doc.add_paragraph()
    code_run2 = code_para2.add_run('context.check_hostname = False\ncontext.verify_mode = ssl.CERT_NONE')
    code_run2.font.name = 'Courier New'
    code_run2.font.size = Pt(10)
    
    doc.add_paragraph()
    
    # Vulnerability 3: Private Key Exposure
    doc.add_heading('3.3 High: Private Key Committed to Repository', level=2)
    
    vuln_table3 = doc.add_table(rows=5, cols=2)
    vuln_table3.style = 'Table Grid'
    vuln3_data = [
        ('Severity', 'HIGH'),
        ('Location', 'PenetrationTesting/TCPSocket/server.key'),
        ('CWE Reference', 'CWE-312: Cleartext Storage of Sensitive Information'),
        ('CVSS Score', '7.5 (High)'),
        ('Status', 'Open - Requires Immediate Action')
    ]
    for i, (key, value) in enumerate(vuln3_data):
        row = vuln_table3.rows[i]
        row.cells[0].text = key
        row.cells[1].text = value
        row.cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    doc.add_paragraph('Description:', style='Intense Quote')
    doc.add_paragraph(
        'The SSL private key (server.key) is committed directly to the repository in plaintext. '
        'This exposes the cryptographic key to anyone with access to the repository, potentially '
        'allowing attackers to impersonate the server or decrypt intercepted communications.'
    )
    
    doc.add_paragraph()
    
    # Vulnerability 4: Hardcoded IP/Port
    doc.add_heading('3.4 Medium: Hardcoded Network Configuration', level=2)
    
    vuln_table4 = doc.add_table(rows=5, cols=2)
    vuln_table4.style = 'Table Grid'
    vuln4_data = [
        ('Severity', 'MEDIUM'),
        ('Location', 'PenetrationTesting/TCPSocket/TCPClient.py, TCPServer.py'),
        ('CWE Reference', 'CWE-798: Use of Hard-coded Credentials'),
        ('CVSS Score', '4.3 (Medium)'),
        ('Status', 'Open - Recommended Fix')
    ]
    for i, (key, value) in enumerate(vuln4_data):
        row = vuln_table4.rows[i]
        row.cells[0].text = key
        row.cells[1].text = value
        row.cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    doc.add_paragraph('Description:', style='Intense Quote')
    doc.add_paragraph(
        'IP addresses (127.0.0.1) and port numbers (8000) are hardcoded in the source files. '
        'This reduces flexibility and makes the tools less portable. Configuration should be '
        'externalized to environment variables or configuration files.'
    )
    
    doc.add_paragraph()
    
    # Vulnerability 5: No Input Validation in Scanner Scripts
    doc.add_heading('3.5 Medium: Insufficient Input Validation', level=2)
    
    vuln_table5 = doc.add_table(rows=5, cols=2)
    vuln_table5.style = 'Table Grid'
    vuln5_data = [
        ('Severity', 'MEDIUM'),
        ('Location', 'PenetrationTesting/Nmap/scanner.py, PortScanner/PortScanner.py'),
        ('CWE Reference', 'CWE-20: Improper Input Validation'),
        ('CVSS Score', '5.3 (Medium)'),
        ('Status', 'Open - Recommended Fix')
    ]
    for i, (key, value) in enumerate(vuln5_data):
        row = vuln_table5.rows[i]
        row.cells[0].text = key
        row.cells[1].text = value
        row.cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    doc.add_paragraph('Description:', style='Intense Quote')
    doc.add_paragraph(
        'User input for IP addresses and ports is accepted without proper validation. '
        'The scanner scripts do not validate IP address format or port number ranges, '
        'which could lead to unexpected behavior or security issues.'
    )
    
    doc.add_paragraph()
    
    # Vulnerability 6: Code Quality Issues
    doc.add_heading('3.6 Low: Code Quality and Error Handling Issues', level=2)
    
    vuln_table6 = doc.add_table(rows=5, cols=2)
    vuln_table6.style = 'Table Grid'
    vuln6_data = [
        ('Severity', 'LOW'),
        ('Location', 'Multiple files'),
        ('CWE Reference', 'CWE-755: Improper Handling of Exceptional Conditions'),
        ('CVSS Score', '3.1 (Low)'),
        ('Status', 'Open - Recommended Improvement')
    ]
    for i, (key, value) in enumerate(vuln6_data):
        row = vuln_table6.rows[i]
        row.cells[0].text = key
        row.cells[1].text = value
        row.cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    doc.add_paragraph('Description:', style='Intense Quote')
    doc.add_paragraph(
        'Several scripts have typos (setimeout instead of settimeout), lack proper exception '
        'handling, and missing documentation. While not directly exploitable, these issues '
        'could lead to application crashes or unexpected behavior.'
    )
    
    doc.add_paragraph()
    
    # Vulnerability Summary Table
    doc.add_heading('3.7 Vulnerability Summary', level=2)
    
    summary_table = doc.add_table(rows=7, cols=4)
    summary_table.style = 'Table Grid'
    
    headers = ['ID', 'Vulnerability', 'Severity', 'Status']
    header_row = summary_table.rows[0]
    for i, header in enumerate(headers):
        header_row.cells[i].text = header
        header_row.cells[i].paragraphs[0].runs[0].bold = True
    
    vuln_summary = [
        ('V-001', 'Command Injection', 'CRITICAL', 'Open'),
        ('V-002', 'SSL Certificate Verification Disabled', 'HIGH', 'Open'),
        ('V-003', 'Private Key Exposure', 'HIGH', 'Open'),
        ('V-004', 'Hardcoded Network Configuration', 'MEDIUM', 'Open'),
        ('V-005', 'Insufficient Input Validation', 'MEDIUM', 'Open'),
        ('V-006', 'Code Quality Issues', 'LOW', 'Open'),
    ]
    
    for i, (vid, vuln, sev, status) in enumerate(vuln_summary):
        row = summary_table.rows[i + 1]
        row.cells[0].text = vid
        row.cells[1].text = vuln
        row.cells[2].text = sev
        row.cells[3].text = status
    
    doc.add_paragraph()
    
    # =====================================================
    # Section 4: Recommendations
    # =====================================================
    doc.add_heading('4. Recommendations and Solutions', level=1)
    
    doc.add_paragraph(
        'The following recommendations are provided to address the identified vulnerabilities '
        'and improve the overall security posture of the repository:'
    )
    
    # Recommendation 1
    doc.add_heading('4.1 Command Injection Remediation (V-001)', level=2)
    doc.add_paragraph('Priority: IMMEDIATE', style='Intense Quote')
    
    para = doc.add_paragraph(); para.add_run('Recommended Actions:').bold = True
    rec1_actions = [
        'Implement a whitelist of allowed commands instead of executing arbitrary input',
        'Use subprocess.run() with shell=False and provide arguments as a list',
        'Sanitize and validate all user input before processing',
        'Consider removing remote command execution functionality entirely'
    ]
    for action in rec1_actions:
        doc.add_paragraph(action, style='List Bullet')
    
    doc.add_paragraph('Secure Code Example:')
    secure_code1 = '''# Whitelist approach for safe commands
ALLOWED_COMMANDS = {'ls', 'pwd', 'whoami', 'date'}

def handle_command(command):
    if command not in ALLOWED_COMMANDS:
        return "Command not allowed"
    result = subprocess.run([command], capture_output=True, text=True, shell=False)
    return result.stdout'''
    
    code_para = doc.add_paragraph()
    code_run = code_para.add_run(secure_code1)
    code_run.font.name = 'Courier New'
    code_run.font.size = Pt(9)
    
    doc.add_paragraph()
    
    # Recommendation 2
    doc.add_heading('4.2 SSL/TLS Security Enhancement (V-002)', level=2)
    doc.add_paragraph('Priority: HIGH', style='Intense Quote')
    
    para = doc.add_paragraph(); para.add_run('Recommended Actions:').bold = True
    rec2_actions = [
        'Enable certificate verification in production environments',
        'Use proper certificate authority (CA) signed certificates',
        'Implement certificate pinning for additional security',
        'Use TLS 1.2 or higher with strong cipher suites'
    ]
    for action in rec2_actions:
        doc.add_paragraph(action, style='List Bullet')
    
    doc.add_paragraph('Secure Code Example:')
    secure_code2 = '''# Proper SSL context configuration
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations('ca_certificate.pem')'''
    
    code_para2 = doc.add_paragraph()
    code_run2 = code_para2.add_run(secure_code2)
    code_run2.font.name = 'Courier New'
    code_run2.font.size = Pt(9)
    
    doc.add_paragraph()
    
    # Recommendation 3
    doc.add_heading('4.3 Secrets Management (V-003)', level=2)
    doc.add_paragraph('Priority: HIGH', style='Intense Quote')
    
    para = doc.add_paragraph(); para.add_run('Recommended Actions:').bold = True
    rec3_actions = [
        'Remove private keys from version control immediately',
        'Add *.key and *.pem to .gitignore',
        'Regenerate compromised certificates and keys',
        'Use environment variables or secure vault solutions for secrets',
        'Consider using GitHub Secrets for CI/CD workflows'
    ]
    for action in rec3_actions:
        doc.add_paragraph(action, style='List Bullet')
    
    doc.add_paragraph()
    
    # Recommendation 4
    doc.add_heading('4.4 Configuration Externalization (V-004)', level=2)
    doc.add_paragraph('Priority: MEDIUM', style='Intense Quote')
    
    para = doc.add_paragraph(); para.add_run('Recommended Actions:').bold = True
    rec4_actions = [
        'Use environment variables for IP addresses and ports',
        'Implement a configuration file (config.ini, .env, or YAML)',
        'Provide command-line arguments for runtime configuration',
        'Document all configuration options'
    ]
    for action in rec4_actions:
        doc.add_paragraph(action, style='List Bullet')
    
    doc.add_paragraph('Example Implementation:')
    config_example = '''import os
import argparse

# Environment variable approach
HOST = os.getenv('SERVER_HOST', '127.0.0.1')
PORT = int(os.getenv('SERVER_PORT', '8000'))

# Command-line argument approach
parser = argparse.ArgumentParser()
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', type=int, default=8000)'''
    
    code_para3 = doc.add_paragraph()
    code_run3 = code_para3.add_run(config_example)
    code_run3.font.name = 'Courier New'
    code_run3.font.size = Pt(9)
    
    doc.add_paragraph()
    
    # Recommendation 5
    doc.add_heading('4.5 Input Validation Implementation (V-005)', level=2)
    doc.add_paragraph('Priority: MEDIUM', style='Intense Quote')
    
    para = doc.add_paragraph(); para.add_run('Recommended Actions:').bold = True
    rec5_actions = [
        'Validate IP address format using ipaddress module',
        'Validate port numbers are within valid range (1-65535)',
        'Implement proper error handling for invalid inputs',
        'Add type hints and input documentation'
    ]
    for action in rec5_actions:
        doc.add_paragraph(action, style='List Bullet')
    
    doc.add_paragraph('Example Validation Code:')
    validation_example = '''import ipaddress

def validate_ip(ip_string):
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False

def validate_port(port):
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False'''
    
    code_para4 = doc.add_paragraph()
    code_run4 = code_para4.add_run(validation_example)
    code_run4.font.name = 'Courier New'
    code_run4.font.size = Pt(9)
    
    doc.add_paragraph()
    
    # Recommendation 6
    doc.add_heading('4.6 Code Quality Improvements (V-006)', level=2)
    doc.add_paragraph('Priority: LOW', style='Intense Quote')
    
    para = doc.add_paragraph(); para.add_run('Recommended Actions:').bold = True
    rec6_actions = [
        'Fix typo: setimeout should be settimeout',
        'Add comprehensive error handling with try-except blocks',
        'Add logging for debugging and auditing purposes',
        'Write unit tests for core functionality',
        'Add docstrings and code comments'
    ]
    for action in rec6_actions:
        doc.add_paragraph(action, style='List Bullet')
    
    doc.add_paragraph()
    
    # README Guidance
    doc.add_heading('4.7 README and Documentation Enhancement', level=2)
    
    doc.add_paragraph(
        'A comprehensive README.md should be created to provide proper documentation for the repository:'
    )
    
    readme_items = [
        'Project description and purpose',
        'Installation instructions and prerequisites',
        'Usage examples for each tool',
        'Security considerations and warnings',
        'Configuration options documentation',
        'Contribution guidelines',
        'License information',
        'Disclaimer for educational/authorized use only'
    ]
    for item in readme_items:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_paragraph()
    
    # =====================================================
    # Section 5: Conclusion
    # =====================================================
    doc.add_heading('5. Conclusion', level=1)
    
    doc.add_paragraph(
        'This VAPT assessment has identified several security vulnerabilities in the '
        'Penetration-Testing-Tool- repository, ranging from Critical to Low severity. '
        'The most critical finding is the command injection vulnerability in TCPServer.py, '
        'which could allow remote code execution.'
    )
    
    doc.add_paragraph(
        'It is strongly recommended to address the Critical and High severity findings '
        'immediately before using these tools in any environment. The tools should only '
        'be used for authorized security testing and educational purposes.'
    )
    
    # Risk Rating Summary
    doc.add_heading('5.1 Overall Risk Rating', level=2)
    
    risk_table = doc.add_table(rows=2, cols=4)
    risk_table.style = 'Table Grid'
    
    risk_headers = ['Critical', 'High', 'Medium', 'Low']
    risk_counts = ['1', '2', '2', '1']
    
    for i, header in enumerate(risk_headers):
        risk_table.rows[0].cells[i].text = header
        risk_table.rows[0].cells[i].paragraphs[0].runs[0].bold = True
        risk_table.rows[1].cells[i].text = risk_counts[i]
    
    doc.add_paragraph()
    doc.add_paragraph(
        'Overall Risk Assessment: HIGH - Immediate remediation required for critical vulnerabilities.'
    )
    
    doc.add_paragraph()
    
    # =====================================================
    # Section 6: Appendix
    # =====================================================
    doc.add_heading('6. Appendix', level=1)
    
    doc.add_heading('6.1 Files Analyzed', level=2)
    files_analyzed = [
        'PenetrationTesting/TCPSocket/TCPClient.py',
        'PenetrationTesting/TCPSocket/TCPServer.py',
        'PenetrationTesting/TCPSocket/server.crt',
        'PenetrationTesting/TCPSocket/server.key',
        'PenetrationTesting/BannerGrabber/bannergrabber.py',
        'PenetrationTesting/Nmap/scanner.py',
        'PenetrationTesting/PortScanner/PortScanner.py'
    ]
    for f in files_analyzed:
        doc.add_paragraph(f, style='List Bullet')
    
    doc.add_heading('6.2 References', level=2)
    references = [
        'OWASP Testing Guide v4.2 - https://owasp.org/www-project-web-security-testing-guide/',
        'CWE (Common Weakness Enumeration) - https://cwe.mitre.org/',
        'SANS Top 25 Software Errors - https://www.sans.org/top25-software-errors/',
        'Python Security Best Practices - https://python.org/dev/security/'
    ]
    for ref in references:
        doc.add_paragraph(ref, style='List Bullet')
    
    doc.add_heading('6.3 Disclaimer', level=2)
    doc.add_paragraph(
        'This report is provided for informational and educational purposes only. '
        'The tools analyzed in this repository should only be used for authorized '
        'security testing with proper permission. Unauthorized use of penetration '
        'testing tools may violate applicable laws and regulations. The authors of '
        'this report are not responsible for any misuse of the information provided.'
    )
    
    # Save the document
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'VAPT_Report_Penetration_Testing_Tool.docx'
    )
    doc.save(output_path)
    print(f"VAPT Report generated successfully: {output_path}")
    return output_path


if __name__ == '__main__':
    create_vapt_report()
