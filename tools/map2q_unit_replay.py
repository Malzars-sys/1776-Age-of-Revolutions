"""Read-only comparison of old snapshot tests on the actual MAP2Q baseline.

Does not change earlier tests, fixtures or their reports. Redirects only current
bitmap/active-ledger reads in this isolated Python process.
"""
import io,json,sys,unittest
import map2q_eutin as q
import map2l_mainz as core

suites=['test_map2l_registry','test_map2m_r8','test_map2m_r9','test_map2n_island','test_map2n_completion','test_map2o_east_frisia']
loader=unittest.TestLoader();suite=loader.loadTestsFromNames(suites)
original=core.packed
import map2l_registry as registry
original_dirs=registry.approved_lot_dirs
registry.approved_lot_dirs=lambda:[p for p in original_dirs() if p!=q.OUT]
def packed(path):
    return original(q.OUT/'provinces_before.png' if path.resolve()==(q.ROOT/'map_data/provinces.png').resolve() else path)
core.packed=packed
core.active_registry_path=lambda:q.OUT/'PRE_LOT_REGISTRY.json'
stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=1).run(suite)
q.dump('UNIT_TESTS_PRE_LOT.json',dict(tests=result.testsRun,failures=[t.id() for t,_ in result.failures],errors=[t.id() for t,_ in result.errors],
    output=stream.getvalue(),scope='Pre-MAP2Q bitmap and imperial registry replay only; not an engine simulation'))
print(stream.getvalue())
