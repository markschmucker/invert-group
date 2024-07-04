from client506 import create_client


def process(group0_name, group1_name):
    client = create_client(1)
    # using members_of_group as it gets all and handles pagination
    all_users = client.members_of_group('trust_level_0')
    group0_users = client.members_of_group(group0_name)
    group1_users = client.members_of_group(group1_name)
    group0_user_ids = [u['id'] for u in group0_users]
    group1_user_ids = [u['id'] for u in group1_users]
    group0_id = client.group(group0_name)['group']['id']
    group1_id = client.group(group1_name)['group']['id']
    for u in all_users:
        if u['id'] in group0_user_ids:
            if u['id'] in group1_user_ids:
                client.delete_group_member(group1_id, u['id'])
        else:
            client.add_group_members(group1_id, [u['username']])


if __name__ == '__main__':
    process('RIA-excluded', 'RIA-included')
