import boto3
import dns.rdata
import dns.rdataclass
import dns.rdatatype
import dns.tokenizer
import dns.zone
import dns.rdataset
import dns.rrset
import os.path
from dns import zone
from dns.rdatatype import *
import re

#Function to convert the escape sequences returned from AWS into the correct characters. I guess for some reason the codes returned by AWS are escaped resulting in misinterpretation. Also I found threads indicating that this has been a known bug since 2017.
def convert_escaped_string(escaped_string):
    def replace_escape(match):
        code = int(match.group(1), 8)
        return chr(code)
    pattern = re.compile(r'\\(\d{3})')
    converted_string = pattern.sub(replace_escape, escaped_string)
    return converted_string

#Connect to Route 53 And establish a list of Zones and their Information

boto3.setup_default_session(profile_name='your-aws-profile-name')
route53 = boto3.client('route53')

zonesresponses = (route53.list_hosted_zones()).get('HostedZones')
zoneids = [zoneid['Id'] for zoneid in zonesresponses]

#A list of all domains/subdomains that have been excluded due to the record being associated with an AWS Alias Target

Subdomainsomitted = []


#Iterate through each zone, get the aws recordsets, and turn it into a zonefile

for zoneid in zoneids:

    recordsetsresponse = route53.list_resource_record_sets(
        HostedZoneId = zoneid,
        MaxItems = "300"
    )

    recordsets = recordsetsresponse.get('ResourceRecordSets')

    sourcezone = route53.get_hosted_zone(
        Id= zoneid
    )

    sourcezonename = ((sourcezone.get('HostedZone')).get('Name'))

    #Build Zone Object with rdata and rdatasets from AWS recordsets. Skips NS and SOA records. Also removes any records that contains the attribute 'AliasTarget' which is only assigned to records that are targeting AWS Resources.
    
    zone = dns.zone.Zone(dns.name.from_text(sourcezonename))

    for record in recordsets:
        if record['Type'] == 'NS':
            recordsets.remove(record)
        elif record['Type'] == 'SOA':
            recordsets.remove(record)
        elif 'AliasTarget' in record or record['TTL'] == '':
            Subdomainsomitted.append(record['Name'])
            recordsets.remove(record)
            continue
        else:
            list_of_values = record.get('ResourceRecords')
            name = record.get('Name')
            converted_string = convert_escaped_string(name)
            values = [value['Value'] for value in list_of_values]
            if len(values) > 1 and record['Type'] == 'A' or record['Type'] == 'AAAA':
                for value in values:
                    tokenizer = dns.tokenizer.Tokenizer(value)
                    rdata = dns.rdata.from_text('IN', record.get('Type'), tokenizer)
                    rdataset = zone.find_rdataset(converted_string,rdata.rdtype,create=True)
                    rdataset.add(rdata,ttl=record.get('TTL'))
                continue
            tokens = ''.join(values)
            tokenizer = dns.tokenizer.Tokenizer(tokens)
            rdata = dns.rdata.from_text('IN', record.get('Type'), tokenizer)
            rdataset = zone.find_rdataset(converted_string,rdata.rdtype,create=True)
            rdataset.add(rdata,ttl=record.get('TTL'))


    #Create The Zone File

    save_path = 'C:/zonefiles'
    file_name = sourcezonename

    dazonefile = zone.to_file((os.path.join(save_path,file_name+"txt")),want_origin=True)

print('These subdomains have been omitted from the zone files. They are using AWS resource alias\'s and cannot be transferred. If other subdomains exist under these, they will be omitted as well:')
for subdomainomitted in Subdomainsomitted:
    print(subdomainomitted)
