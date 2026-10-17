import copy
import unittest
from map2l_runtime_receipt import annotate

class ReceiptTests(unittest.TestCase):
    def test_manual_record_preserves_static_failure(self):
        report={'status':'FAIL','checks':[{'name':'existing failure','passed':False}],'engine_tested':False,'inherited_reference_errors':['old']}
        original=copy.deepcopy(report);annotate(report,'BELGIUM')
        for key,value in original.items():self.assertEqual(report[key],value)
        self.assertEqual(report['runtime_status'],'PASS_RUNTIME_USER_VALIDATED')
        self.assertFalse(report['runtime_user_validation']['automated_engine_test'])
        self.assertFalse(report['runtime_user_validation']['historical_boundary_certification'])
    def test_new_uninspected_lot_not_promoted(self):
        report={'status':'PASS_STATIC_ENGINE_DEFERRED','engine_tested':False};original=copy.deepcopy(report)
        self.assertEqual(annotate(report,'MINDEN_RAVENSBERG'),original)
    def test_receipt_is_idempotent(self):
        report={'status':'FAIL','checks':[]};annotate(report,'FRANCONIA');original=copy.deepcopy(report)
        self.assertEqual(annotate(report,'FRANCONIA'),original)
    def test_late_receipt_is_scoped_and_preserves_failure(self):
        report={'status':'FAIL','engine_tested':False,'checks':[{'passed':False}]};original=copy.deepcopy(report)
        annotate(report,'SWABIA')
        for key,value in original.items():self.assertEqual(report[key],value)
        self.assertIn('RHINE_SWABIA',report['runtime_user_validation']['receipt'])
        self.assertIn('One in-game month',report['runtime_user_validation']['duration'])
    def test_continuation_not_promoted(self):
        report={'status':'PASS_STATIC_ENGINE_DEFERRED'};original=copy.deepcopy(report)
        self.assertEqual(annotate(report,'SWABIA_CONTINUATION'),original)
    def test_completion_and_nested_addon_are_scoped(self):
        for name in ['SWABIA_COMPLETION','SWABIA_COMPLETION/PRUSSIAN_INDUSTRY_ADDON']:
            report={'status':'FAIL','engine_tested':False};annotate(report,name)
            self.assertEqual(report['runtime_status'],'PASS_RUNTIME_USER_VALIDATED')
            self.assertEqual(report['status'],'FAIL')
    def test_new_prussian_work_not_manually_certified(self):
        for name in ['PRUSSIA_MICRO_ADJUSTMENT_2026_10_14','LOWER_SILESIA_TEXTILE_REMOVAL','OTHER/PRUSSIAN_INDUSTRY_ADDON','PEENE','NETZE']:
            report={'status':'FAIL'};self.assertEqual(annotate(report,name),{'status':'FAIL'})
    def test_prussian_core_manual_receipt_not_new_geometry(self):
        report={'status':'PASS_STATIC_ENGINE_DEFERRED','engine_tested':False};annotate(report,'PRUSSIAN_BORDERS')
        self.assertEqual(report['runtime_status'],'PASS_RUNTIME_USER_VALIDATED')
        self.assertEqual(report['runtime_user_validation']['date'],'2026-10-15')
        self.assertFalse(report['engine_tested'])

if __name__=='__main__':unittest.main()
