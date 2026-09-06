# Upstream boundary

This evidence tranche treats `OpenVTC/verifiable-trust-infrastructure` as read-only source material. The workflow checks out an immutable revision, creates a temporary test-only observer file inside the ephemeral runner checkout, executes it, removes it, and verifies that the checkout is clean. No commit, branch, pull request, issue, comment, tag, release, or other write is made to OpenVTC or to any `trustoverip/*` repository.
