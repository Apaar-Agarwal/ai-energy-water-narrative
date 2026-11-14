> Historical review. Current deployment and final status: FINAL_REVIEW_NOV14.md.

# Shared main upload — 8 November 2026

Apaar authorised publishing the shared integrated app, data, processing scripts, combined documentation and setup files to main. No individual contributor folder is included in this commit; each member uploads their own reviewed folder from their GitHub account, in any order. contributors/README.md gives the entry points.

The obsolete top-level dashboards guide was removed. The shared app imports only root/frontend/story and reads shared processed data. No environment, cache, secret, ZIP archive or fabricated public app URL is included in this shared upload. Public source data filenames and workbook contents remain unchanged.

Use scripts/verify_integration.py --shared-only until all member uploads arrive; member comparisons are explicitly not run in that mode. Then run the strict default verification, deploy the final assessed commit and record real URLs/revisions in the submission PDF. Original member branch revisions remain documented in BRANCH_SOURCES.json. The combined provenance preserves each member's supplied account; the commit author is not a claim of sole authorship of the team app.

Shared-only verification passed before upload: 40 electricity rows and 192 water records match source checks; 65/86 recomputed; all four initial charts and guided interactions passed. Local render 2.86 seconds, country update 0.81 seconds. Member snapshot checks were explicitly not run because those files are reserved for member uploads. Windows temporary cleanup emitted a warning after successful assertions and exit code 0.

Git attributes preserve CSV source bytes and binary assets, and keep Unix shell scripts on LF line endings.
