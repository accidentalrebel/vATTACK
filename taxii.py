from taxii2client.v20 import Server, Collection
from stix2 import Filter, TAXIICollectionSource, FileSystemSource

IS_ONLINE = False

if IS_ONLINE:
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
else:
    src = FileSystemSource('./cti/enterprise-attack')

# Print name and ID of all ATT&CK domains available as collections
# for collection in api_root.collections:
#     print(collection.title.ljust(20) + collection.id)

def get_technique_by_name(thesrc, name):
    filt = [
        Filter('type', '=', 'attack-pattern'),
        Filter('name', '=', name)
    ]
    return thesrc.query(filt)

def get_related(thesrc, src_type, rel_type, target_type, reverse=False):
    """build relationship mappings
       params:
         thesrc: MemoryStore to build relationship lookups for
         src_type: source type for the relationships, e.g "attack-pattern"
         rel_type: relationship type for the relationships, e.g "uses"
         target_type: target type for the relationship, e.g "intrusion-set"
         reverse: build reverse mapping of target to source
    """

    relationships = thesrc.query([
        Filter('type', '=', 'relationship'),
        Filter('relationship_type', '=', rel_type)
    ])

    # stix_id => [ { relationship, related_object_id } for each related object ]
    id_to_related = {} 

    # build the dict
    for relationship in relationships:
        if (src_type in relationship.source_ref and target_type in relationship.target_ref):
            if (relationship.source_ref in id_to_related and not reverse) or (relationship.target_ref in id_to_related and reverse):
                # append to existing entry
                if not reverse: 
                    id_to_related[relationship.source_ref].append({
                        "relationship": relationship,
                        "id": relationship.target_ref
                    })
                else: 
                    id_to_related[relationship.target_ref].append({
                        "relationship": relationship, 
                        "id": relationship.source_ref
                    })
            else: 
                # create a new entry
                if not reverse: 
                    id_to_related[relationship.source_ref] = [{
                        "relationship": relationship, 
                        "id": relationship.target_ref
                    }]
                else:
                    id_to_related[relationship.target_ref] = [{
                        "relationship": relationship, 
                        "id": relationship.source_ref
                    }]
    # all objects of relevant type
    if not reverse:
        targets = thesrc.query([
            Filter('type', '=', target_type),
            Filter('revoked', '=', False)
        ])
    else:
        targets = thesrc.query([
            Filter('type', '=', src_type),
            Filter('revoked', '=', False)
        ])

    # build lookup of stixID to stix object
    id_to_target = {}
    for target in targets:
        id_to_target[target.id] = target

    # build final output mappings
    output = {}
    for stix_id in id_to_related:
        value = []
        for related in id_to_related[stix_id]:
            if not related["id"] in id_to_target:
                continue # targeting a revoked object
            value.append({
                "object": id_to_target[related["id"]],
                "relationship": related["relationship"]
            })
        output[stix_id] = value
    return output

def groups_using_software(thesrc):
    """returns software_id => {group, relationship} for each group using the software."""
    return get_related(thesrc, "intrusion-set", "uses", "tool", reverse=True) | get_related(thesrc, "intrusion-set", "uses", "malware", reverse=True)

def groups_using_technique(thesrc):
    """returns technique_id => {group, relationship} for each group using the technique."""
    return get_related(thesrc, "intrusion-set", "uses", "attack-pattern", reverse=True)

print('Getting technique by name')

# get the technique titled 'System Information Discovery'
technique = get_technique_by_name(src, 'System Information Discovery')
print(str(technique))

all_groups = groups_using_technique(src)
groups = all_groups[technique[0]['id']]

for g in groups:
    print('>>')
    print(str(g['object']['name']))
    print(str(g['relationship']['source_ref'] + " " + g['relationship']['relationship_type']) + " " + g['relationship']['target_ref'])
    print('\n')