from taxii2client.v20 import Server, Collection
from stix2 import Filter, TAXIICollectionSource

collections = {
    'enterprise_attack': '95ecc380-afe9-11e4-9b6c-751b66dd541e',
    'pre_attack': '062767bd-02d2-4b72-84ba-56caef0f8658',
    'mobile_attack': '2f669986-b40b-4423-b720-4396ca6a462b',
    'ics_attack': '02c3ef24-9cd4-48f3-a99f-b74ce24f1d34'
    
}

server = Server('https://cti-taxii.mitre.org/taxii/')
api_root = server.api_roots[0]

print('Getting collection...')
collection = Collection(f'https://cti-taxii.mitre.org/stix/collections/{collections["enterprise_attack"]}/')
print('Collection received.')
src = TAXIICollectionSource(collection)
print('src created.')

# Print name and ID of all ATT&CK domains available as collections
# for collection in api_root.collections:
#     print(collection.title.ljust(20) + collection.id)

def get_technique_by_name(thesrc, name):
    filt = [
        Filter('type', '=', 'attack-pattern'),
        Filter('name', '=', name)
    ]
    return thesrc.query(filt)

print('Getting technique by name')
# get the technique titled 'System Information Discovery'
print(get_technique_by_name(src, 'System Information Discovery'))
