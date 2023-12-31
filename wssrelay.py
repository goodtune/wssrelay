import click
import websocket
from first import first
from github import Github


@click.command()
@click.option("--github-token", envvar="GITHUB_TOKEN")
@click.option("--repository", "--repo")
@click.option("--organization", "--org")
@click.option("--reset", is_flag=True, default=False)
def wssrelay(github_token, repository, organization, reset):
    if (repository and organization) or not (repository or organization):
        raise click.UsageError("Must specify exactly one of --repo or --org")

    gh = Github(jwt=github_token)  # FIXME: can we do App Auth?

    if repository:
        thing = gh.get_repo(repository)
    elif organization:
        thing = gh.get_organization(organization)
    else:
        raise click.ClickException("Unexpected situation with no --repo or --org")

    click.secho(f"thing={thing}", fg="red")

    hook = first(thing.get_hooks(), key=lambda x: x.name == "cli")

    click.secho(f"hook={hook}", fg="cyan")

    if hook and reset:
        click.secho(f"Deleting {hook}", fg="white", bg="red")
        hook.delete()
        hook = None

    if hook is None:
        hook = thing.create_hook(
            "cli",
            {
                "url": "wss://webhook-forwarder.github.com/forward",
                "content_type": "json",
            },
            ["push", "pull_request"],
            active=True,
        )

    click.secho(f"hook={hook}", fg="cyan")

    click.secho(f"{hook.raw_data['ws_url']}", fg="red")

    ws = websocket.WebSocket()
    ws.connect(hook.raw_data["ws_url"], header={"Authorization": github_token})
    while True:
        ws.recv()


if __name__ == "__main__":
    wssrelay()
