import tss
from tss import Hash
import base64
import time
import dropbox
import io
from dropbox.files import WriteMode
import New_user

#dropbox authentification code
dropbox_access_token= "sl.BFOH9gk88_xOqfapMXI_uvAc1ji2ijones_burN1ZEq_uvYWgDGQEElA7QVqccx7_Em2Q2q9vGoWZt3TDpWtawpAS-jOEo-UN7scRahOGmz1QQCN2Pqh_AyyMXSeMRylOzjOnDj99LNO"    #Enter your own access token
client = dropbox.Dropbox(dropbox_access_token)

#function to upload csv to dropbox app
def dropbox_upload():
    dropbox_path= r"/user_details/enc_logins.csv" #directory in dropbox to send to
    computer_path= r"C:\Users\samhu\Desktop\Encryption_Decryption\Chacha20_encryption_decryption\Cryptology_app\storage\enc_logins.csv" #directory of file to upload
    print("dropbox account connected")

    #uploads file in overwrite mode
    client.files_upload(open(computer_path, "rb").read(), dropbox_path, mode=WriteMode('overwrite'))
    print("successfully uploaded")
