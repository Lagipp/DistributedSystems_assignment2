import xmlrpc.client
from datetime import datetime


# sources used:
#    https://docs.python.org/3/library/xmlrpc.client.html 



def main():
    server = xmlrpc.client.ServerProxy('http://localhost:8000', allow_none=True)
    choice = 0
    
    print(f'\n== Welcome to the notebook application! ==\n')
    while True:
        print(f"  1) Add a new topic\n  2) Search for a topic\n  0) Quit\n")
        
        
        
        # trying to run the code
        
        try:
            choice = input(f'Your choice: ')
            
            
            # choice 1: posting a new topic
            #           calling the server-side function 'sendMessage' with
            #           user supplied parameters.
            
            if int(choice) == 1:
                newTopic = input(f'Enter a topic: ')
                newHeader = input(f'Enter a header: ')
                newContent = input(f'Enter text: ')
                newTimestamp = datetime.now().strftime('%c')
                
                print(f'\nTopic: {newTopic}\nText: {newContent}\nTime: {newTimestamp}')
                result = server.sendMessage(newTopic, newHeader, newContent, newTimestamp)
                
                print(result)
            
            
            # choice 2: searching for an existing topic
            #           calling the server-side function 'getMessage' with 
            #           searchTopic supplied by the user.
            
            elif int(choice) == 2:
                searchTopic = input(f'Search for a topic: ')
                result = server.getMessage(searchTopic)
                
                for item in result:
                    print(f'{item}')
                
                
            # choice 0: quitting the loop
            #           shutting the program down altogether.
                
            elif int(choice) == 0:
                print('Shutting down...\n')
                exit(0)
            
            
            # choice x: any input other than 0-2
            #           checking for letters/sentences/other
            #           and skipping them.
            
            else:
                print(f' Not a valid input, try again!\n')
        
        
        
        
        # checking for any errors
            
        except Exception as error:
            print("  -- Error occurred!: ", error)
            print(f'')
            
            
main()