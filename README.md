# Inspectinator
_Scams_ and _Phishing_ attacks are common these days. <br/>
Inspectinator inspects URLs and Domains for scams. <br/>

The site is analyzed based on the following aspects or parameters: <br/>
    - are too many **hyphens** in the domain <br/>
    - *google analysis* <br/>
    - *whois* data check <br/>
    - *tld* check <br/>

### __Home page__ <br/>
![alt text](demo/home2.png)

### __Result page__ <br/>
![alt text](demo/result.png)

[__Demo video__ <br/>](https://github.com/teleport-1254/Inspectinator/blob/main/demo/vid.mp4)

---
## Requirements: <br/>
- Python 3.9 <br/>
- MySQL 8.0 <br/>
---

## Setup: <br/>
Install all required python libraries by <br/>
`pip install -r requirements.txt` <br/>
Run MySQL queries in `table-query.txt` <br/>
Change `mysql.connector` configs in `isscam.py` <br/>
Run `app.py` <br/>
Open browser and navigate to `http:127.0.0.1:5000/`
