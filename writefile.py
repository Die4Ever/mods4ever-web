#!/usr/bin/python3
import sys
import os
import json
import urllib.parse

def get_request():
    s_content_length = os.environ.get('CONTENT_LENGTH')
    if s_content_length is None:
        s_content_length = "0"
    else:
        s_content_length = str(s_content_length)

    content_length = int(s_content_length)
    content:str = ""
    data:bytes = b''

    try:
        #while len(args) < content_length AND (datetime.datetime.now() - now).total_seconds() < 10:
        if content_length > 0:
            data:bytes = sys.stdin.buffer.read()
            content = read_binary_content(data)
            content = content.replace('\x00','').replace('\r','')
    except Exception as e:
        print(e)

    ip = os.environ.get('REMOTE_ADDR')
    qps = query_params()
    return content, content_length, ip, qps

def read_binary_content(data:bytes) -> str:
    try:
        return data.decode('utf-8','ignore')
    except Exception as e:
        print(e)
        return data.decode('iso_8859_1','ignore')
    return data.decode()

def parse_query_string(q):
    d = {}
    for m in re.finditer(r'(([^=]+)=([^\&]+)&?)', q):
        d[m.group(2)] = m.group(3).replace("%20", " ")
    return d

def query_params():
    if os.environ.get('QUERY_STRING'):
        return parse_query_string(os.environ.get('QUERY_STRING'))
    return {}

def saveContentToFile(content):
    cleanContent = urllib.parse.unquote_plus(content)
    cleanContent = cleanContent.lstrip("bingo=")
    print(cleanContent)

    f = open("bingo.txt",'w')
    f.write(cleanContent)
    f.close()

def main():
    print("Status: 200")
    print("")

    content, content_length, ip, qps = get_request()

    saveContentToFile(content)

    #print("")
    #print(content)
    #print("")
    #print(content_length)
    #print("")
    response = {}
    if len(content) != content_length:
        response['status'] = "ERROR: only received "+str(len(content))+"/"+str(content_length)+" bytes"
    else:
        response['status'] = "ok received "+str(len(content))+"/"+str(content_length)+" bytes"

    print(json.dumps(response))

if __name__=='__main__':
    main()
