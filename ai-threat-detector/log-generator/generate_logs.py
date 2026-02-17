import time
import random
import logging
import socket
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

def generate_log_entry():
    """
    Generates a fake log entry.
    """
    actions = ["LOGIN", "LOGOUT", "FILE_ACCESS", "DATA_TRANSFER"]
    users = ["admin", "user1", "user2", "guest"]
    statuses = ["SUCCESS", "FAILURE", "ERROR"]
    
    log_entry = {
        "timestamp": time.time(),
        "ip_address": f"192.168.1.{random.randint(1, 255)}",
        "user_id": random.choice(users),
        "action": random.choice(actions),
        "status": random.choice(statuses),
        "bytes_sent": random.randint(100, 5000)
    }
    
    # Simulate an anomaly occasionally
    if random.random() < 0.05:
        log_entry["action"] = "SUDO_ACCESS"
        log_entry["status"] = "FAILURE"
        log_entry["bytes_sent"] = random.randint(10000, 50000)
        
    return log_entry

def send_logs():
    """
    Sends logs to Logstash via TCP.
    """
    host = 'logstash'
    port = 5000
    
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            
            while True:
                log_en = generate_log_entry()
                message = json.dumps(log_en) + "\n"
                sock.sendall(message.encode('utf-8'))
                time.sleep(1) # Send 1 log per second
                
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    send_logs()
