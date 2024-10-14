import warnings

class IPv4Address:
    _ADDRESS_INVALID_FORMAT = "IPv4 bad address format"
    _ADDRESS_CHARACTER_ERROR = "IPv4 address contains unusual characters."
    _ADDRESS_IS_SUBNET_ID = "Invalid IP Address, this is the Subnet Address for the given CIDR"
    _ADDRESS_IS_BROADCAST_ID = "Invalid IP Address, this is the Broadcast Address for the given CIDR"
    _ADDRESS_NOT_STR = "IPv4 must be written as a string. Ex. '192.168.10.1'"
    _ADDRESS_OCTET_RANGE = "Address octets must be between 0 and 255 inclusive."
    _SUBNET_INVALID_FORMAT = "Bad subnet_mask address"
    _CIDR_NOT_INT = "CIDR notation must be an integer."
    _CIDR_OUT_OF_RANGE = "CIDR must be between 0 and 32."
    _CIDR_NOT_SET = "CIDR has not been set."

    def __init__(self, address, cidr):
        self._cidr = self._validate_cidr(cidr)
        self._address = self._validate_address(address) # validation of the address is reliant on the cidr notation

    def _validate_cidr(self, cidr):
        if not isinstance(cidr, int):
            raise TypeError(self._CIDR_NOT_INT)
        
        if cidr < 0 or cidr > 32:
            raise ValueError(self._CIDR_OUT_OF_RANGE)
        
        if cidr == 31:
            warnings.warn('Warning: CIDR is /31. This is typically used in networking equipment for point-to-point connections, and not typically used for edge devices.')
        
        return cidr
    
    def _validate_address(self, address):
        # Step 1: Format Validation
        if not isinstance(address, str):
            raise TypeError(self._ADDRESS_NOT_STR)
        
        address_octets = address.split('.')
        if len(address_octets) != 4:
            raise ValueError(self._ADDRESS_INVALID_FORMAT)
        
        try:
            address_octets = [int(octet) for octet in address_octets]
        except ValueError:
            raise ValueError(self._ADDRESS_INVALID_FORMAT)
        
        for octet in address_octets:
            if octet < 0 or octet > 255:
                raise ValueError(self._ADDRESS_OCTET_RANGE) 
        
        # Step 2: Determine Subnet Address and Broadcast Address
        subnet_octets = self.subnet_mask.split('.') # this should be safe, as I guarantee the octets themselves
        subnet_octets = [int(subnet_octet) for subnet_octet in subnet_octets] # convert to integers
        wildcard_octets = [(255 - subnet_octet) for subnet_octet in subnet_octets] # essentially the inverse of the subnet mask
        
        subnet_address_result = []
        broadcast_result = []

        if self._cidr_check():
            for i in range(4):
                subnet_address_result.append(address_octets[i] & subnet_octets[i])
                broadcast_result.append(address_octets[i] | wildcard_octets[i])
        
                self._subnet_address = f'{subnet_address_result[0]}.{subnet_address_result[1]}.{subnet_address_result[2]}.{subnet_address_result[3]}'

        # Step 3: Ensure the address is not the Subnet Address or a Broadcast Address
        if address_octets == subnet_address_result:
            raise ValueError(self._ADDRESS_IS_SUBNET_ID)
        
        if address_octets == broadcast_result:
            raise ValueError(self._ADDRESS_IS_BROADCAST_ID)
        
        self._integer_ip = (address_octets[0] << 24) + (address_octets[1] << 16) + (address_octets[2] << 8) + address_octets[3]

        return address
            

    @property
    def subnet_address(self):
        if self._cidr_check():
            return self._subnet_address
        else:
            print(f'There is no subnet address for {self.address}/{self.cidr}')
    
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = self._validate_address(address)

    @property
    def cidr(self):
        return self._cidr
    
    @cidr.setter
    def cidr(self, cidr):
        self._cidr = self._validate_cidr(cidr)

    @property
    def subnet_mask(self):
        if self._cidr != None:
            cidr_dict = {
                0: '0.0.0.0',
                1: '128.0.0.0',
                2: '192.0.0.0',
                3: '224.0.0.0',
                4: '240.0.0.0',
                5: '248.0.0.0',
                6: '252.0.0.0',
                7: '254.0.0.0',
                8: '255.0.0.0',
                9: '255.128.0.0',
                10: '255.192.0.0',
                11: '255.224.0.0',
                12: '255.240.0.0',
                13: '255.248.0.0',
                14: '255.252.0.0',
                15: '255.254.0.0',
                16: '255.255.0.0',
                17: '255.255.128.0',
                18: '255.255.192.0',
                19: '255.255.224.0',
                20: '255.255.240.0',
                21: '255.255.248.0',
                22: '255.255.252.0',
                23: '255.255.254.0',
                24: '255.255.255.0',
                25: '255.255.255.128',
                26: '255.255.255.192',
                27: '255.255.255.224',
                28: '255.255.255.240',
                29: '255.255.255.248',
                30: '255.255.255.252',
                31: '255.255.255.254',
                32: '255.255.255.255'
            }

            return cidr_dict[self._cidr]
        else:
            raise ValueError(self._CIDR_NOT_SET)
        
    @property
    def integer_ip(self):
        return self._integer_ip
    
    def __gt__(self, other):
        if not isinstance(other, IPv4Address):
            return NotImplemented
        return self.integer_ip > other.integer_ip
    
    def __lt__(self, other):
        if not isinstance(other, IPv4Address):
            return NotImplemented
        return self.integer_ip < other.integer_ip
    
    def __ge__(self, other):
        if not isinstance(other, IPv4Address):
            return NotImplemented
        return self.integer_ip >= other.integer_ip
    
    def __le__(self, other):
        if not isinstance(other, IPv4Address):
            return NotImplemented
        return self.integer_ip <= other.integer_ip
    
    def __eq__(self, other):
        if not isinstance(other, IPv4Address):
            return NotImplemented
        return self.integer_ip == other.integer_ip
    
    def __ne__(self, other):
        if not isinstance(other, IPv4Address):
            return NotImplemented
        return self.integer_ip != other.integer_ip
    
    def _cidr_check(self):
        if self._cidr != 31 and self._cidr != 32:
            return True
        else:
            return False
        
addr1 = IPv4Address('192.168.10.1', 31)
print(addr1.address)
print(addr1.cidr)
print(addr1.subnet_mask)
print(addr1.subnet_address)
print(addr1.integer_ip)