
    
def run():
    import RPi.GPIO as GPIO
    from time import sleep    
    import time
    import keyboard
    
    GPIO.setwarnings(False)
    
    GPIO.setmode(GPIO.BCM) 
    
    #Motor
    GPIO.setup(6, GPIO.OUT)  
    #Magnet
    GPIO.setup(13, GPIO.OUT)  
                     
  
  
    while True:
        start = time.time()
        
        while start > time.time()-2:
            GPIO.output(6,1)
            GPIO.output(13,1)                      
     
        GPIO.output(6,0)      
        GPIO.output(13,0)    
        sleep(7)
     
    
def main(args):
    run()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
    GPIO.cleanup()

    
def run():
    import RPi.GPIO as GPIO
    from time import sleep    
    import time
    import keyboard
    
    GPIO.setwarnings(False)
    
    GPIO.setmode(GPIO.BCM) 
    
    #Motor
    GPIO.setup(6, GPIO.OUT)  
    #Magnet
    GPIO.setup(13, GPIO.OUT)  
                     
  
  
    while True:
        start = time.time()
        
        while start > time.time()-2:
            GPIO.output(6,1)
            GPIO.output(13,1)                      
     
        GPIO.output(6,0)      
        GPIO.output(13,0)    
        sleep(7)
     
    
def main(args):
    run()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
    GPIO.cleanup()
