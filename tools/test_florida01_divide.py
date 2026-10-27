"""Regression guards for State splitting in future-sale and conquest content."""
import unittest
from florida01_divide import broaden,exclude_buyer,parse,walk,normalized


class FloridaDependencies(unittest.TestCase):
    def test_sale_keeps_the_seller_filter_and_visits_every_share(self):
        raw='event = { random_state = { limit = { state_region = s:STATE_FLORIDA owner = { OR = { this = scope:seller is_subject_of = scope:seller } } } set_state_owner = scope:buyer } }'
        result=parse(broaden(raw));sale=next(n for n in walk(result) if n.key=='every_state')
        old_owner=next(n for n in walk(parse(raw)) if n.key=='owner')
        self.assertEqual(normalized([old_owner]),normalized([next(n for n in walk(sale.children()) if n.key=='owner')]))
        self.assertFalse(any(n.key=='random_state' for n in walk(result)))
        self.assertEqual(sum(n.key=='set_state_owner' for n in walk(result)),1)

    def test_full_ownership_cannot_be_satisfied_by_one_half(self):
        result=parse(broaden('complete = { owns_entire_state_region = STATE_FLORIDA }'))
        clause=result[0].children()[0]
        self.assertEqual(clause.key,'AND')
        self.assertEqual({n.value for n in clause.children()},{'STATE_FLORIDA','STATE_WEST_FLORIDA'})

    def test_representative_saved_scope_not_duplicated(self):
        raw='immediate = { s:STATE_FLORIDA = { save_scope_as = florida_region } }'
        self.assertEqual(normalized(parse(raw)),normalized(parse(broaden(raw))))

    def test_unrelated_state_and_effects_unchanged(self):
        raw='event = { state_region = s:STATE_GEORGIA add_claim = c:SPA change_relations = { country = c:USA value = 10 } }'
        self.assertEqual(normalized(parse(raw)),normalized(parse(broaden(raw))))

    def test_purchaser_cannot_be_selected_as_its_own_seller(self):
        raw='florida.4 = { immediate = { random_state = { limit = { state_region = s:STATE_FLORIDA owner = { NOT = { is_country_type = decentralized } } } save_scope_as = florida_scope } } }'
        updated=exclude_buyer(broaden(raw),'florida.4')
        owner=next(n for n in walk(parse(updated)) if n.key=='owner')
        self.assertTrue(all(any(n.one(field)=='root' for n in owner.children('NOT')) for field in ['this','is_subject_of']))
        self.assertTrue(any(n.one('is_country_type')=='decentralized' for n in owner.children('NOT')))


if __name__=='__main__':unittest.main()
