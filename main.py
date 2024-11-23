from client506 import create_client
from ses import send_simple_email
import traceback
from time import sleep


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

    added = []
    removed = []

    # Change memberships only when necessary, so we can log changes
    for u in all_users:
        # If user is in group0 and group1, remove user from group1
        if u['id'] in group0_user_ids:
            if u['id'] in group1_user_ids:
                client.delete_group_member(group1_id, u['id'])
                removed.append(u['username'])
        # If user is not in group0 and not yet in group1, add user to group1.
        else:
            if not u['id'] in group1_user_ids:
                client.add_user_to_group(group1_id, u['id'])
                added.append(u['username'])
        sleep(1)

    sep = '<br>'
    subject = '%s %s report' % (group0_name, group1_name)
    text = 'Added to %s:%s' % (group1_name, sep)
    if added:
        text += sep.join(added)
    else:
        text += '[none]'
    text += sep
    text += sep
    text += 'Removed from %s:%s' % (group1_name, sep)
    if removed:
        text += sep.join(removed)
    else:
        text += '[none]'
    send_simple_email('markschmucker@yahoo.com', subject, text)
    send_simple_email('support@506investorgroup.com', subject, text)


if __name__ == '__main__':
    try:
        process('RIA-excluded', 'RIA-included')
    except Exception, exc:
        print exc
        send_simple_email('markschmucker@yahoo.com', 'Error in RIA-excluded RIA-included script', traceback.format_exc())
        send_simple_email('support@506investorgroup.com', 'Error in RIA-excluded RIA-included script', traceback.format_exc())

