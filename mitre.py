from taxii2client.v20 import Collection
from stix2 import Filter, TAXIICollectionSource, FileSystemSource
from stix2 import MemoryStore

IS_ONLINE = False


def get_technique_by_name(src, name):
    filt = [
        Filter('type', '=', 'attack-pattern'),
        Filter('name', '=', name)
    ]
    return src.query(filt)

def get_technique_by_external_id(src, _id):
    filt = [
        Filter('type', '=', 'attack-pattern'),
        Filter("external_references.external_id", "=", _id)
    ]

    return src.query(filt)


def get_technique_id(cti_src, technique):
    technique_id = technique[0]['id']
    return technique_id


def get_technique_name(cti_src, technique):
    technique_name = technique[0]['name']
    return technique_name


def get_related(src, src_type, rel_type, target_type, reverse=False):
    """build> relationship mappings
       params:
         src: MemoryStore to build relationship lookups for
         src_type: source type for the relationships, e.g "attack-pattern"
         rel_type: relationship type for the relationships, e.g "uses"
         target_type: target type for the relationship, e.g "intrusion-set"
         reverse: build reverse mapping of target to source
    """

    relationships = src.query([
        Filter('type', '=', 'relationship'),
        Filter('relationship_type', '=', rel_type)
    ])

    id_to_related = {}

    # build the dict
    for relationship in relationships:
        if src_type in relationship.source_ref and \
           target_type in relationship.target_ref:
            if (relationship.source_ref in id_to_related and not reverse) or\
               (relationship.target_ref in id_to_related and reverse):
                # append to existing entry
                if not reverse:
                    id_to_related[relationship.source_ref].append({
                        'relationship': relationship,
                        'id': relationship.target_ref
                    })
                else:
                    id_to_related[relationship.target_ref].append({
                        'relationship': relationship,
                        'id': relationship.source_ref
                    })
            else:
                # create a new entry
                if not reverse:
                    id_to_related[relationship.source_ref] = [{
                        'relationship': relationship,
                        'id': relationship.target_ref
                    }]
                else:
                    id_to_related[relationship.target_ref] = [{
                        'relationship': relationship,
                        'id': relationship.source_ref
                    }]
    # all objects of relevant type
    if not reverse:
        targets = src.query([
            Filter('type', '=', target_type),
            Filter('revoked', '=', False)
        ])
    else:
        targets = src.query([
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
            if not related['id'] in id_to_target:
                continue
            value.append({
                'object': id_to_target[related['id']],
                'relationship': related['relationship']
            })
        output[stix_id] = value
    return output


def groups_using_software(src):
    return get_related(src, 'intrusion-set', 'uses', 'tool', reverse=True) or \
        get_related(src, 'intrusion-set', 'uses', 'malware', reverse=True)


def get_groups_using_any_technique(src):
    return get_related(src, 'intrusion-set',
                       'uses', 'attack-pattern',
                       reverse=True)


def get_groups_using_technique(src, technique_id):
    all_groups = get_groups_using_any_technique(src)
    if technique_id in all_groups:
        return all_groups[technique_id]
    return None


def get_mitigations_for_any_technique(src):
    return get_related(src, "course-of-action",
                       "mitigates", "attack-pattern",
                       reverse=True)


def get_mitigations_for_technique(src, technique_id):
    all_mitigations = get_mitigations_for_any_technique(src)
    if technique_id in all_mitigations:
        return all_mitigations[technique_id]
    return None


def get_malware_for_any_technique(src):
    return get_related(src, "malware", "uses", "attack-pattern", reverse=True)


def get_malware_for_technique(src, technique_id):
    all_malware = get_malware_for_any_technique(src)
    if technique_id in all_malware:
        return all_malware[technique_id]
    return None


def get_tool_for_any_technique(src):
    return get_related(src, "tool", "uses", "attack-pattern", reverse=True)


def get_tool_for_technique(src, technique_id):
    all_tool = get_tool_for_any_technique(src)
    if technique_id in all_tool:
        return all_tool[technique_id]
    return None


def get_all_subtechniques(src):
    return get_related(src, "attack-pattern",
                       "subtechnique-of", "attack-pattern",
                       reverse=True)


def get_subtechnique_for_technique(src, technique_id):
    all_subs = get_all_subtechniques(src)
    if technique_id in all_subs:
        return all_subs[technique_id]
    return None


def setup_cti_source():
    if IS_ONLINE:
        collections = {
            'enterprise_attack': '95ecc380-afe9-11e4-9b6c-751b66dd541e',
            'pre_attack': '062767bd-02d2-4b72-84ba-56caef0f8658',
            'mobile_attack': '2f669986-b40b-4423-b720-4396ca6a462b',
            'ics_attack': '02c3ef24-9cd4-48f3-a99f-b74ce24f1d34'
        }

        print('Getting collection...')
        collection = Collection(f'https://cti-taxii.mitre.org/stix/collections/{collections["enterprise_attack"]}/')
        print('Collection received.')
        cti_src = TAXIICollectionSource(collection)
    else:
        cti_src = MemoryStore()
        cti_src.load_from_file('./cti/enterprise-attack/enterprise-attack.json')

    return cti_src


if __name__ == "__main__":
    cti_src = setup_cti_source()
