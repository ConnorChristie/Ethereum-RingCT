from secp256k1 import * 
import struct
import random

MAX_AMOUNT = 2**64;
MAX_MIXIN = 100; 

def getPublicKeys(number):
	# TODO
	return False


def pedersen(m, r):
	return (pow(g,m,p)*pow(h,r,p))%p


def ecdhEncode(mask, amount, receiverPk): 
	sendPriv = PrivateKey()
	recvPubKey = PublicKey(pubkey=receiverPk, raw=True)
	sharedSecret = recvPubKey.ecdh(bytes.fromhex(sendPriv.serialize()))
	sharedSecretInt = int.from_bytes(sharedSecret, byteorder='big')
	#overlow ??
	newMask = mask + sharedSecretInt
	newAmount = amount + sharedSecretInt
	return newMask, newAmount, sendPriv.pubkey.serialize()

def ecdhDecode(mask, amount, senderPk, receiverSk): 
	priv = PrivateKey(privkey=receiverSk, raw=True)
	sharedSecret = PublicKey(pubkey=senderPk, raw=True).ecdh(bytes.fromhex(priv.serialize()))
	sharedSecretInt = int.from_bytes(sharedSecret, byteorder='big')
	newMask = mask - sharedSecretInt
	newAmount = amount - sharedSecretInt
	return newMask, newAmount

def genMG(pubs, inSk, outSk, outPk, index):
    #pubs is a matrix of ctkeys [P, C] 
    #inSk is the keyvector of [x, mask] secret keys
    #outMasks is a keyvector of masks for outputs
    #outPk is a list of output ctkeys [P, C]
    #index is secret index of where you are signing (integer)
    #returns a list (mgsig) [ss, cc, II] where ss is keymatrix, cc is key, II is keyVector of keyimages

    rows = len(pubs[0])
    cols = len(pubs)

def createTransaction(privateKey, publicKey, destinations, amounts, mixin):
	if(mixin < 0 or mixin > MAX_MIXIN):
		print("The number of ring participant should be between 0 and " + str(MAX_MIXIN) + "\n Aborting...")
		return False
	try:
		privkey = PrivateKey(privkey=privateKey, raw=True)
		pubkey = privkey.pubkey;
		assert pubkey.serialize() == PublicKey(pubkey=publicKey, raw=True).serialize()
	except AssertionError:
		print("Derived public key: " + bytes.hex(privkey.pubkey.serialize()))
		print("Provied public key: " + bytes.hex(PublicKey(pubkey=publicKey, raw=True).serialize()))
		print("The provided public key doesn't match the private key.\n Aborting...")
	except Exception:
		print("The private key is not in the right format.\n\
			The format is either a compressed key as a string of 33 hex or an uncompresed key as a string of 65 hex.\n\
			Aborting...")
		return False

	if(len(destinations) != len(amounts) or mixin != len(amounts)):
		print("The mixin number should match the number of outputs addresses and the number of outputs amounts.\n Aborting...")
		return False

	destPubKeys = []
	for i in range (0, len(destinations)):
		try:
			destPubKeys.append(PublicKey(pubkey=destinations[i], raw=True))
		except Exception:
			print("The public key #" + str(i) + " is not in the right format.\n\
				The format is either a compressed key as a string of 33 hex or an uncompresed key as a string of 65 hex.\n\
				Aborting...")
	for i in range (0, len(amounts)):
		if(amounts[i] < 0 or amounts[i] > MAX_AMOUNT):
			print("The amount #" + str(i) + " should be between 0 and " + str(MAX_AMOUNT) + "\n Aborting...")
			return False



	

def test():
	for i in range(0, 10):
		x = random.randrange(21784719801723098712037190283701982371098273102873012873083917231287301287313289)
		y = random.randrange(21784719801723098712037190283701982371098273102873012873083917231287301287313289)
		newMask, newAmount, sendPubKey = ecdhEncode(x, y, bytes.fromhex(pub))
		newX, newY = ecdhDecode(newMask, newAmount, sendPubKey, bytes.fromhex(pri))
		assert newX == x and newY == y, "ECDH failed, x = %d, y = %d" % (x, y)

pri = "07ca500a843616b48db3618aea3e9e1174dede9b4e94b95b2170182f632ad47c"
pub = "0462abcca39e6dbe30ade7be2949239311162792bdb257f408ccd9eab65e18bc5bbcf8a3f08675bd792251a23d09a48a870644ba3923996cc5b5ec2d68043f3df3"
pub2 = "040ccad48919d8f6a206a1ac7113c22db62aa744a0700762b70aa0284d474c00203029637ce8e84f6551fd92a0db8e1f964ff13aa992e4cbfd1fb8fa33c6e6c53c"
pub3 = "049f742f925b554e2dc02e2da5cb9663ef810e9eefb30818b3c12bc26afb8dd7ba3461c0f7d2b997bf455973af308a71ed34ae415cfc946de84db3961db522e5d2"
createTransaction(bytes.fromhex(pri), bytes.fromhex(pub), [bytes.fromhex(pub2), bytes.fromhex(pub3)], [1, 2], 2)

newMask, newAmount, sendPubKey = ecdhEncode(1,2,bytes.fromhex(pub))
# print(bytes.hex(newMask))
# print(bytes.hex(newAmount))

ecdhDecode(newMask, newAmount, sendPubKey, bytes.fromhex(pri))


test()

