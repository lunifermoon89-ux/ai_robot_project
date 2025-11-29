"""Small Python client example that calls the `/predict` API.

Usage:
    python scripts/client_predict.py 400
"""
import sys
import requests

def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/client_predict.py <X_Feature>')
        sys.exit(1)

    value = float(sys.argv[1])
    url = 'http://localhost:8080/predict'
    resp = requests.post(url, json={'X_Feature': value})
    print('Status:', resp.status_code)
    print('Response:', resp.text)

if __name__ == '__main__':
    main()
