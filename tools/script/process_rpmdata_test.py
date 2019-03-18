# Copyright 2019 Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tools.convert import CsvConverter
from tools.script.create_rpm_data_test_data import expected_output
from tools.script.process_rpmdata import main


def gen_input(tmpdir, rpmdata):
    p = tmpdir.join('rpmdata.json')
    p.write(rpmdata)
    return str(p)


def test_no_output(tmpdir):
    main(['--rpmdata-path', gen_input(tmpdir, {})])


def test_components(tmpdir):
    input_content = [expected_output[0],
                     expected_output[3]]
    input_ = json.dumps(input_content)
    output_json = tmpdir.join('components.json')
    output_csv = tmpdir.join('components.csv')
    main(['--rpmdata-path', gen_input(tmpdir, input_),
          '--output-components', str(output_json),
          '--output-components-csv', str(output_csv)])
    additions = [{'FOSS': u'yes',
                  'Source RPM': 'internal-pkg-4-4.src.rpm',
                  'Name': '@types/d3-axis',
                  'Source URL': 'http://some.url/1',
                  'Version': '1.0.10',
                  'Crypto capable': True},
                 {'FOSS': u'Yes',
                  'Source RPM': 'internal-pkg-4-4.src.rpm',
                  'Name': '@types/d3-array@*',
                  'Source URL': 'http://some.url/2',
                  'Version': '1.2.1'}]
    assert json.loads(output_json.read()) == input_content + additions
    assert output_csv.read() == _gen_components_csv(input_content + additions)


def _gen_components_csv(_list):
    csv = CsvConverter(_list, preferred_field_order=['Name', 'Version', 'Release', 'Source RPM'])
    return csv.convert_to_ms_excel(text_fields=['Version'])
