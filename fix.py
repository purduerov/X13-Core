import os 
import re 

store = set()

for xml in os.listdir('./labelled_images/'):
    store.add( re.findall(r'\d+', xml)[0] )
print(store)

for image in os.listdir('./images'):
    if not(image == 'a.bash'):
        num = re.findall(r'\d+', image)[0]
        
        if not(num in store):
            os.remove('./images/'+image)