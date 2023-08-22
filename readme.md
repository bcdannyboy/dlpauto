Data Loss Prevention Testing utility 

# How to run:

- Server Mode: `sudo python3 src/dlpautomation/main.py -s --config example_server_config.yml -v`
- Client Mode: `python3 src/dlpautomation/main.py --config example_client_config.yml -v`

# DLP Testing Automation Code

- [ ] Report Generation
- [ ] YAML Based Configuration
  - [x] Infil server configuration
  - [ ] Infil confirmer configuration
  - [x] Exfil client configuration
- [x] Central Logging
- [x] NPI Generation
- [x] Data Encoding
  - [x] plaintext
  - [x] base64 encode
  - [x] base32 encode
  - [x] base16 encode
  - [x] zlib compress
  - [x] xor encode
  - [x] urlencode
  - [x] hex encode
  - [x] rot13 encode
  - [x] ascii encode
  - [x] binary encode
  - [x] caesar cipher
  - [x] reverse data
  - [x] aes encryption (16 byte key)
  - [x] fernet encryption (16 byte key)
- [x] Document Generation
  - [x] Word
  - [x] Excel
  - [x] Powerpoint
  - [x] Visio
  - [x] Outlook
    - [x] Subject
    - [x] Body
    - [x] Attachment
  - [x] CSV
  - [x] TXT
  - [x] PDF
  - [x] HTML
  - [x] XML
  - [x] JSON
  - [x] YML
  - [x] ZIP
    - [x] Password Protected
    - [x] Embedded ZIP
  - [x] Bad format file
- [ ] Exfil Methods
  - [x] Local Service
    - [x] HTTP/S Standard
      - [x] All method types
      - [x] Header
      - [x] Body
      - [x] URL Param
      - [x] URL Query Value
      - [x] Cookies
    - [x] HTTP/S Advanced
      - [x] GraphQL
      - [x] gRPC
      - [x] WebSockets
    - [x] DNS
    - [x] Email
      - [x] subject
      - [x] Body
      - [x] Attachment
    - [x] S/FTP
    - [x] TCP
    - [x] UDP
    - [x] ICMP
    - [x] RPC
    - [x] SSH
  - [ ] External Service
    - [ ] OneDrive
    - [ ] Sharepoint
    - [ ] Chat Applications
    - [x] AWS
    - [x] Github
- [x] Infil Servers
  - [x] HTTP/S Server
  - [x] HTTP/S Advanced
    - [x] GraphQL
    - [x] WebSocket
    - [x] gRPC
  - [x] DNS
  - [x] TCP
  - [x] UDP
  - [x] ICMP
- [ ] Infil Confirmers
  - [ ] Github Confirmation
  - [ ] Onedrive Confirmation
  - [ ] Sharepoint Confirmation
  - [ ] Chat Application Confirmation

## Notes:

- SSH, RPC, FTP, and AWS S3 exfil confirmation is based on files existing
  - ssh file names will all start with dlpd_ssh
  - rpc file names will all start with dlpd_rpc
  - ftp file names will all start with dlpd_ftp
  - s3 file names will all start with dlpd_aws
- Email exfil confirmation is based on emails received