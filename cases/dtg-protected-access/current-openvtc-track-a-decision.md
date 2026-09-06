# Implementation decision

Use a **small current-target adapter**, not a generalized new evidence framework and not a renamed Dogwood adapter.

This preserves three useful properties: historical Dogwood evidence remains intelligible; generic `composed-unlinkability-v1` capture/classification/export semantics stay stable; and target-specific breakage caused by future OpenVTC changes is localized to the adapter that actually knows that implementation surface.
