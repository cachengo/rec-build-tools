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

# pylint: disable=line-too-long,invalid-name
import json

from tools.script.ci_build_diff import main
from tools.script.ci_build_diff_test_data import component_added, component_changed_old, \
    component_changed_new, component_removed, caas_grafana1, caas_grafana2, caas_grafana2_sub, \
    caas_grafana1_sub, caas_grafana1_v2, caas_grafana1_v2sub, caas_grafana1_r2, \
    caas_grafana1_r2sub, grafana_v1, grafana_v2, caas_grafana3, caas_grafana3_sub, caas_abc1_sub, \
    caas_abc1, caas_abc1_r2, caas_abc1_sub_r2, abc1_v2, abc1, abc2, abc3, \
    caas_grafana1_sub_new_field


def test_no_output_args(tmpdir):
    input_old, input_new = _gen_input_json(tmpdir)
    main([str(input_old), str(input_new)])


def test_no_changes(tmpdir):
    input_old, _ = _gen_input_json(tmpdir)
    output_csv = tmpdir.join('diff.csv')
    output_json = tmpdir.join('diff.json')
    main([str(input_old), str(input_old),
          '--output-csv', str(output_csv),
          '--output-json', str(output_json)])
    assert output_csv.read() == 'sep=,'
    assert json.loads(output_json.read()) == {"added": {},
                                              "changed": {},
                                              "removed": {},
                                              "counts": {
                                                  "added": 0,
                                                  "changed": 0,
                                                  "removed": 0
                                              }}


def test_no_changes_if_json_field_is_added(tmpdir):
    """
    Make sure diff is ok e.g. when new build has new field in json
    """
    _assert_json_out(tmpdir,
                     [caas_grafana1_sub],
                     [caas_grafana1_sub_new_field],
                     {"added": {},
                      "changed": {},
                      "removed": {},
                      "counts": {
                          "added": 0,
                          "changed": 0,
                          "removed": 0
                      }})


def test_multiple_rpms(tmpdir):
    _assert_json_out(tmpdir,
                     [component_changed_old, component_removed],
                     [component_changed_new, component_added],
                     {"added": {component_added['Name']: [component_added]},
                      "changed": {component_changed_old['Name']: {'old': [component_changed_old],
                                                                  'new': [component_changed_new]}},
                      "removed": {component_removed['Name']: [component_removed]},
                      "counts": {
                          "added": 1,
                          "changed": 1,
                          "removed": 1
                      }})


def test_component_name_change(tmpdir):
    """
    Sub-component does not change although RPM containing it changes
    """
    _assert_json_out(tmpdir,
                     [caas_grafana1, caas_grafana1_sub],
                     [caas_grafana2, caas_grafana2_sub],
                     {"added": {caas_grafana2['Name']: [caas_grafana2]},
                      "changed": {},
                      "removed": {caas_grafana1['Name']: [caas_grafana1]},
                      "counts": {
                          "added": 1,
                          "changed": 0,
                          "removed": 1
                      }})


def test_component_version_change(tmpdir):
    _assert_json_out(tmpdir,
                     [caas_grafana1, caas_grafana1_sub],
                     [caas_grafana1_v2, caas_grafana1_v2sub],
                     {"added": {},
                      "changed": {caas_grafana1['Name']: {'old': [caas_grafana1],
                                                          'new': [caas_grafana1_v2]},
                                  caas_grafana1_sub['Name']: {'old': [caas_grafana1_sub],
                                                              'new': [caas_grafana1_v2sub]}},
                      "removed": {},
                      "counts": {
                          "added": 0,
                          "changed": 2,
                          "removed": 0
                      }})


def test_component_release_change(tmpdir):
    _assert_json_out(tmpdir,
                     [caas_grafana1, caas_grafana1_sub],
                     [caas_grafana1_r2, caas_grafana1_r2sub],
                     {"added": {},
                      "changed": {caas_grafana1['Name']: {'old': [caas_grafana1],
                                                          'new': [caas_grafana1_r2]}},
                      "removed": {},
                      "counts": {
                          "added": 0,
                          "changed": 1,
                          "removed": 0
                      }})


def test_same_name_component_added(tmpdir):
    _assert_json_out(tmpdir,
                     [caas_grafana1, caas_grafana1_sub],
                     [caas_grafana1, caas_grafana1_sub, grafana_v1],
                     {"added": {},
                      "changed": {grafana_v1['Name']: {'old': [caas_grafana1_sub],
                                                       'new': [caas_grafana1_sub, grafana_v1]}},
                      "removed": {},
                      "counts": {
                          "added": 0,
                          "changed": 1,
                          "removed": 0
                      }})


def test_same_name_component_removed(tmpdir):
    _assert_json_out(tmpdir,
                     [caas_grafana1, caas_grafana1_sub, grafana_v1],
                     [caas_grafana1, caas_grafana1_sub],
                     {"added": {},
                      "changed": {grafana_v1['Name']: {'old': [caas_grafana1_sub, grafana_v1],
                                                       'new': [caas_grafana1_sub]}},
                      "removed": {},
                      "counts": {
                          "added": 0,
                          "changed": 1,
                          "removed": 0
                      }})


def test_same_name_component_changed(tmpdir):
    _assert_json_out(tmpdir,
                     [caas_grafana1, caas_grafana1_sub, grafana_v1],
                     [caas_grafana1, caas_grafana1_sub, grafana_v2],
                     {"added": {},
                      "changed": {grafana_v1['Name']: {'old': [caas_grafana1_sub, grafana_v1],
                                                       'new': [caas_grafana1_sub, grafana_v2]}},
                      "removed": {},
                      "counts": {
                          "added": 0,
                          "changed": 1,
                          "removed": 0
                      }})


def test_epic(tmpdir):
    _assert_json_out(tmpdir,
                     [caas_grafana1, caas_grafana1_sub,
                      caas_grafana2, caas_grafana2_sub,
                      grafana_v1],
                     [caas_grafana1_r2, caas_grafana1_r2sub,
                      grafana_v2,
                      caas_grafana3, caas_grafana3_sub],
                     {"added": {caas_grafana3['Name']: [caas_grafana3]},
                      "changed": {caas_grafana1['Name']: {'old': [caas_grafana1],
                                                          'new': [caas_grafana1_r2]},
                                  grafana_v1['Name']: {
                                      'old': [caas_grafana1_sub, caas_grafana2_sub, grafana_v1],
                                      'new': [caas_grafana1_r2sub, caas_grafana3_sub, grafana_v2]}},
                      "removed": {caas_grafana2['Name']: [caas_grafana2]},
                      "counts": {
                          "added": 1,
                          "changed": 2,
                          "removed": 1
                      }})


def _assert_json_out(tmpdir, from_build, to_build, expected_output):
    input_old, input_new = _gen_input_json(tmpdir, from_build, to_build)
    output_json = tmpdir.join('diff.json')
    main([str(input_old), str(input_new), '--output-json', str(output_json)])
    assert json.loads(output_json.read()) == expected_output


def test_csv(tmpdir):
    input_old, input_new = _gen_input_json(tmpdir,
                                           [caas_abc1, caas_abc1_sub, abc1, abc2],
                                           [caas_abc1_r2, caas_abc1_sub_r2, abc1_v2, abc3])
    output_csv = tmpdir.join('diff.csv')
    main([str(input_old), str(input_new), '--output-csv', str(output_csv)])
    rows = [['name',
             'old_components', 'old_srpms', 'old_licenses',
             'new_components', 'new_srpms', 'new_licenses'],
            ['abc',
             'abc:v1(abc-v1-r1.src.rpm)\nabc:v1(caas-abc-v1-r1.src.rpm)',
             'abc-v1-r1.src.rpm\ncaas-abc-v1-r1.src.rpm',
             'GPL\nUnknown',
             'abc:v1(caas-abc-v1-r2.src.rpm)\nabc:v2(abc-v2-r1.src.rpm)',
             'caas-abc-v1-r2.src.rpm\nabc-v2-r1.src.rpm',
             'Unknown\nGPL'],
            ['abc2',
             'abc2:v1(abc2-v1-r1.src.rpm)', 'abc2-v1-r1.src.rpm', 'GPL',
             'None', 'None', 'None'],
            ['abc3',
             'None', 'None', 'None',
             'abc3:v1(abc3-v1-r1.src.rpm)', 'abc3-v1-r1.src.rpm', 'GPL'],
            ['caas-abc',
             'caas-abc:v1(caas-abc-v1-r1.src.rpm)', 'caas-abc-v1-r1.src.rpm', 'Commercial',
             'caas-abc:v1(caas-abc-v1-r2.src.rpm)', 'caas-abc-v1-r2.src.rpm', 'Commercial']]
    expected_csv = '\r\n'.join(['sep=,'] + [_get_csv_row(row) for row in rows])
    assert output_csv.read() == expected_csv


def _get_csv_row(items):
    return ','.join(['"{}"'.format(i) for i in items])


def _gen_input_json(tmpdir, _from=None, _to=None):
    if _from is None:
        _from = [component_changed_old, component_removed]
    if _to is None:
        _to = [component_changed_new, component_added]
    input_old = tmpdir.join('input_old.json')
    input_new = tmpdir.join('input_new.json')
    json_old = json.dumps(_from)
    json_new = json.dumps(_to)
    input_old.write(json_old)
    input_new.write(json_new)
    return input_old, input_new
