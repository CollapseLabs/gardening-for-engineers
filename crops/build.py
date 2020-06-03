import markdown_table
import yaml

import csv
from os import listdir
from pathlib import Path


in_dir_path = Path('data')
out_dir_path = Path('dist')
out_dir_path.mkdir()


localizable_strings = {}
with open(in_dir_path.joinpath('lang.csv')) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        key = row['Key']
        del(row['Key'])
        localizable_strings[key] = {k:[s.strip() for s in v.split(',')] for k,v in row.items() if v}

all_crops = []
fieldnames = []

for child_path in in_dir_path.iterdir():
    if child_path.name.endswith('yml') and not child_path.name.startswith('_'):
        with child_path.open() as f:
            s = f.read()
            crop = yaml.safe_load(s)

        common_name_key = crop['common_name_key']
        common_name_dict = localizable_strings[common_name_key]
        title = common_name_dict['en'][0].title()

        headers = ['Language', 'String']
        matrix = [[f'`{k}`',', '.join(v)] for k,v in common_name_dict.items()]
        common_names_md_table = markdown_table.render(headers,matrix)	
        del(crop['common_name_key'])

        headers = ['Key', 'Value']
        matrix = [[f'`{k}`', str(v)] for k,v in crop.items() if not k == 'title']
        crop_md_table = markdown_table.render(headers,matrix)	

        template_path = child_path.with_suffix('.md')
        try:
            with template_path.open() as template_file:
                s = template_file.read()
        except FileNotFoundError as e:
                s = ''
        s = f'# {title}\n\n## Common Names\n\n{common_names_md_table}\n\n\n## Data\n\n{crop_md_table}\n\n\n{s}'

        out_filename = Path(template_path.name)
        out_md_path = out_dir_path.joinpath(out_filename)
        print('Writing ' + str(out_md_path))
        with out_md_path.open('w') as outfile:
            outfile.write(s)

        all_crops.append(crop)
        [fieldnames.append(k) for k in crop.keys() if k not in fieldnames]


out_crops_csv = out_dir_path.joinpath('crops.csv')
print('Writing ' + str(out_crops_csv))
with out_crops_csv.open('w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for crop in all_crops:
        writer.writerow(crop)
