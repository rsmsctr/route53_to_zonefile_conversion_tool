#You don't need the SOA or NS Record when importing into Cloudflare. Since you will need to create the hosted zone within cloudflare anyways. Test zone file works


import boto3, json
from pprint import pprint

from dns import zone
from dns import name
from dns.rdataclass import IN
from dns.rdatatype import A, NS, MX, SOA, TXT


route53 = boto3.client('route53')
allzones = route53.list_hosted_zones().get('HostedZones')

#print(allzones)

for zone in allzones:
    print(zone.get('Name'))
    zoneid = zone.get('Id')
    print(zoneid)
    recordsetsresponse = route53.list_resource_record_sets(
    HostedZoneId = zoneid
    )
    recordsets = recordsetsresponse.get('ResourceRecordSets')
    recordnames = recordsets[0]
    #print(recordsets)
    #Gets the first record set of rsmtech.net (SOA)
    #print(recordnames)


#count = 2
#Gets 5th record set of rsmtech.net
#for records in recordsets:
    #print(recordsets[4])


#print(recordsets.get('ResourceRecordSets').get('Name'))



type(recordsets)
#pprint(recordsets)

#define and create the recordset list from the hosted zone

txtrecords = []
cnamerecords = []
soarecords = []
nsrecords = []
arecords = []
aaaarecords = []



for item in recordsets:
    if item.get('Type') == 'CNAME':
        #print(item)
        cnamerecords.append(item)
    if item.get('Type') == 'TXT':
        #print(item)
        txtrecords.append(item)
    if item.get('Type') == 'SOA':
        #print(item)
        soarecords.append(item)
    if item.get('Type') == 'NS':
        #print(item)
        nsrecords.append(item)
    if item.get('Type') == 'A':
        #print(item)
        arecords.append(item)
    if item.get('Type') == 'AAAA':
        #print(item)
        aaaarecords.append(item)


#NS Object Definitions and variable assignments


#ns = recordsets[0] # quick and dirty way of doing it for research purposes.......
#nsresourcerecords = ns.get('ResourceRecords')
#for record in nsresourcerecords:
    #print(record['Value'])

#Add CNAMES

#Add TXT Records

#Add A Records

#Add Types


#Make the file