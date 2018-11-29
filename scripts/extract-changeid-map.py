import sys
import os
import json

import json_lines

output_file = 'output.jl'
if not os.path.exists(output_file):
    print('Did not find expected output file!')
    sys.exit(1)

change_id_to_change_number = {}
with open(output_file, 'rb') as fp:
    for item in json_lines.reader(fp):
        if 'ChangeIdToChangeNumber' in item:
            change_id_to_change_number.update(item['ChangeIdToChangeNumber'])


with open(os.path.join('mirror', 'ChangeIdToChangeNumber.json'), 'w') as fp:
    json.dump(change_id_to_change_number, fp)
