from django.conf import settings
import xml.etree.ElementTree as ET
from kkb.kkb_sign import KKBSign
from django.template.loader import render_to_string
import base64
class Result:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

def xml2dict(xml):
	root = ET.fromstring(xml)
	bank = root.find('bank')
	customer = bank.find('customer')
	merchant = customer.find('merchant')
	order = merchant.find('order')
	department = order.find('department')
	merchant_sign = customer.find('merchant_sign')
	customer_sign = bank.find('customer_sign')
	results = bank.find('results')
	payment = results.find('payment')
	bank_sign = root.find('bank_sign')
	result = {
        'BANK_NAME': bank.get('name'),
        'CUSTOMER_NAME': customer.get('name'),
        'CUSTOMER_MAIL': customer.get('mail'),
        'CUSTOMER_PHONE': customer.get('phone'),
        'MERCHANT_CERT_ID': merchant.get('cert_id'),
        'MERCHANT_NAME': merchant.get('name'),
        'ORDER_ID': order.get('order_id'),
        'ORDER_AMOUNT': order.get('amount'),
        'ORDER_CURRENCY': order.get('currency'),
        'DEPARTMENT_MERCHANT_ID': department.get('merchant_id'),
        'DEPARTMENT_AMOUNT': department.get('amount'),
        'MERCHANT_SIGN_TYPE': merchant_sign.get('type'),
        'CUSTOMER_SIGN_TYPE': customer_sign.get('type'),
        'RESULTS_TIMESTAMP': results.get('timestamp'),
        'PAYMENT_MERCHANT_ID': payment.get('merchant_id'),
        'PAYMENT_AMOUNT': payment.get('amount'),
        'PAYMENT_REFERENCE': payment.get('reference'),
        'PAYMENT_APPROVAL_CODE': payment.get('approval_code'),
        'PAYMENT_RESPONSE_CODE': payment.get('response_code'),
        'BANK_SIGN_CERT_ID': bank_sign.get('cert_id'),
        'BANK_SIGN_TYPE': bank_sign.get('type'),
	}
	result['LETTER'] = letter = '<bank ' + xml.split('<bank ')[1].split('</bank>')[0] + '</bank>'
	result['SIGN'] = ET.tostring(bank_sign)
	result['RAWSIGN'] = bank_sign.text
	return result

	
def postlink_process(response=""):
	args = {
		'status' : False,
		'message':"",
	}
	result = Result(**args)
	try:
		root = ET.fromstring(response)
	except Exception as e:
		result.message = "xml file not parsable"
		return result
	if root.find('error'):
		result.message = root.find('error').text
		return result
	if root.tag == 'document':
		kkbSign = KKBSign()
		data = xml2dict(response)
		check = kkbSign.check(data['RAWSIGN'],data['LETTER'])
		if "Verified OK" in check:
			result.status = True
			result.data = data
			result.message = check
		else:
			result.message = check
	else:
		result.message = "[XML_DOCUMENT_UNKNOWN_TYPE]";
	return result


def get_context(order_id,amount='0',currency_id='398',b64=True):
	context = {
	'ORDER_ID' : int(order_id),
	'CURRENCY' : currency_id,
	'AMOUNT' : float(amount),
	'MERCHANT_CERTIFICATE_ID' : settings.MERCHANT_CERTIFICATE_ID,
	'MERCHANT_NAME' : settings.MERCHANT_NAME,
	'MERCHANT_ID' : settings.MERCHANT_ID,
	}
	kkbSign = KKBSign()
	try:
		rendered = render_to_string(settings.XML_TEMPLATE_FN, context)
	except Exception as e:
		return "Error reading XML template.";
	result_sign = "".join(['<merchant_sign type="RSA" cert_id="',settings.MERCHANT_CERTIFICATE_ID, '">',kkbSign.sign64(rendered).decode('utf-8'),'</merchant_sign>'])
	xml = "".join(["<document>",rendered,result_sign,"</document>"])
	if b64:
		return base64.b64encode(xml.encode('ascii')).decode('utf-8')
		#return "".join(base64.b64encode(xml.encode('utf-8')).split("\n"))
	else:
		return xml;
