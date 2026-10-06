COUNTRIES={'ALB':'Albania','AUT':'Austria','BEL':'Belgium','BGR':'Bulgaria','BIH':'Bosnia and Herzegovina','CHE':'Switzerland','CYP':'Cyprus','CZE':'Czechia','DEU':'Germany','DNK':'Denmark','ESP':'Spain','EST':'Estonia','FIN':'Finland','FRA':'France','GBR':'United Kingdom','GRC':'Greece','HRV':'Croatia','HUN':'Hungary','IRL':'Ireland','ISL':'Iceland','ITA':'Italy','LIE':'Liechtenstein','LTU':'Lithuania','LUX':'Luxembourg','LVA':'Latvia','MDA':'Moldova','MKD':'North Macedonia','MLT':'Malta','MNE':'Montenegro','NLD':'Netherlands','NOR':'Norway','POL':'Poland','PRT':'Portugal','ROU':'Romania','SRB':'Serbia','SVK':'Slovakia','SVN':'Slovenia','SWE':'Sweden','UKR':'Ukraine'}
# No-auth connectors verified for this build.
def sources_for(countries):
 c=set(countries);out=[]
 eu=sorted(c-{'UKR'})
 if eu:out.append(('ted',eu))
 if 'UKR' in c:out.append(('prozorro',['UKR']))
 if 'DEU' in c:out.append(('germany',['DEU']))
 if 'POL' in c:out.append(('poland',['POL']))
 return out
