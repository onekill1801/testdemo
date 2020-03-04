import sys
# Importing the JSON module
import json
# Importing the different stix2 modules
from stix2 import MemoryStore
from stix2 import Vulnerability
from stix2 import Bundle
from stix2 import Identity
from stix2 import ExternalReference


def convert(parse_data, output='output.json'):
	# Create the default author
	author = Identity(name='The MS Bulletin Corporation', identity_class='organization')
	print(author)
	count = 0

	vulnerabilities_bundle = [author]
	# Getting modified date
	mdate = parse_data["rss"]["channel"]["lastBuildDate"]
	for msb in parse_data["rss"]["channel"]["item"]:
		count += 1
		# Get the name
		name = msb["title"]
		# Getting the create date
		cdate = msb["pubDate"]
		# Getting description
		description = msb["description"]
		 # Create external references
		external_references = ExternalReference(
			source_name="Microsoft Security Bulletin",
			url=msb["link"]
		)
		# Creating the vulnerability with the extracted fields
		vuln = Vulnerability(
			name=name,
			created=cdate,
			modified=mdate,
			description=description,
			created_by_ref=author,
			external_references=external_references
        )
        # Adding the vulnerability to the list of vulnerabilities
		vulnerabilities_bundle.append(vuln)
	# Creating the bundle from the list of vulnerabilities
	bundle = Bundle(vulnerabilities_bundle)
	# Creating a MemoryStore object from the bundle
	memorystore = MemoryStore(bundle)
	# Dumping this object to a file
	memorystore.save_to_file(output)

	print("Successfully converted " + str(count) + " vulnerabilities")

if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2])
