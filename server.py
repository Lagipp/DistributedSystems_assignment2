from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ETree

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2,')

# sources used:    
#    https://docs.python.org/3/library/xmlrpc.server.html
#    https://docs.python.org/3/library/xml.etree.elementtree.html



def main():
    with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()
        
        
        # sendMessage():    / sending a new message to the XML-database /
        #                   parameters are given by user in the client-side code.
        
        def sendMessage(topic, header, content, timestamp):
            try:
                
                # opening up the xml-db
                
                tree = ETree.parse('db.xml')
                root = tree.getroot()
                
                print(f'\nRequesting a message:\nTopic: {topic}\nHeader: {header}\nText: {content}\nTime: {timestamp}')
                
                
                # searching for the topic name from the xml-db
                #   if the topic is already existing -> adding
                #   only the new message under the same topic
                
                for child in root:
                    if child.attrib['name'] == topic:
                        print(f'Found existing topic \'{topic}\'.')
                        
                        newNote = ETree.SubElement(child, 'note')
                        newNote.set('name', header)
                        
                        newNoteContent = ETree.SubElement(newNote, 'text')
                        newNoteContent.text = content
                        
                        newNoteTimestamp = ETree.SubElement(newNote, 'timestamp')
                        newNoteTimestamp.text = timestamp
                        
                        tree.write('db.xml')
                        
                        result = f'Added new message to existing topics.\n'
                        return result
                    
                
                
                # if there was no existing topic, creating a new one
                # and adding all parts of the message under it
                
                    
                print(f'Creating new topic \'{topic}\'...')
                
                newTopic = ETree.SubElement(root, 'topic')
                newTopic.set('name', topic)
                
                newNote = ETree.SubElement(newTopic, 'note')
                newNote.set('name', header)
                
                newNoteText = ETree.SubElement(newNote, 'text')
                newNoteText.text = content
                
                newNoteTimestamp = ETree.SubElement(newNote, 'timestamp')
                newNoteTimestamp.text = timestamp
                
                tree.write('db.xml')
                
                result = f'Created a new topic.\n'
                return result
                        
           
            except Exception as error:
                print("  -- Error occurred!: ", error)
                print(f'')
                
                
        # getMessage():     / trying to fetch a message from the XML-database /
        #                   searching for the user's desired topic from the database.
        
        def getMessage(topic):
            try:
                
                # opening the xml-db
                
                tree = ETree.parse('db.xml')
                root = tree.getroot()
                
                print(f'\nRequest for topic \'{topic}\'')
                
                result = []
                
                
                # searching for the topic name from the xml-db
                #   if the topic is found -> copying it into a message
                #   which is then sent to the user
                
                for child in root:
                    if child.attrib['name'] == topic:
                        result.append(child.attrib['name'])
                        result.append('\n')
                        
                        for gchild in child:
                            result.append(gchild.attrib['name'])
                            
                            for msg in gchild:
                                result.append(msg.text)
                                
                            result.append('\n')
                        return result
                    
                    
                    # if the topic name wasn't found:
                    
                    return ['No topic found.\n']
                
    
            # universal error handling
    
            except Exception as error:
                print("  -- Error occurred!: ", error)
                print(f'')
                
                
                
    # https://docs.python.org/3/library/xmlrpc.server.html#xmlrpc.server.SimpleXMLRPCServer.register_function 
    
    # registering the functions for the client-side to use them

        server.register_function(sendMessage, 'sendMessage')
        server.register_function(getMessage, 'getMessage')
        
        # TODO: save the port as a constant variable
        print(f'\nServer started, listening to port 8000.\n')
        
        server.serve_forever()
        
main()