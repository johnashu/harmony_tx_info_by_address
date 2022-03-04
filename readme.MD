# Script for getting information from archival nodes and saving to csv.

Change address and run the script. It will create a `data` folder and save a raw JSON response and a CSV with timestamps and amount parsed to reflect datetime and One amount.

# Install requirements

```
sudo apt install python3-pip
pip3 install -r requirements.txt
```

# run program

1. Change the address in `get_tx_info_by_address.py` to your one address.
2.  run `python3 get_tx_info_by_address.py`
3.  check data folder for  results.


