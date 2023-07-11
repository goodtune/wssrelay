# wssrelay

Utility to relay using GitHub websocket webhook events.

Based on https://docs.github.com/en/webhooks-and-events/webhooks/receiving-webhooks-with-the-github-cli

## Testing

When you've got a current `gh webhook forward` session running, try using `wsdump` to connect and listen.

    wsdump -v 2 --headers "Authorization: $(gh auth token)" $(gh api repos/USER/REPO/hooks --jq 'first|.ws_url')
