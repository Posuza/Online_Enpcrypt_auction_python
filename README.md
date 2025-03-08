# Online Auction System

A client-server based auction system that enables users to participate in real-time auctions with secure communication and user management.

## Features

### User Management
- User registration and authentication
- Role-based access control (Admin and Regular users)
- Profile management
- Secure account management

### Auction Features
- Real-time bidding system
- Create and manage auction items
- View active auctions
- Automatic time-based auction closure
- Bid history tracking

### Admin Capabilities
- User management (CRUD operations)
- Item management
- System monitoring
- User role management

### Security Features
- Encrypted communication
- Secure authentication
- Session management
- Protected data transmission

## Prerequisites

Before running the application, ensure you have:
- Python 3.x installed
- Same network configuration for client and server
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository
  ```bash
  git@github.com:Posuza/python_auction_project.git
  cd auction-system
  ```
  - Or 
    - download the Zip File


2.Configure the system
  -Verify IP addresses for client and server are on the same network
  -Set up initial admin user:
    . Register first user
    . Close both server and client
    . Update user role to "admin" in the database
    . Restart the system
3.Start the server
  ```bash
    python server.py
    python client7.py
  ```
### For Users
  -Register a new account or login with existing credentials
  -Browse active auctions
  -Create new auction items
  -Place bids on active items
  -Monitor your active bids and items
  
### For Administrators
  -Access admin panel through login
  -Manage user accounts
  -Monitor system activity
  -Control auction items
  -Configure system settings
  
### Important Notes
  -Always ensure proper logout before closing the application
  -Check user status if experiencing login issues
  -Admin users must be configured manually in the initial setup
  -Keep the server and client on the same network for proper communication
  
### System Architecture
  -Client-Server architecture
  -Multi-threaded communication
  --Real-time bidding system
  Encrypted data transmission
  -Database persistence
### Security Considerations
  -All communications are encrypted
  -Secure password handling
  -Protected user sessions
  -Role-based access control
  -Input validation
  
### Contributing
  -We welcome contributions to the Online Auction System! Here's how you can help:
###Fork the Repository
 ```bash
    git clone git@github.com:Posuza/python_auction_project.git
  ```
###Create a Branch
  ```bash
    git checkout -b feature/example
  ```
###Commit Changes
  ```bash
    git commit -m 'Add some AmazingFeature'
  ```
###Push to Branch
  ```bash
    git push origin feature/AmazingFeature
  ```
##Open a Pull Request
  -License
  -This project is licensed under the MIT License - see the LICENSE file for details.

##Contact
   -posu0009@gmail.com

##Acknowledgments
  -Thanks to all contributors who have helped shape this project
  -Special thanks to the Python community for excellent libraries and tools

  
