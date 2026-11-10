The first candidate audit invocation stopped before writing its JSON result.
Its deliberate `wrong_country` mutation introduced `c:BRZ`, outside the fixture
interpreter's selected vocabulary. The six-case loop recorded this as failure,
but the separate existing-country equivalence check did not yet catch the same
ValueError and terminated the run. The reader now records that check as false
for unsupported mutated predicates; it does not accept an unknown predicate.
No gameplay file was installed or modified by the failed audit. This is an
audit-control exception, not a reported engine error or a failed candidate fix.
