#!/usr/bin/env python3
import sys
import json


def get_vulnerabilities(name, db):
	if hasattr(db, "read"):
		data = json.load(db)
	elif isinstance(db, str):
		data = json.loads(db)
	else:
		raise TypeError("db must be file-like object or JSON string")

	vulns = []

	if name in data:
		for vuln in data[name]:
			vuln_id = vuln.get("id", "")
			versions = vuln.get("v", [])
			# 确保 versions 是列表，然后拼接成字符串
			if isinstance(versions, list):
				version_str = ",".join(versions)
			else:
				version_str = versions or ""
			cveid = vuln.get("cve", None)
			vulns.append((vuln_id, version_str, cveid))

	return vulns


def main(argv):
	name = sys.argv[1]
	db = open(sys.argv[2])
	vulnerabilities = get_vulnerabilities(name, db)
	for v in vulnerabilities:
		print('%s; %s; %s' % (v[0], v[1], v[2]))


# This makes sure the main function is not called immediatedly
# when TMC imports this module
if __name__ == "__main__": 
	if len(sys.argv) != 3:
		print('usage: python %s name db' % sys.argv[0])
	else:
		main(sys.argv)
