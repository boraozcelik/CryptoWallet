from web3 import Web3
from bitcoinlib.wallets import Wallet

def create_ethereum_wallet():
    # Ethereum cüzdanı oluşturma
    w3 = Web3()
    account = w3.eth.account.create()
    private_key = account.privateKey.hex()
    address = account.address
    return private_key, address

def create_bitcoin_wallet():
    # Bitcoin cüzdanı oluşturma
    wallet = Wallet.create()
    private_key = wallet.privkey
    address = wallet.address
    return private_key, address

def send_ethereum_transaction(sender_private_key, sender_address, recipient_address, amount):
    # Ethereum işlemi gönderme
    w3 = Web3()
    sender_account = w3.eth.account.privateKeyToAccount(sender_private_key)
    nonce = w3.eth.getTransactionCount(sender_address)
    txn = {
        'nonce': nonce,
        'to': recipient_address,
        'value': w3.toWei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    }
    signed_txn = sender_account.signTransaction(txn)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txn_hash.hex()

def send_bitcoin_transaction(sender_private_key, recipient_address, amount):
    # Bitcoin işlemi gönderme
    wallet = Wallet.import_key(sender_private_key)
    txn = wallet.send_to(recipient_address, amount)
    return txn.txid

def select_language():
    print("Please select your language / Bitte wählen Sie Ihre Sprache / Lütfen dilinizi seçin:")
    print("1. English")
    print("2. Deutsch")
    print("3. Türkçe")
    choice = input("Enter your choice / Geben Sie Ihre Auswahl ein / Seçiminizi girin: ")
    return choice

def get_user_input(language):
    if language == "1":
        recipient_prompt = "Please enter the recipient address: "
        amount_prompt = "Please enter the amount to send: "
    elif language == "2":
        recipient_prompt = "Bitte geben Sie die Empfängeradresse ein: "
        amount_prompt = "Bitte geben Sie den zu sendenden Betrag ein: "
    elif language == "3":
        recipient_prompt = "Alıcı adresini giriniz: "
        amount_prompt = "Gönderilecek miktarı giriniz: "
    else:
        print("Invalid choice.")
        return None, None
    recipient_address = input(recipient_prompt)
    amount = float(input(amount_prompt))
    return recipient_address, amount

def save_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# Dil seçeneği seçme
language_choice = select_language()

# Ethereum cüzdanı oluşturma
eth_private_key, eth_address = create_ethereum_wallet()
eth_info = f"Ethereum Private Key: {eth_private_key}\nEthereum Address: {eth_address}"

# Bitcoin cüzdanı oluşturma
btc_private_key, btc_address = create_bitcoin_wallet()
btc_info = f"Bitcoin Private Key: {btc_private_key}\nBitcoin Address: {btc_address}"

# Kullanıcıdan gerekli bilgileri alınması
recipient_address, amount = get_user_input(language_choice)

# Ethereum işlemi gönderme
eth_txn_hash = send_ethereum_transaction(eth_private_key, eth_address, recipient_address, amount)
eth_txn_info = f"Ethereum Transaction Hash: {eth_txn_hash}"

# Bitcoin işlemi gönderme
btc_txn_id = send_bitcoin_transaction(btc_private_key, recipient_address, amount)
btc_txn_info = f"Bitcoin Transaction ID: {btc_txn_id}"

# Bilgileri dosyaya yazma
file_content = f"{eth_info}\n\n{btc_info}\n\n{eth_txn_info}\n\n{btc_txn_info}"
file_name = "crypto_transaction_info.txt"
save_to_file(file_name, file_content)

print(f"Transaction information saved to {file_name}")
