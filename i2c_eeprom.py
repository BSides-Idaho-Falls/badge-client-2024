# Driver for the 24LC001 I2C EEPROM on the badge.
#
# Specifically, this makes use of the 'feature' that this EEPROM responds to all
# addresses of the form 0b101 0xxx (0x50--0x57), so this breaks individual
# transactions into out-of-order byte accesses. This trades efficiency for a bit
# more of a challenge for those reversing and sniffing the traffic.
#
# TODO: make a better granular read/write, maybe?
import random
import machine
import utime

# Addresses
I2C_LOW  = 0x50
I2C_HIGH = 0x57

LEN_EEPROM = 16 # bytes

#eeprom_write_command = bytearray([0xA0])


"""
Public interface. Use these to interact with the EEPROM
"""

def i2c_eeprom_init(i2c_handle: machine.I2C):
    # Setup the WP pin

    iwp = machine.Pin(22, machine.Pin.OUT)
    iwp.low()

    #mem_addr = 0x50
    # Don't actually need to mess with i2c_handle here currently


def write_i2c(i2c_handle, data, in_order=False):
    # Unsure what mem_addr is doing
    #mem_addr = 0

    if in_order:
        _ordered_write_data_to_i2c_eeprom(i2c_handle, data)
    else:
        _random_write_data_to_i2c_eeprom(i2c_handle, data)

def read_i2c(i2c_handle, in_order=False):
    """
    Read the entire contents of the I2C EEPROM
    """

    if in_order:

        # Pick a random address to read from
        dev_addr = random.randint(I2C_LOW, I2C_HIGH)
        data = i2c_handle.readfrom_mem(dev_addr, 0, LEN_EEPROM)

    else:
        # TODO: optimize this
        data = bytearray(LEN_EEPROM)

        # Generate a random ordering of addresses
        mem_addrs = _rand_sample(range(LEN_EEPROM), LEN_EEPROM)

        for i in range(LEN_EEPROM):

            # Randomize device address
            dev_addr = random.randint(I2C_LOW, I2C_HIGH)

            # Have to slice the returned bytes object to get an int-value from it
            data[mem_addrs[i]] = i2c_handle.readfrom_mem(dev_addr, mem_addrs[i], 1)[0]

    return data



def test_i2c(i2c_handle):
    # TODO!!!!!
    mem_addr = 0
    # write_data_to_i2c_eeprom(b'this is a eeprom', i2c_handle, 0x50)
    utime.sleep(.1)
    data = i2c_handle.readfrom_mem(80, 0, 32)
    # print("Read before : ", data )
    # i2c_handle.writeto_mem(80, 0, 0x50)
    print("Read after : ", i2c_handle.readfrom_mem(80, mem_addr, 4 ) )



"""
Internal functions to this file. These shouldn't be called by external callers.
"""
def _rand_sample(seq, k):
    """
    Pick k elements out of a set of n elements, by tracking the chosen elements.
    This is largely a simplified version of CPython's implementation, as μPy
    doesn't include one

    For simplicity, this just uses the list method for tracking the selected
    elements, since the intended usage has n == k.
    """

    def bit_len(i):
        """
        Bit-length implementation taken from Cpython. Uses an optimized shift
        and lut to figure out length.
        """
        table = [
            0, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4,
            5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5
            ]
        msb = 0

        while i >= 32:
            msb += 6
            i >>= 6
        msb += table[i];
        return msb

    def randbelow(x):
        k = bit_len(x)
        v = random.getrandbits(k)
        while v >= x:
            v = random.getrandbits(k)
        return v

    n = len(seq)
    result = [None] * k

    pool = list(seq)
    for i in range(k):
        j = randbelow(n - i)
        result[i] = pool[j]
        pool[j] = pool[n - i - 1]  # move non-selected item into vacancy

    return result


def _ordered_write_data_to_i2c_eeprom(i2c_handle, data):
    """
    TODO: This assumes that whatever it is to write starts at zero and is less
    than the eeprom size.
    """

    data = bytes(data, 'utf8')
    for item in range(0, len(data)):
        chunk = data[item].to_bytes(1, 'big')
        address_bytes = item
        # print(f'Attempting write {data[item]} as {chunk} to addr {address_bytes}\n')

        # Randomize device address
        dev_addr = random.randint(I2C_LOW, I2C_HIGH)
        utime.sleep_ms(10)
        i2c_handle.writeto_mem(dev_addr, item,  chunk)

def _random_write_data_to_i2c_eeprom(i2c_handle, data):
    """
    TODO: This assumes that whatever it is to write starts at zero and is less
    than the eeprom size.
    """
    over_len = min(LEN_EEPROM, len(data))

    # Generate a random ordering of addresses
    mem_addrs = _rand_sample(range(over_len), over_len)

    data = bytes(data, 'utf8')
    for item in range(over_len):
        chunk = data[item].to_bytes(1, 'big')
        #address_bytes = item
        # print(f'Attempting write {data[item]} as {chunk} to addr {address_bytes}\n')

        # Randomize device address
        dev_addr = random.randint(I2C_LOW, I2C_HIGH)
        utime.sleep_ms(10)
        i2c_handle.writeto_mem(dev_addr, item,  chunk)
