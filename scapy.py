import requests
import base64
import re
import sys
import urllib.parse as urlparse
from lxml import etree

scheme = {
    'png': 'data:image/png;base64,',
    'gif': 'data:image/gif;base64,',
    'jpeg': 'data:image/jpeg;base64,',
    'icon': 'data:image/x-icon;base64,',
    'svg': 'data:image/svg;base64',
    'jpg': 'data:image/jpg;base64'
}

def get_img_content(a_src):
    img_content = requests.Session().get(url=a_src).content
    base64_img_content = base64.b64encode(img_content)
    return base64_img_content.decode('utf-8')

def convert_to_base64(content_without_script, img_src_list, img_datasrc_list, host):
    for src in img_src_list:
        if src == '':
            continue
        elif src.startswith('//'):
            a_src = 'http:' + src
        elif src.startswith(host):
            a_src = 'http://' + src
        elif src.startswith("http"):
            a_src = src
        else:
            a_src = 'http://' + host + src
        suffix = a_src.rsplit('.', 1)[1]
        if suffix in scheme.keys():
            a_scheme = scheme[suffix]
        else:
            #print(a_src)
            parse = urlparse.urlparse(a_src)
            try:
                query = parse.query.split('=')[1]
            except:
                query = ''
            if '.' in parse.path:
                print(src,end='\n')
                img_type = parse.path.rsplit('.',1)[1]
#if img_type not in scheme:
#                   img_type = 'png'
            else:
                img_type = 'png'
            suffix = img_type if query not in scheme else query
            a_scheme = scheme[suffix]
        base64_content = get_img_content(a_src)
        new_src = "{scheme}{base64}".format(scheme=a_scheme, base64=base64_content)
        content_without_script = content_without_script.replace(src, new_src)

    for src in img_datasrc_list:
        if src == '':
            continue
        elif src.startswith('//'):
            a_src = 'http:' + src
        else:
            a_src = src
        suffix = a_src.rsplit('.', 1)[1]
        if suffix in scheme.keys():
            a_scheme = scheme[suffix]
        else:
            query = urlparse.urlparse(a_src).query
            suffix = query.split('=')[1]
            a_scheme = scheme[suffix]

        base64_content = get_img_content(a_src)
        new_src = "{scheme}{base64}".format(scheme=a_scheme, base64=base64_content)
        content_without_script = content_without_script.replace(src, new_src)
    content_with_base64 = content_without_script.replace('data-src','src')
    return content_with_base64

def main(url):
    fetch = requests.Session()
    resp = fetch.get(url=url)
    content = resp.content.decode('utf-8')

    pattern = re.compile(r'<script.*?>.*?</script>')
    content_without_script = re.sub(pattern, '', content)

    root = etree.HTML(content_without_script)
    #title = root.xpath('.//title/text()')[0].strip()
    title = urlparse.urlparse(url).netloc

    img_src_list = root.xpath('.//img/@src')
    img_datasrc_list = root.xpath('.//img/@data-src')

    content_with_base64 = convert_to_base64(content_without_script, img_src_list, img_datasrc_list, title)
    
    with open("{title}.html".format(title=title), "w") as f:
        print("Outputing...{title}".format(title=title))
        f.write(content_with_base64)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: {sys} url'.format(sys=sys.argv[0]))
        exit(-1)
    url = sys.argv[1]
    main(url)
