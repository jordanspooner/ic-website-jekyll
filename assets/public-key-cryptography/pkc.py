import random
from fractions import gcd

msg = input('Enter a message: ')

print('\n')

n = int(input('Enter the length of your key: '))

##msg = 'HelloWorld'
##n = 10

x = ''.join('{:08b}'.format(ord(x)) for x in msg)

print('\n')
print('Message in binary: ')
print(x)

chunks = len(x)
chunk_size = n

to_encrypt = [x[i:i+chunk_size] for i in range(0, chunks, chunk_size)]

print('\n')
print(to_encrypt)

def key(n):

    def creation(n):
        
##        n = int(input('Enter the length of your key: '))
        
        global privatekey

        privatekey = [0] * n

        i = 0

        for i in range (0, len(privatekey)):

            privatekey[i] = round((random.uniform(1.0, 10.0)**5.0), 0)

            i += 1
        
        privatekey = sorted(privatekey)

        j = 0
        sum = 0
        test = True

        for j in range(0, len(privatekey)):
            
            if privatekey[j] <= sum:
                test = False
                break
            
            sum += privatekey[j]
            j += 1
         
        if test == False:
            creation(n)


    creation(n)

    def integers(n):
       
        global w
        global m
    
        w = round(random.uniform(0.0, 10.0) * 1000, 0)
        m = round(random.uniform(100.0, 150.0) * 1000, 0)

    ## print('w = ', w)
    ## print('m = ', m)

        key_sum = 0

        for i in range(0, len(privatekey)):

            key_sum += privatekey[i]

        if key_sum < m:
        
            if gcd(w, m) == 1:
            
                i = 0

                global publickey

                publickey = sorted(privatekey)

                for i in range(0, len(publickey)):

                    publickey[i] = (w * publickey[i]) % m
                    
                    i += 1

                j = 0
                sum = 0
                test = True

                for j in range(0, len(publickey)):
                    
                    if publickey[j] <= sum:
                        test = False
                        break
                    
                    sum += publickey[j]
                    j += 1
                 
                if test == False:
                    print('\n')
                    print('Privatekey: ')
                    print(privatekey)
                    print('\n')
                    print('w = ', w)
                    print('\n')
                    print('m = ', m)
                    print('\n')
                    print('Publickey: ')
                    print(publickey)

                else: ## test != false
                    key(n)

            else: ## gcd(w,m) != 1
                key(n)

        else: ## keysum >= m
            key(n)

    integers(n)

print('\n')
input('Press enter to continue: ')

key(n)

encrypted = [0] * len(to_encrypt)

for h in range(0, len(to_encrypt)):

    value = [to_encrypt[h][j:j+1] for j in range(0, n, 1)]
    
##    print(value)

    for i in range(0, len(publickey)):

        value2 = int(value[i]) * publickey[i]

        encrypted[h] += value2


print('\n')
input('Press enter to continue: ')
print('\n')
print('Encrypted message: ')
print(encrypted)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else: ## a != 0
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else: ## g == 1
        return x % m

winv = modinv(w, m)

print('\n')
print('Inverse of w: ' + str(winv))

print('\n')
input('Press enter to continue: ')

conver = [0] * len(encrypted)

for i in range(0, len(encrypted)):

    conver[i] = (encrypted[i]*winv) % m

print('\n')
print('Converted: ')
print(conver)

print('\n')
input('Press enter to continue: ')

p_descend = sorted(privatekey, reverse=True)

print('\n')
print('Private key descending: ')
print(p_descend)

final = [0] * len(encrypted)

for i in range(0, len(encrypted)):

    summ = 0
    decrypt = [0] * n
    
    for j in range(0, len(p_descend)):

        if p_descend[j] + summ <= conver[i]:

            decrypt[j] = 1
            
            summ += p_descend[j]

        else: ## p_descend[j] + summ > conver[i]

            decrypt[j] = 0;

    decrypt.reverse()
    
    decrypt = ''.join(map(str, decrypt))

    final[i] = decrypt

final = ''.join(final)

print('\n')
input('Press enter to continue: ')

print('\n')
print('Decrypted binary message: ')
print(final)

final_msg = ''.join(chr(int(final[i:i+8], 2)) for i in range(0, len(final), 8))

print('\n')
input('Press enter to continue: ')

print('\n')
print('Decrypted message: ')
print(final_msg)
