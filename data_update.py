from groupy import Client
import pickle
import json

def get_name_from_member_id(id, id_to_member, stats):
    if id in id_to_member:
        return id_to_member[id]
    return f"Removed Member: {stats}"

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def load_rest(name):
    with open('obj/' + name + '.txt', 'rb') as f:
        file_text = f.readlines()
        json_dt = json.loads(file_text[1])
        return file_text[0].decode("utf-8")[:-1], json_dt, file_text[2], file_text[3]

people = load_obj("people_data")
group_name, id_to_member, total_messages, last_message_id = load_rest("additional_data")


init_data = open("init_info.txt", "r").readlines()
api_token = init_data[0][:-1]
client = Client.from_token(api_token)
groups = list(client.groups.list())
print(groups)
group_list = list(filter(lambda x: x.name == group_name, groups))
if len(group_list) == 0:
    print("Couldn't find a group by that name, sorry!")
    exit()

group = group_list[0]

print(type(group))
messages_to_update = list(group.messages.list_since(last_message_id))

print(messages_to_update)

for message in messages_to_update:
    person = message.user_id
    if not message.name == "GroupMe":
        like_list = message.favorited_by
        if person in like_list:
            like_list.remove(person)
        likes = len(like_list)
        if not person in people:
            people[person] = (0,0,set([]))
        s = people[person][2]
        s.add(message.name)
        people[person] =  (people[person][0] + likes, people[person][1]+1, s)

save_obj(people, "people_data")
data_file = open("obj/additional_data.txt", 'w')
data_file.write(group_name + "\n")
data_file.write(json.dumps(id_to_member))
data_file.write("\n" + str(int(total_messages) + len(messages_to_update)))
data_file.write("\n" + str(messages_to_update[-1].id))
print("Saved data to files")