Referrals Outgoing Referrals
=============================

This test will select a "referral" case and upon form submission, essentially "close" the case and
make it unavailable for selection on the next iteration. Therefore, this test requires setting up
a large enough set of cases for each user so that the case list is not exhausted during the test.

The "Referrals Search for Beds" test script will create cases that will be consumed by this test. So,
running that test first could suffice. Alternatively, "referral" cases can be imported with the case property
"current_status" set to "open".

Central Registry Search and Admit
==================================

This test will select a "client" case. These cases will not be consumed during the test, so it only needs
to be set up once for the domain. See "client-cases-import-example" for a template on how to define the
cases to be imported, then follow case import `instructions <https://dimagi.atlassian.net/wiki/spaces/commcarepublic/pages/2143946828/Importing+Cases+Using+Excel#When-Should-I-Use-the-Case-Importer>`_.
