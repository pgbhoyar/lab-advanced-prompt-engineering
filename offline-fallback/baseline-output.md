# Offline Fallback — Baseline Response Sample (Lab 00)

Use this if the network or model is unavailable during the session. This is a **sanitized,
synthetic** example of a typical baseline response to `starter-01`. Actual responses vary.

## Input (SR-0001)

> Hi, my laptop won't connect to the office WiFi since this morning. I've tried restarting.
> I have a client demo at 2pm and can't get online. Everyone else on my team seems fine.
> Can someone help? - Jordan, Sales

## Example baseline response (vague prompt)

> It sounds like your laptop is having trouble connecting to the WiFi. Since your teammates are
> fine, the issue is probably specific to your device. You could try forgetting the network and
> reconnecting, checking that WiFi is turned on, or restarting the router. If that doesn't work,
> contact IT support. Good luck with your demo!

## Observable weaknesses (for the exercise)

1. No structure — free prose that another system cannot reliably parse.
2. No explicit **category** or **urgency**, and no criteria for them.
3. Does not state what information is missing or whether a human should review.

These are exactly the gaps Lab 01 (Explicit Prompt Contract) addresses.
