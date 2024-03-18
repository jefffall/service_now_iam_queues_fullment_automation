#==============
# First program to run
#==============
 
import requests
import json
 
snow_queues = ["MA-ASGN-CIS-IAM","MA-ASGN-CIS-IAM-UNIX","MA-ASGN-CIS-IAM-WINDOWS","MA-ASGN-CIS-IAM-SOFTLAYER","MA-ASGN-CIS-IAM-QMX"]
          
def pull_assigned_to_user(url):
    if "3ac138cbdb8df30001869476db96191b" in url:
        return "I.BABY.PRASHANTHI.Pudota@kyndryl.com"
    elif "f2c138cbdb8df30001869476db961910" in url:
        return "Suresh.Raju@kyndryl.com"
    elif "f6c138cbdb8df30001869476db96190c" in url:
        return "ithyavathi.Karunagaran@kyndryl.com"
    elif "76c138cbdb8df30001869476db961929" in url:
        return "Praveen.Ratnam@kyndryl.com"
    elif "32c138cbdb8df30001869476db961914" in url:
        return "Adinarayana.Medishetty@kyndryl.com"
    elif "a2c1f4cbdb8df30001869476db9619da" in url:
        return "Karthikeyan.Ramasubbu@kyndryl.com"
    elif "db8aec4b1b2838d031516243604bcbde" in url:
        return "Wilson.Cheatham@kyndryl.com"
    elif "acf078b11b4178508d1dc9d0604bcbb9" in url:
        return "Jeffrey.Fall@kndryl.com"
    elif "d0e1340fdb8df30001869476db961928" in url:
        return "ucastroj@kyndryl.com"
    elif "5ac1f4cbdb8df30001869476db96196d" in url:
        return "Harish.Dhatrik@kyndryl.com"
    elif "24e1340fdb8df30001869476db9619ef" in url:
        return "Senthil.D.S@kyndryl.com"
    elif "f5b13c8bdb8df30001869476db9619e3" in url:
        return "Saraswati.Sridhar@kyndryl.com"
    elif "d48694091b108dd0204965f0b24bcb4e" in url:
        return "talluri.jayasri@kyndryl.com"
    elif "fcd1a975dba55cd0883d06e2ca961944" in url:
        return "Suchita.Khedekar@kyndryl.com"
    elif "0029a9531bcfc9900177c998624bcb2f" in url:
        return "Joern.Martin.Vogt@kyndryl.com"
    elif "bac1f4cbdb8df30001869476db9619fe" in url:
        return "Bill.Keen@kyndryl.com"
    else:
        print ("This user is not cached: ",url)
        user = 'kyndryl_iam'
        pwd = 'H1eGHfLyCL0ud$'
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        
        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers )
        
        if response.status_code != 200: 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()
        
        myresponse = response.content.decode('utf-8')
        mydict = json.loads(myresponse)
        print ("Please add this user to the static cache -> ",mydict['result']['user_name'])
        exit(0)
 
def remove_excess_double_quotes(line):
    collect = ""
    linelen = len(line)
    for x in range(0,linelen):
        if line[x] == '"':
            if line[x+1] == "," or line[x+1] == "}" or  line[x+1] == '"' or line[x+1] == ':' or line[x+1] == ': ' or line[x-1] == "{" or (line[x-1] == " " and line[x-2] == ",") or (line[x-1] == " " and line[x-2] == ":"):
                collect = collect + (line[x])
            else:
                pass
        else:
            collect = collect + (line[x])
    return collect
 
def fix_double_quotes_in_descriptions(line):
    '''
    # this is the problem string: Full Access"",
    # this is permitted: ': "",'
    '''
    line = str(line)
    new_string = ""
    mylen = len(line)
    for x in range(0,mylen):
        if line[x] == '"' and line[x+1] == '"':
            if line[x-2] == ":" and line[x-1] == " ":
                new_string = new_string + line[x]
            else:
                x = x + 1
        else:
            new_string = new_string + line[x]
    try:
        mydict = json.loads(new_string)
    except:
        print ("Original line:")
        print (line)
        print ("ERROR LINE is below:")
        print(new_string)
        mydict = False
    return mydict
 
def get_snow_queue(queue):
    url = 'https://kyndrylcsm.service-now.com/api/now/table/sn_customerservice_case?&sysparm_order=sys_created_on &sysparm_order_direction=desc&sysparm_query=sys_created_onONLast%20hour@javascript:gs.hoursAgoStart(336)@javascript:gs.hoursAgoEnd(0)&assignment_group='+str(queue)
 
    user = 'kyndryl_iam'
    pwd = 'H1eGHfLyCL0ud$'
        
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
        
    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )
        
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit(0)
    # Decode the JSON response into a dictionary and use the data
    json_data = response.json()
    
    # assign queue`
    for line in json_data['result']:
        line['queue']= queue
    return json_data
     
def fix_noise_in_line(line):
    line = str(line)
   
    line = line.replace("'","\"",1000)
    
    line = str(line).replace("u_","").strip()
    line = line.replace("'","\"")
    line = line.replace("\\","",200)
    line = line.replace("u200b","",200)
    line = line.replace('AddOnly Error: {','", "')
    line = line.replace(' } { ','", "')
    try:
        line = json.loads(line)
    except:
        try:
            line = remove_excess_double_quotes(line)
        except:
            try:
                myresult = fix_double_quotes_in_descriptions(line)
                if myresult != False:
                    line = myresult
                else:
                    print ("Fix double quotes in description failed")
                    exit (0)
            except:
                print ("fix_double_quotes_in_descriptions failed")
    return line
   
 
def scan_tickets_for_user_links(json_data):
    for line in json_data['result']:
        mytemp = line['assigned_to']
        #print (str(type(mytemp)))
        if str(type(mytemp)) == "<class 'dict'>":
            #print (mytemp['link'])
            user_name = pull_assigned_to_user(mytemp['link'])
            #print (user_name)
            line['assigned_to'] = user_name
        else:
            line['assigned_to'] = 'not assigned...'
            
'''
#################################################################################################
MAIN
#################################################################################################
'''
            
myfp = open('/Users/jfall/tickets_json.txt', 'w')  
                     
ticket_count = 0  
         
for queue in snow_queues:
    print ("Processing Queue: ",queue)
    print(" ")
    json_result = get_snow_queue(queue)
    
    scan_tickets_for_user_links(json_result)
 
    
    per_queue_ticket_count = 0
    print ("------ top --------")
    for line in json_result['result']:
        per_queue_ticket_count = per_queue_ticket_count + 1
        ticket_count = ticket_count + 1
        print("QUEUE: ",queue,"Ticket: ",per_queue_ticket_count)
        line = fix_noise_in_line(line)
        #print (str(line)) # <<------ !!!!
        myfp.write(str(line)+"\n")
    print(" ")         
myfp.close()
 
print ("Done processing all known Softlayer ticket queues...")
print (" ")
print ("Now run 'read from disk' program to process JSON entries gathered for ", ticket_count," tickets")
        
 
