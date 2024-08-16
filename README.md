# Route53 to Zonefile Conversion tool.

The creation of this tool was to automate a way to take all zones within route53 and convert them into usable BIND zone files. That way you could import them into any DNS provider that supports uploads. Amazon does not have a way to do this with it's boto3 toolkit. Nor do I think it's really a priority for them to create a tool that facilitates the ease of maneuverability away from their walled garden. 

# Things to note:

1) The script assumes that all DNS records / recordsets in Route53 are classified as `IN` records.
2) The script contains logic to create seperate rdata for `AAAA` and `A` records since the rdata for said records only support single cardinality from what I've gathered.
3) There is no logic for ordering rdata that support mutli-cardinality.
4) You need to create a profile on your home drive for the boto client to refer to, and adjust it within the script.
5) If the route53 record contains a subdomain that refers to an AWS resource, it will be filtered out and NOT applied to the BIND zone file. This includes all of its subdomains. The list at the end of the script will print list of these subdomains. 
6) The boto client will only return up to 300 recordsets for a single zone per request. You can add logic to make it continue if needed. 
7) The boto client will only return up to 100 zones per request. You can add logic to make it continue if needed.

# Resources:

https://groups.google.com/g/dnspython-users/c/-jivSPKIElo
https://agiletesting.blogspot.com/2005/08/managing-dns-zone-files-with-dnspython.html
https://dnspython.readthedocs.io/en/latest/manual.html
and my good bud gpt for the regex escape sequence function. 
