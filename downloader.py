"""
import urllib

out = '/c/Users/corvit/Downloads/Slow_Deustsch/'
for i in range(125, 1):
    msg = f'i={i}'
    print(msg)
    pdf = 'sg' + str(i) + 'kurz.pdf'
    url = 'https://slowgerman.com/folgen/' + pdf

    file = urllib.urlopen(url)
    with open('out' + pdf, 'wb') as output:
        output.write(file.read())

    mp3 = 'sg' + str(i) + '.mp3'
    url = 'https://slowgerman.com/folgen/' + mp3

    file = urllib.urlopen(url)
    with open('out' + mp3, 'wb') as output:
        output.write(file.read())
"""


import os
import wget

print('Beginning file download with wget module')
out = os.path.abspath('/Users/corvit/Downloads/Slow_Deustsch/')

for i in range(126, 280):
    """
    msg = f'i={i}'
    print(msg)
    pdf = 'sg' + str(i) + 'akurz.pdf'
    url = 'https://slowgerman.com/folgen/' + pdf
    try:
        wget.download(url, out=out)
        # wget.download(url)
    except Exception as e:
        print(e)
    """
    
    mp3 = 'sg' + str(i) + '.mp3'
    # url = 'https://slowgerman.com/folgen/' + mp3
    url = 'https://cdn.podseed.org/slowgerman/' + mp3
    try:
        wget.download(url, out=out)
        # wget.download(url)
    except Exception as e:
        print(e)


"""
https://slowgerman.com/folgen/sg125kurz.pdf
https://slowgerman.com/folgen/sg125.mp3
https://cdn.podseed.org/slowgerman/sg214.mp3
"""