# Script for getting tx information of a ONE address from archival nodes and saving to csv.

Change address and run the script. It will create a `data` folder and save a raw JSON response and a CSV with timestamps and amount parsed to reflect datetime and One amount.

# Install requirements

Install Python 3.7+

https://python.org

```
sudo apt install python3-pip
pip3 install -r requirements.txt
```

# run program

1. Change the `address` to your one address.
2. Change the `pages` to the desired amount. (working backwards from the current block)
3.  run `python3 get_tx_info_by_address.py`
4.  check data folder for results.
5.  Data logged in logs folder


Requests can be added to the issues tab.
# Find this useful?

Donate: one1xlu2vumced5sm5qtmxx27sekec8hcdc3maffaz
