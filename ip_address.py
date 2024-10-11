class IPv4Address:
    ADDRESS_INVALID_FORMAT = "IPv4 bad address format"
    ADDRESS_IS_SUBNET_ID = "Invalid IP Address, this is the Subnet Address for the given CIDR"
    ADDRESS_IS_BROADCAST_ID = "Invalid IP Address, this is the Broadcast Address for the given CIDR"
    ADDRESS_NOT_STR = "IPv4 must be written as a string. Ex. '192.168.10.1'"
    ADDRESS_OCTET_RANGE = "Address octets must be between 0 and 255 inclusive."
    SUBNET_INVALID_FORMAT = "Bad subnet_mask address"
    CIDR_NOT_INT = "CIDR notation must be an integer."
    CIDR_OUT_OF_RANGE = "CIDR must be between 0 and 32."
    CIDR_NOT_SET = "CIDR has not been set."

    def __init__(self, address, cidr):
        self._cidr = self._validate_cidr(cidr)
        self._address = self._validate_address(address) # validation of the address is reliant on the cidr notation

    def _validate_cidr(self, cidr):
        if not isinstance(cidr, int):
            raise TypeError(self.CIDR_NOT_INT)
        
        if cidr < 0 or cidr > 32:
            raise ValueError(self.CIDR_OUT_OF_RANGE)
        
        return cidr
    
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
            ValueError(self.CIDR_NOT_SET)
    
    def _validate_address(self, address):
        # must not be the broadcast address
        if not isinstance(address, str):
            raise TypeError(self.ADDRESS_NOT_STR)
        
        octets = address.split('.')

        # Convert each octet into an integer
        octets = [int(octet) for octet in octets]
        if len(octets) != 4:
            raise ValueError(self.ADDRESS_INVALID_FORMAT)
        
        for octet in octets:
            if octet < 0 or octet > 255:
                raise ValueError(self.ADDRESS_OCTET_RANGE)
        
        subnet_mask = self.subnet_mask()
        subnet_octets = subnet_mask.split('.') # this should be safe, as I guarantee the octets themselves
        subnet_octets = [int(subnet_octet) for subnet_octet in subnet_octets] # convert to integers
        wildcard_octets = [(255 - subnet_octet) for subnet_octet in subnet_octets]
        
        id_result = []
        broadcast_result = []

        for i in range(4):
            id_result.append(octets[i] & subnet_octets[i])
            broadcast_result.append(octets[i] | wildcard_octets[i])
        
        if octets == id_result:
            raise ValueError(self.ADDRESS_IS_SUBNET_ID)
        
        if octets == broadcast_result:
            raise ValueError(self.ADDRESS_IS_BROADCAST_ID)

        self._subnet_address = f'{id_result[0]}.{id_result[1]}.{id_result[2]}.{id_result[3]}'

        return address

    
    def subnet_address(self):
        return self._subnet_address


        

addr1 = IPv4Address('192.168.10.255', 24)
print(addr1._address)
print(addr1.subnet_mask())
print(addr1.subnet_address())


# class IPv4Address:
#     ADDRESS_INVALID_FORMAT = "IPv4 bad address format"
#     ADDRESS_IS_SUBNET_ID = "Invalid IP Address, this is the Subnet Address for the given subnet_mask/cidr"
#     SUBNET_INVALID_FORMAT = "Bad subnet_mask address"

#     def __init__(self, address, subnet_mask):
#         self._subnet_mask = self._validate_subnet(subnet_mask) # it is important to validate the subnet_mask first, as this helps to validate the address
#         self._address = self._validate_address(address)
#     # END __init__()

#     def address_as_list(self):
#         octets = self._address.split('.')
#         octets = [int(octet) for octet in octets]

#         return octets
#     # END address_as_list()

#     def subnet_as_list(self):
#         octets = self._subnet_mask.split('.')
#         octets = [int(octet) for octet in octets]

#         return octets
#     # END subnet_as_list()

#     def _validate_address(self, _address):

#         if not isinstance(_address, str):
#             raise ValueError(self.ADDRESS_INVALID_FORMAT)

#         octets = _address.split('.')
#         if len(octets) != 4:
#             raise ValueError(self.ADDRESS_INVALID_FORMAT)
        
#         # Convert each octet into an integer
#         octets = [int(octet) for octet in octets]

#         for octet in octets:
#             if octet < 0 or octet > 255:
#                 raise ValueError(self.ADDRESS_INVALID_FORMAT)
            
#         # frankly, a lot of this would have been easier if doing bitwise operators. Probably faster too.

        
#         return _address
#     # END _validate_address()

#     @property
#     def address(self):
#         return self._address

#     @address.setter
#     def address(self, _address):
#         self._address = self._validate_address(_address)
    
#     def _cidr_to_subnet(self, cidr):

#         cidr_dict = {
#             0: '0.0.0.0',
#             1: '128.0.0.0',
#             2: '192.0.0.0',
#             3: '224.0.0.0',
#             4: '240.0.0.0',
#             5: '248.0.0.0',
#             6: '252.0.0.0',
#             7: '254.0.0.0',
#             8: '255.0.0.0',
#             9: '255.128.0.0',
#             10: '255.192.0.0',
#             11: '255.224.0.0',
#             12: '255.240.0.0',
#             13: '255.248.0.0',
#             14: '255.252.0.0',
#             15: '255.254.0.0',
#             16: '255.255.0.0',
#             17: '255.255.128.0',
#             18: '255.255.192.0',
#             19: '255.255.224.0',
#             20: '255.255.240.0',
#             21: '255.255.248.0',
#             22: '255.255.252.0',
#             23: '255.255.254.0',
#             24: '255.255.255.0',
#             25: '255.255.255.128',
#             26: '255.255.255.192',
#             27: '255.255.255.224',
#             28: '255.255.255.240',
#             29: '255.255.255.248',
#             30: '255.255.255.252',
#             31: '255.255.255.254',
#             32: '255.255.255.255'
#         }

#         return cidr_dict[cidr]

#     def _validate_subnet(self, subnet_mask):
#         # if the subnet mask is not a string or an integer, then the value is bad
#         if not isinstance(subnet_mask, str) and not isinstance(subnet_mask, int):
#             raise ValueError(self.SUBNET_INVALID_FORMAT)
        
#         # if the subnet_mask is in cidr notation, it is an int
#         if isinstance(subnet_mask, int):
#             if subnet_mask >= 0 and subnet_mask <= 32:
#                 subnet_mask = self._cidr_to_subnet(subnet_mask)
#             else:
#                 raise ValueError(self.SUBNET_INVALID_FORMAT) # TODO make this a different error.

#         if isinstance(subnet_mask, str):
#             octets = subnet_mask.split('.')
#             if len(octets) != 4:
#                 raise ValueError(self.SUBNET_INVALID_FORMAT)
            
#             octets = [int(octet) for octet in octets]

#             for i in range(4):
#                 octet = octets[i]
#                 if (octet != 0 and octet != 128 and octet != 192 
#                     and octet != 224 and octet != 240 and octet != 248 
#                     and octet != 252 and octet != 255):
#                     raise ValueError(self.SUBNET_INVALID_FORMAT)
#                 if i != 0:
#                     if octets[i - 1] != 255 or octets[i - 1] == 0:
#                         if octet != 0:
#                             raise ValueError(self.SUBNET_INVALID_FORMAT)

        
#         return subnet_mask
#     # END _validate_subnet()

#     @property
#     def subnet_mask(self):
#         return self._subnet_mask
    
#     @subnet_mask.setter
#     def subnet_mask(self, _subnet):
#         self._subnet_mask = self._validate_subnet(_subnet)

#     def subnet_id(self):



# addr1 = IPv4Address("192.168.10.1", "255.255.240.0")
# print(addr1.address, addr1.subnet_mask)

# addr2 = IPv4Address("10.0.0.1", 24)
# print(addr2.address, addr2.subnet_mask)

# addr3 = IPv4Address('10.0.0.0', 24) # this would be invalid, as 10.0.0.0 would be a subnet address
# print(addr3.address, addr3.subnet_mask)