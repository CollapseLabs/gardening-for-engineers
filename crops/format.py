import markdown_table
import yaml

import csv
from os import listdir
from pathlib import Path

all_crops = []
fieldnames = []

dir_path = Path('data')
for child_path in dir_path.iterdir():
    if child_path.name.endswith('yml') and not child_path.name.startswith('_'):
        with child_path.open() as f:
            s = f.read()
            crop = yaml.safe_load(s)

        title = crop['title']

        headers = ['Language', 'String']
        matrix = [[f'`{k}`',v] for k,v in crop['common_names'].items()]
        common_names_md_table = markdown_table.render(headers,matrix)	
        del(crop['common_names'])

        headers = ['Key', 'Value']
        matrix = [[f'`{k}`', str(v)] for k,v in crop.items() if not k == 'title']
        crop_md_table = markdown_table.render(headers,matrix)	

        template_path = child_path.with_suffix('.md')
        with template_path.open() as template_file:
            s = template_file.read()
            s = f'# {title}\n\n## Common Names\n\n{common_names_md_table}\n\n\n## Data\n\n{crop_md_table}\n\n\n{s}'

        out_filename = Path(template_path.name)
        print('Writing ' + str(out_filename))
        with out_filename.open('w') as outfile:
            outfile.write(s)

        all_crops.append(crop)
        [fieldnames.append(k) for k in crop.keys() if k not in fieldnames]

out_filename = 'crops.csv'
print('Writing ' + out_filename)
with open(out_filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for crop in all_crops:
        writer.writerow(crop)
