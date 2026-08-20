# ANAB name-assurance gate

An A2A client resolves an active ARPA agent and retrieves a card carrying the ANAB description extension. Before consequential interaction, the relying implementation checks that the card name matches the assured name, that the identity state and freshness are current, and that declaration and card-binding evidence are intact. These checks admit ANAB as an assurance input only. ARPA delegation and relying-party policy still control effect admission.

Negative variants exercise a mismatched name, stale assurance, revoked identity, and unbound declaration/card evidence. Each must fail before the A2A task can be treated as eligible for consequential execution.
