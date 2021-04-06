import requests, concurrent.futures, socket
from bs4 import BeautifulSoup
import string as s
import itertools as it
#Symbols is just letters and numbers and a space and an underscore
symbols=s.ascii_letters
symbols+=''.join([str(i) for i in range(10)])
symbols+=' _-'

#user is between 3 and 20 chars 
possible_names= [it.combinations(symbols,i) for i in range(3,20) ]

redirect_page= BeautifulSoup(requests.get('https://www.reddit.com/user/a').text,'html.parser')

def internetOn(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False
    
def StateList(i,j):
    state_list=[]
    for combo_list in possible_names[i:j]:
        for name in combo_list:
            if internetOn():
                reddit= BeautifulSoup(requests.get('https://reddit.com/u/{}'.format(''.join(name))).text, 'html.parser')
                if reddit!=redirect_page:
                    state_list.append(''.join(name))
            else:
                while not internetOn():
                    continue
                reddit= BeautifulSoup(requests.get('https://reddit.com/u/{}'.format(''.join(name))).text, 'html.parser')
                if reddit!=redirect_page:
                    state_list.append(''.join(name))
                
                
            
        
    return state_list
    
    
def main():
    with open(r'C:\Users\ashib\Desktop\bruh.txt','wb') as bruh:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            intervals=[[0,4],[4,7],[7,11],[11,17]]
            
            results= [executor.submit(StateList,coords[0],coords[1]) for coords in intervals]
            
            for f in concurrent.futures.as_completed(results):
                bruh.write(''.join(f.result())+'\n')
                print()

if __name__ == '__main__':
    main()
