# Lab 02 — Challenge (Optional)

> Optional. Does not block later labs.

1. Try `adversarial-indirect-01`, where the injection is hidden inside a *forwarded ticket* in
   the `policy_context`. Does the improved prompt still resist it?
2. Add a second layer of defense: instruct the model to quote the exact sentence it treated as an
   injection attempt. Does explicit acknowledgement make the behavior more reliable?
