from groupy import Client
import pickle
import json

init_data = open("init_info.txt", "r").readlines()
api_token = init_data[0][:-1]
group_name = init_data[1]

print(api_token, group_name)


def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

client = Client.from_token(api_token)

groups = list(client.groups.list())
print(groups)
group_list = list(filter(lambda x: x.name == group_name, groups))
if len(group_list) == 0:
    print("Couldn't find a group by that name, sorry!")
    exit()

group = group_list[0]

id_to_member = {}
for member in group.members:
    id_to_member[member.user_id] = member.nickname

print(group)
print("Identified Group")

messages = list(group.messages.list_all())

print(messages)

people = {}

for message in messages:
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

print(f"Processed {len(messages)} Messages")
print(people)

save_obj(people, "people_data")
data_file = open("obj/additional_data.txt", 'w')
data_file.write(group_name + "\n")
data_file.write(json.dumps(id_to_member))
data_file.write("\n" + str(len(messages)))
data_file.write("\n" + str(messages[-1].id))
data_file.close()