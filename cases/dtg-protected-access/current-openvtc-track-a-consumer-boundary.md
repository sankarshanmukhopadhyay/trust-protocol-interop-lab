# Producer / consumer boundary

Interop Lab answers **what the pinned implementation actually exposed during the bounded execution**. DPIP answers **whether the resulting evidence is acceptable, applicable and sufficient for the privacy question**. RAHP answers **what that privacy judgment does to the relevant assurance propositions and aggregate state**.

Those are deliberately three separate decisions. #153 can therefore complete its producer obligation even if the current implementation path leaves `ER-STATUS-AB` or `ER-TASK-AB` unresolved. The unresolved requirements must travel downstream as explicit evidence gaps rather than keeping the producer issue artificially open or, worse, being filled with synthetic observations.
