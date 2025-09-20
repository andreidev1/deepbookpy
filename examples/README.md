## Run examples

Clone the repo using 

`git clone https://github.com/andreidev1/deepbookpy`

Change directory to cloned repo

`cd deepbookpy`

Create a virtual environment (optional)

`python3 -m venv env && source ./env/bin/activate`

Install dep requirements

`pip install -r example-requirements.txt`

Run an example

`python3 examples/balance.py`


## Note

Examples directory use environment variables.

To be able to run examples create a `.env` file at the root directory of the repo and add your SUI private key.

`PRIVATE_KEY=....`

