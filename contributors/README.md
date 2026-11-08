# Individual contributions

Each member uploads their own folder containing the standalone contribution and supporting files. This shared commit contains only this guide; the member folders may arrive independently:

| Member | Standalone entry point (relative to project root) |
|---|---|
| Apaar | contributors/Apaar/app.py |
| Brighty | contributors/Brighty/dashboards/electricity_comparison.py |
| Harsh | contributors/Harsh/dashboards/m4_stress_vs_drought.py |
| Sanjai | contributors/Sanjai/app.py |

Run the integrated group story from root app.py. These standalone files document individual work; they are not imported to assemble the story. Member subfolders may retain their original dashboards directories.

The former top-level dashboards directory was removed as redundant. Its corrected Brighty/Harsh modules now live in the member folders: Brighty's data paths are anchored to its member folder, and Harsh's source path uses data/raw. Historical provenance may name dashboards/... relative to the original member project; see the paths above. Prior package snapshots and branch revisions retain the originals.
