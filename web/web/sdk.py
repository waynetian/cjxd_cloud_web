#coding=utf-8
import httplib, urllib, json, logging
import settings

API = settings.OPEN_SERVER
PORT = settings.OPEN_PORT
TIMEOUT = settings.TIMEOUT
log_sdk = logging.getLogger('sdk')
TIMEOUT = 3600



def process_response(response):
    status = response.status
    data = response.read()
    log_sdk.info("rsp status=%s\tdata=%s" %(status, data))
    if status < 300:
        return json.loads(data)
    else:
        return None



def process_request(url, kwargs, method):
    response = None
    headers = {"Accept": "*/*", \
         "Content-type": "application/x-www-form-urlencoded",}
    conn =httplib.HTTPConnection(API,PORT, timeout=TIMEOUT)
    conn.set_debuglevel(1)
    if method in ('POST', "PUT"):
        params = urllib.urlencode(kwargs)
        #params = urllib.unquote(params)
        log_sdk.info("req method=%s\turl=%s\tparams=%s\theaders=%s" \
                    %(method, url, params, headers))
        conn.request(method, url, params, headers)
        response = conn.getresponse()
    elif method in ("GET", "DELETE"):
        log_sdk.info("req method=%s\turl=%s\theaders=%s" \
                    %(method, url, headers))
        conn.request(method, url, headers=headers)
        response = conn.getresponse()

    conn.close()
    return response

def ProcessMethod(method):
    def _deco(func):
        def __deco(*args, **kwargs):
            url = func(*args, **kwargs)
            response = process_request(url, kwargs, method)
            return process_response(response)
        return __deco
    return _deco



class APIServer:
    
    @classmethod
    @ProcessMethod("POST")
    def create_user(*args, **kwargs):
        return  '/user/' 

    @classmethod
    @ProcessMethod("GET")
    def retrieve_user(*args, **kwargs):
        obj, pk = args
        return  '/user/%s/' %pk
    
    @classmethod
    @ProcessMethod("POST")
    def create_org(*args, **kwargs):
        return  '/organization/' 

    @classmethod
    @ProcessMethod("DELETE")
    def delete_org(*args, **kwargs):
        obj, pk = args
        return  '/organization/%s/' %pk 
    
    @classmethod
    @ProcessMethod("PUT")
    def update_org(*args, **kwargs):
        obj, pk = args
        return  '/organization/%s/' %pk 
    
    @classmethod
    @ProcessMethod("GET")
    def retrieve_organization_set(*args, **kwargs):
        obj, pk = args
        return  '/organization/?org_id=%s' %pk


    @classmethod
    @ProcessMethod("POST")
    def create_orguser(*args, **kwargs): 
        return  '/orguser/' 

    @classmethod
    @ProcessMethod("DELETE")
    def delete_orguser(*args, **kwargs): 
        obj, pk = args
        return  '/orguser/%s/' %pk
    
    @classmethod
    @ProcessMethod("PUT")
    def update_orguser(*args, **kwargs): 
        obj, pk = args
        return  '/orguser/%s/' %pk

    
    @classmethod
    @ProcessMethod("GET")
    def retrieve_orguser_set(*args, **kwargs):
        obj, pk = args
        return  '/orguser/?org_id=%s' %pk

    @classmethod 
    @ProcessMethod('GET')
    def user_login(*args, **kwargs):
        obj, email, password = args
        return "/auth/?email=%s&password=%s" %(email, password)

    @classmethod 
    @ProcessMethod('POST')
    def create_multi_orguser(*args, **kwargs):
        return "/multi_orguser/" 



if __name__ == '__main__':
    #org_map = {'/name/123':{'name':'abc', 'short_name':'a', 'type':1},'/name/123/ddd':{'name':'abc1', 'short_name':'1', 'type':1}} 
    #domain_id = 54
    #domain_name = 'name'
    #import json
    #org_map_data = json.dumps(org_map) 

    import csv
    #'''
    reader = csv.reader(file('tb_dept.csv', 'rb'))
    org_map = {}

    for line in reader:
        name = line[2]
        short_name = line[3]
        path = line[7]
        type = int(line[8])
        print name, short_name, path, type

        org_map[path] = {'name':name, 'short_name':short_name, 'type':type}
    #''' 
    orguser_list = [] 
    reader = csv.reader(file('tb_user.csv', 'rb'))
    for q in reader:
        i = { 'user_name': q[4], 'email': q[17]\
        , 'mobile_number': q[19]\
        , 'id_number': ''\
        , 'path': q[14]\
        , 'job_title': q[15]\
        , 'job_type': 0\
        , 'role_id': 0\
        }
        orguser_list.append(i)
    print orguser_list

    import json
    orguser_list_data = json.dumps(orguser_list) 
    orguser_list_data1 = json.loads(orguser_list_data) 


    org_map_data = json.dumps(org_map) 


    domain_id = 54
    domain_name = '长江设计院'

    
    result = APIServer.create_multi_orguser( \
                    domain_id=domain_id, \
                    domain_name= domain_name, \
                    org_map=org_map_data, \
                    orguser_list=orguser_list_data)
    print result
     
