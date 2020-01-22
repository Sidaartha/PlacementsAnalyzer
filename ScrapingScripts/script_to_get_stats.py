import csv
import json
import collections

def load_json(filename):
	with open(filename, 'r') as f:
		return json.load(f)

def csv_to_dict(file_path):
	object_list = []
	with open(file_path) as f:
		for row in csv.DictReader(f, skipinitialspace=True):
			object_dict = {}
			for key, val in row.items():
				if val.isdigit() and key not in ['jnf_str']:
					object_dict[key] = int(val)
				else:
					object_dict[key] = val
			object_list.append(object_dict)
	return object_list

file_path = ['../DataJSON/companies.json', '../DataJSON/profiles.json', '../DataJSON/departments.json', '../DataJSON/days.json', '../DataJSON/locations.json', '../DataJSON/packages.json', '../DataJSON/sectors.json', '../DataJSON/students.json', 'OutputFiles/placements.csv', 'OutputFiles/placements_companies.csv']

companies = load_json(file_path[0])
profiles = load_json(file_path[1])
departments = load_json(file_path[2])
days = load_json(file_path[3])
locations = load_json(file_path[4])
packages = load_json(file_path[5])
sectors = load_json(file_path[6])
students = load_json(file_path[7])
placements_students = csv_to_dict(file_path[8])
placements_companies = csv_to_dict(file_path[9])

offers=0
startups=0
mncs=0
stu_dict_o = {}
students_list = []
for key, val in companies.items():
	offers += len(val['students'])
	stu_dict_o[val["com_id"]] = [val["com_id"], val["company"], len(val['students'])]
	if val["category"]== "\nStartUp\n":
		startups+=1
	elif val["category"].split(',')[0]== "\nMNC\n":
		mncs+=1
	for stu in val['students']:
		students_list.append(stu['roll_no'])

print("Offers: {0}".format(offers))
print("Placed: {0}".format(len(list(set(students_list)))))
print("Companies: {0}".format(len(companies.keys())))
print("Startups: {0}".format(startups))
print("MNC: {0}".format(mncs))
print("Locations: {0}".format(len(locations.keys())))
print("Sectors: {0}".format(len(sectors.keys())))

profiles_count=0
for key1, val1 in profiles.items():
	profiles_count+=len(val1.keys())
print("Profiles: {0}".format(profiles_count))

base_list = []
ctc_list = []
ctc_list_domestic = []
ctc_list_abroad = []
base_list_domestic = []
base_list_abroad = []
base_dict = {}
ctc_dict = {}
international=0
for key1, val1 in companies.items():
	for val2 in val1['students']:
		dep = val2['roll_no'][2:4].upper()
		yr = int(val2['roll_no'][0:2])
		com_id = str(val1['com_id'])
		jnf_id = str(val2['jnf_ids'][0])
		currency = profiles[com_id][jnf_id]['currency']
		if currency == 'USD':
			international+=1
			multi_factor = 70.0
			# multi_factor = 0
		elif currency == 'JPY':
			international+=1
			multi_factor = 0.64
			# multi_factor = 0
		else:
			multi_factor = 1
		if yr:
			base_list.append(float(profiles[com_id][jnf_id]['base'])*multi_factor)
			ctc_list.append(float(profiles[com_id][jnf_id]['ctc'])*multi_factor)
			if dep in base_dict:
				base_dict[dep].append(float(profiles[com_id][jnf_id]['base'])*multi_factor)
				ctc_dict[dep].append(float(profiles[com_id][jnf_id]['ctc'])*multi_factor)
			else:
				base_dict[dep] = [float(profiles[com_id][jnf_id]['base'])*multi_factor]
				ctc_dict[dep] = [float(profiles[com_id][jnf_id]['ctc'])*multi_factor]
			if currency in ['USD', 'JPY']:
				ctc_list_abroad.append(ctc_list[-1])
				base_list_abroad.append(base_list[-1])
			else:
				ctc_list_domestic.append(ctc_list[-1])
				base_list_domestic.append(base_list[-1])

dep_keys = base_dict.keys()
dep_keys.sort() 

print("International: {0}".format(international))
print("Max CTC domestic: {0}".format(max(ctc_list_domestic)))
print("Max CTC abroad: {0}".format(max(ctc_list_abroad)))
print("Max Base domestic: {0}".format(max(base_list_domestic)))
print("Max Base abroad: {0}".format(max(base_list_abroad)))

for dep in dep_keys:
	print("{0} \tBase: {1} \tCTC: {2} \tStudents: {3}".format(dep, round(sum(base_dict[dep])/len(base_dict[dep]), 1), round(sum(ctc_dict[dep])/len(ctc_dict[dep]), 1), len(ctc_dict[dep])))

print("Avg base: {0}".format(sum(base_list)/len(base_list)))
print("Avg ctc: {0}".format(sum(ctc_list)/len(ctc_list)))
base_list = [int(i) for i in base_list]
ctc_list = [int(i) for i in ctc_list]
print(collections.Counter(base_list), collections.Counter(ctc_list))
print("Mode base: {0}".format([max(set(base_list), key=base_list.count)][0]))
print("Mode ctc: {0}".format([max(set(ctc_list), key=ctc_list.count)][0]))