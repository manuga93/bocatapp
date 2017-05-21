import requests
import base64
import json
import datetime

class PSCPayment:

    def __init__(self, key, environment):
        #Construct payment class.
        self.key = key #define psc key
        self.error = {}
        self.environment = environment
        self.setEnvironment()


    def doRequest(self, parameter, method, headers=None):
        """
        Make an API request and return all needed information
        """

        # define default headers
        header = {'Authorization': 'Basic ' + base64.b64encode(self.key), 'Content-Type': 'application/json'}

        self.requestParameter = parameter
        # add additional header
        if headers is not None:
            for key in headers:
                header[key] = headers[key]
        # method handling
        if method == 'POST':
            r = requests.post(self.url, data=json.dumps(parameter), headers=header)
        elif method == 'GET':
            r = requests.get(self.url, headers=header)

        # asign requested data
        self.request = r
        self.requestinfo = {}
        self.requestinfo['links'] = r.links
        self.requestinfo['status_code'] = r.status_code
        self.requestinfo['reason'] = r.reason
        self.requestinfo['response'] = r.request
        self.requestinfo['url'] = r.url
        self.requestinfo['headers'] = r.headers
        self.requestinfo['apparent_encoding'] =  r.apparent_encoding

        # Reset URL
        self.setEnvironment()


    def requestIsOK(self):
        # check if request was successful
        if self.request.status_code < 300:
            return True
        else:
            return False

    def getResponse(self):
        # get the response
        if not self.request.json():
            return {}
        else:
            return self.request.json()

    def getRequestPrameter(self):
        # get request parameter
        return self.requestParameter

    def getRequestInfo(self):
        # get Request Information
        return self.requestinfo


    def setEnvironment(self):
        # set the environment and URLs
        if self.environment == 'TEST':
            self.url = 'https://apitest.paysafecard.com/v1/payments/'
        elif self.environment == 'PRODUCTION':
            self.url = 'https://api.paysafecard.com/v1/payments/'
        else:
            print "#### environment not supported"

    def retrievePayment(self, payment_id):
        # retrieve payment informations
        self.url = self.url + payment_id
        self.doRequest({}, 'GET')
        # return False if request failed
        if self.requestIsOK:
            return self.getResponse()
        else:
            return False

    def capturePayment(self, payment_id):
        # capture a payment
        self.url = self.url + payment_id + '/capture'
        parameter = {'id':payment_id}
        self.doRequest(parameter, 'POST')
        # return False if request failed
        if self.requestIsOK:
            return self.getResponse()
        else:
            return False


    def createPayment(self, amount, currency, customer_id, customer_ip, success_url, failure_url, notification_url, correlation_id=None, country_restriction=None, kyc_restriction=None, min_age=None, shop_id=None, submerchant_id=None):
        # create a payment
        """
        necessary variables:
        amount = 10.00 # payments amount
        currency = 'EUR' # payment currency, USD, EUR, SEK..
        customer_id = 'customer_id_123' # your psc customer id, merchant client id
        customer_ip = '123.123.123.123' # the customers IP
        success_url = 'http://www.yoururl.com/success.php?payment_id={payment_id}' # URL to redirect the customer to after a successful payment
        failure_url = 'http://www.yoururl.com/failure.php?payment_id={payment_id}' # URL to redirect the customer to after a failed payment
        notification_url = 'http://www.yoururl.com/notification.php?payment_id={payment_id}' # URL to call by the psc API to notify your scripts of the payment
        optional variables:
        correlation_id = str(uuid.uuid4()) # Define a unique identifier for referencing (optional) default is None
        country_restriction = 'DE' # restrict to certain country
        kyc_restriction = 'FULL' # only allow customers with a certain kyc level
        min_age = 18 # set the minimum age of the customer
        shop_id = 1 # chose the shop id to use for this payment
        submerchant_id = 1 # Reporting criteria
        """

        headers = {}
        customer = {
        'id': customer_id,
        'ip': customer_ip
        }

        if country_restriction is not None:
            customer['country_restriction'] = country_restriction

        if kyc_restriction is not None:
            customer['kyc_level'] = kyc_restriction

        if min_age is not None:
            customer['min_age'] = min_age

        parameter = {
            'currency' : currency,
            'amount' : amount,
            'customer' : customer,
            'redirect' : {
                'success_url' : success_url,
                'failure_url' : failure_url,
            },
            'type' : 'PAYSAFECARD',
            'notification_url' : notification_url,
            'shop_id'          : shop_id
        }

        if submerchant_id is not None:
            parameter['submerchant_id'] = submerchant_id

        if correlation_id is not None:
            headers['Correlation-ID'] = correlation_id

        self.doRequest(parameter, 'POST', headers)

        if self.requestIsOK:
            return self.getResponse()
        else:
            return False


    def getError(self):
        # get Errors request errors and returned errors

        if self.request.status_code == 400:
            self.error['number'] = "HTTP:400"
            self.error['message'] = 'Logical error. The requested URL cannot be found. Check your request data'
        elif self.request.status_code == 403:
            self.error['number']  = "HTTP:403"
            self.error['message'] = 'Transaction could not be initiated due to connection problems. The servers IP address is probably not whitelisted!'
        elif self.request.status_code == 500:
            self.error['number']  = "HTTP:500"
            self.error['message'] = 'Server error.'

        if self.error:
            return self.error
        if 'number' in self.getResponse():
            if self.getResponse()['number'] == 4003:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'The amount for this transaction exceeds the maximum amount. The maximum amount is 1000 EURO (equivalent in other currencies)'
            elif self.getResponse()['number'] == 3001:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Transaction could not be initiated because the account is inactive.'
            elif self.getResponse()['number'] == 2002:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'payment id is unknown.'
            elif self.getResponse()['number'] == 2010:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Currency is not supported.'
            elif self.getResponse()['number'] == 2029:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Amount is not valid. Valid amount has to be above 0.'
            else:
                self.error['number'] = self.getResponse()['number']
                self.error['message'] = 'Transaction could not be initiated due to connection problems. If the problem persists, please contact our support.';

        return self.error
