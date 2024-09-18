class IPv4Address:
    ADDRESS_INVALID_FORMAT = "IPv4 bad address format"
    SUBNET_INVALID_FORMAT = "Bad subnet_mask address"

    def __init__(self, address, subnet_mask):
        self._address = self._validate_address(address)
        self._subnet_mask = self._validate_subnet(subnet_mask)

    def address_as_list(self):
        octets = self._address.split('.')
        octets = [int(octet) for octet in octets]

        return octets
    
    def subnet_as_list(self):
        octets = self._subnet_mask.split('.')
        octets = [int(octet) for octet in octets]

        return octets
    # END subnet_as_list()

    def _validate_address(self, _address):

        if not isinstance(_address, str):
            raise ValueError(self.ADDRESS_INVALID_FORMAT)

        octets = _address.split('.')
        if len(octets) != 4:
            raise ValueError(self.ADDRESS_INVALID_FORMAT)
        
        # Convert each octet into an integer
        octets = [int(octet) for octet in octets]

        for octet in octets:
            if octet < 0 or octet > 255:
                raise ValueError(self.ADDRESS_INVALID_FORMAT)
        
        return _address
    # END _validate_address()

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, _address):
        self._address = self._validate_address(_address)
    
    def _validate_subnet(self, subnet_mask):

        if not isinstance(subnet_mask, str):
            raise ValueError(self.SUBNET_INVALID_FORMAT)
        
        octets = subnet_mask.split('.')
        if len(octets) != 4:
            raise ValueError(self.SUBNET_INVALID_FORMAT)
        
        octets = [int(octet) for octet in octets]

        for i in range(4):
            octet = octets[i]
            if (octet != 0 and octet != 128 and octet != 192 
                and octet != 224 and octet != 240 and octet != 248 
                and octet != 252 and octet != 255):
                raise ValueError(self.SUBNET_INVALID_FORMAT)
            if i != 0:
                if octets[i - 1] != 255 or octets[i - 1] == 0:
                    if octet != 0:
                        raise ValueError(self.SUBNET_INVALID_FORMAT)

        
        return subnet_mask
    # END _validate_subnet()

    @property
    def subnet_mask(self):
        return self._subnet_mask
    
    @subnet_mask.setter
    def subnet_mask(self, _subnet):
        self._subnet_mask = self._validate_subnet(_subnet)

addr1 = IPv4Address("192.168.10.1", "255.255.240.0")
print(addr1.address, addr1.subnet_mask)