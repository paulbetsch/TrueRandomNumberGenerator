
class Buffer:
    BUFFER_MAX_SIZE = 1000000
    BITS_PER_SECOND = 50
    FILE_PATH = "TRNG_Pendel/KameraRaspberryPi/bitBuffer.bin"
    
    def setBufferMaxSize(self, size):
        self.BUFFER_MAX_SIZE = size

    def GetBits(self, qty):
        """
        Returns Bits from the Buffer 

        param: qty - number of bits to return from buffer
        returns: Binary String (0s and 1s)
        """

        # Get bitStream from file
        try: 
            with open(self.FILE_PATH, 'rb') as file:
                byteStream = file.read().replace(b'\n', b'').replace(b'\r', b'').replace(b' ', b'').replace(b'\t', b'')
        except FileNotFoundError:
            self.CreateBufferFile()
            raise FileNotFoundError(f"File{self.FILE_PATH} not found")

        # Checks if enough bits are in the Buffer ( * 8 because 1 Byte = 8  Bit and qty is in Bit)
        if len(byteStream) * 8 >= qty:
            bitsToReturn = ''
            # Count of bytes needing to be extracted from the byteStream 
            byteCount = qty // 8
            remainingBits = qty % 8

            # Convert bytes to binary string
            for byte in byteStream[:byteCount]:
                bitsToReturn += format(byte, '08b')

            # Convert remaining bits to binary string
            if remainingBits > 0:
                lastByte = byteStream[byteCount]
                bitsToReturn += format(lastByte, '08b')[:remainingBits]

            # Update byteStream
            byteStream = byteStream[byteCount + (1 if remainingBits else 0):]

            # Write updated byteStream to file
            with open(self.FILE_PATH, 'wb') as file:
                file.write(byteStream)

            return bitsToReturn
        else:
            print(f"Insufficient amount of bits in the buffer. Refilling Buffer with '{qty - len(byteStream) * 8}' Bits")
            raise Exception("Invalid Parameter - missing bits in Buffer")
        

    def Fill(self, bitString):
        """
        param: bitString - binary String with prefix (0b)

        Refills the Buffer with the bitString
        """
        # Remove prefix from bitString
        bitString = bitString[2:]
        
        # Split the bit string into multiple 8-bit chunks
        chunks = [bitString[i:i+8] for i in range(0, len(bitString), 8)]
        
        # Convert each chunk to a byte and write to the file
        with open(self.FILE_PATH, 'ab') as file:
            for chunk in chunks:
                byte = int(chunk, 2).to_bytes(1, byteorder='big')
                file.write(byte)

    def Info(self, consolePrint):
        """
        Gives the User the current Buffer Info - size, count measurements, estimated time to refill buffer

        param: consolePrint(boolean), if True prints Info to console 

        returns Buffer size
        """
        try: 
            with open(self.FILE_PATH, 'rb') as file:
                bufferSize = len(file.read().replace(b'\n', b'').replace(b'\r', b'').replace(b' ', b'').replace(b'\t', b'')) * 8
        except FileNotFoundError:
            self.CreateBufferFile()
            raise FileNotFoundError(f"File{self.FILE_PATH} not found")
        missingBits = self.BUFFER_MAX_SIZE - bufferSize
        timeRefill = missingBits / self.BITS_PER_SECOND / 60
        
        if consolePrint:
            print(" - - - Buffer Info - - - ")
            print(f"Current Buffer size: {bufferSize}")
            print(f"Missing Bits for full Buffer: {missingBits}")
            print(f"estimated time to refill Buffer: ~{int(timeRefill)} minutes")
        return bufferSize
    
    def CreateBufferFile(self):
        with open(self.FILE_PATH, "wb") as file:
            file.write()


    def CreateNewBuffer(self, bitString):
        """
        Deletes the old Data Buffer and creates a new one.
        New Buffer can be optionally filled with Bits

        param: bitSting - binary String with prefix (0b)
        -- Call with empty bitStream to not fill Buffer (bin(0))
        """
        try: 
            with open(self.FILE_PATH, 'wb') as f:
                f.truncate(0)
        except FileNotFoundError:
            self.CreateBufferFile()
            raise FileNotFoundError(f"File{self.FILE_PATH} not found")
            
        # Check if bitString is longer than 0b0
        if len(bitString) > 3:
            self.Fill(bitString)
 
