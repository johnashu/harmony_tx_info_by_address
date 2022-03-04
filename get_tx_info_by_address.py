from requests import post
from json import dump
from datetime import datetime
import logging, os, sys, csv
from collections import namedtuple
from web3 import Web3


address = "one1xlu2vumced5sm5qtmxx27sekec8hcdc3maffaz"
pages = 10
harmony_api = "https://a.api.s0.t.hmny.io"  # Archive node


def create_data_path(pth: str, data_path: str = "data") -> os.path:
    cwd = os.getcwd()
    p = os.path.join(cwd, data_path, pth)
    if not os.path.exists(p):
        os.mkdir(p)
    return p


def yield_data(address: str, num_pages: int = 10) -> list:
    i = 0
    result = []
    while 1:
        params = [
            {
                "address": address,
                "pageIndex": i,
                "fullTx": True,
                "txType": "ALL",
                "order": "DESC",
            }
        ]
        result, data = rpc_v2(result, "hmyv2_getTransactionsHistory", params)
        if not data or i == num_pages:
            log.info(f"NO MORE DATA.. ENDING ON PAGE {i}.")
            break
        i += 1

    with open(os.path.join("data", "tx_data.json"), "w") as j:
        dump(result, j, indent=4)
    return result


def rpc_v2(
    result: list,
    method: str,
    params: list,
) -> dict:

    d = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    try:
        r = post(harmony_api, json=d)
        data = r.json()["result"]
    except KeyError:
        log.error(r)
        data = r.json()
    result += data["transactions"]
    return result, data


def save_csv(fn: str, data: list) -> None:
    if not data:
        log.info("No Data Found..")
        return
    data = convert_unix_time_and_one(data)
    header = data[0].keys()
    with open(os.path.join("data", fn), "w", newline="", encoding="utf-8") as csvfile:
        w = csv.DictWriter(csvfile, fieldnames=header, delimiter=",")
        w.writeheader()
        for x in data:
            w.writerow(x)


def convert_unix_time_and_one(data: list) -> list:
    fmt = "%Y-%m-%d %H:%M:%S"
    rtn = []
    for x in data:
        new_d = x
        new_d.update(
            {
                "timestamp": datetime.fromtimestamp(x["timestamp"]).strftime(fmt),
                "value": Web3.fromWei(x["value"], "ether"),
            }
        )
        rtn.append(new_d)
    return rtn


if __name__ == "__main__":
    create_data_path((""))
    create_data_path(("logs"), "")

    file_handler = logging.FileHandler(filename=os.path.join("logs", "tx_data.log"))
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=handlers)

    log = logging.getLogger()

    data = yield_data(address, num_pages=pages)
    save_csv("Tx_Date.csv", data)
