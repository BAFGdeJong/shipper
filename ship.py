import pshipper.commands as cmd

import typer

app = typer.Typer()

@app.command()
def generate_variant_table(
        starsector_data_dir: str = typer.Option(..., "-d", "--data"),
        ships: str = typer.Option(..., "-s", "--ships"),
        key_by: str = typer.Option("name", "-kb", "--key-by"),
        template: str = typer.Option("ship_variant.template", "-t", "--template"),
        notes: str = typer.Option("notes.json", "-n", "--notes"),
        collapse_whitelist: str = typer.Option("collapse_whitelist.json", "-cw", "--collapse-whitelist"),
        collapse_after_amount: int = typer.Option(0, "-cam", "--collapse-after-amount"),
        write_to_file: str = typer.Option(None, "-wtf", "--write-to-file"),
):
    cmd.generate_variant_table(starsector_data_dir, key_by, ships, template, notes,
                               collapse_whitelist, collapse_after_amount, write_to_file)

@app.command()
def view_ship(
        starsector_data_dir: str = typer.Option(..., "-d", "--data"),
        ship: str = typer.Option(..., "-s", "--ships"),
        key_by: str = typer.Option("name", "-kb", "--key-by")
):
    cmd.view_ship(starsector_data_dir, ship, key_by)

@app.command()
def view_hull_mod(
        starsector_data_dir: str = typer.Option(..., "-d", "--data"),
        hull_mod: str = typer.Option(None, "-m", "--hull-mod"),
        key_by: str = typer.Option("name", "-kb", "--key-by"),
        random: bool = typer.Option(False, "-r", "--random"),
):
    cmd.view_hull_mod(starsector_data_dir, hull_mod, key_by, random if hull_mod is None else False)

@app.command()
def view_ship_system(
        starsector_data_dir: str = typer.Option(..., "-d", "--data"),
        system: str = typer.Option(None, "-m", "--hull-mod"),
        key_by: str = typer.Option("name", "-kb", "--key-by"),
        random: bool = typer.Option(False, "-r", "--random"),
):
    cmd.view_ship_system(starsector_data_dir, system, key_by, random if system is None else False)

@app.command()
def validate_wiki_ship_info(
        starsector_data_dir: str = typer.Option(..., "-d", "--data"),
        ships: str = typer.Option(..., "-s", "--ships"),
        key_by: str = typer.Option("name", "-kb", "--key-by"),
        show_identical: bool = typer.Option(False, "-si", "--show-identical"),
):
    cmd.validate_wiki_ship_info(starsector_data_dir, ships, key_by, show_identical)

#
# @app.command()
# def sync(
#     update: bool = typer.Option(False, "-u", "--update"),
#     ships: str = typer.Option(..., "-s", "--ships")
# ):
#     """
#     Sync content.
#     """
#     if update:
#         typer.echo("Updating...")

if __name__ == "__main__":
    app()

    #
    # parser = argparse.ArgumentParser(description="Shipper Tool")
    # parser.add_argument("-d", "--data", default="", help="Set starsector data directory", required=True)
    #
    # subparsers = parser.add_subparsers(dest="command", required=True)

# if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Shipper Tool")
    #
    # parser.add_argument("-d", "--data", default="", help="Set starsector data directory", required=True)
    #
    # subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
    #
    # # CHECK
    # check_parser = subparsers.add_parser("check", help="Check if wiki page needs to be updated")
    #
    # check_subparsers = check_parser.add_subparsers(dest="subcommand", help="Check wiki page")
    #
    # check_variant_table_parser = check_subparsers.add_parser("variant_table", help="Check table")
    #
    # check_variant_table_parser.add_argument("-s", "--ships", default="", help="Ships tables to create", required=True)
    #
    # # GENERATE
    # generate_parser = subparsers.add_parser("generate", help="Generate content")
    #
    # generate_subparsers = generate_parser.add_subparsers(dest="subcommand", help="Generate sub-commands", required=True)
    #
    # variant_table_parser = generate_subparsers.add_parser("variant_table", help="Generate a variant table")
    #
    # variant_table_parser.add_argument("-s", "--ships", default="", help="Ships tables to create", required=True)
    # variant_table_parser.add_argument("-n", "--notes", default="notes.json", help="Path to the notes JSON")
    # variant_table_parser.add_argument("-t", "--template", default="ship_variant.template",
    #                                   help="Path to the template file")
    # variant_table_parser.add_argument("-o", "--collapse_whitelist", default="collapse_whitelist.json",
    #                                   help="Path to the whitelist JSON")
    # variant_table_parser.add_argument("-c", "--collapse_after_amount", default=0, type=int,
    #                                   help="After what amount of variants to collapse")
    # variant_table_parser.add_argument("-w", "--write_to_file", default="", help="Write table to disk")
    # variant_table_parser.add_argument("-k", "--key_by", default="name", help="The key to use when requesting data")
    #
    # # SYNC
    # sync_parser = subparsers.add_parser("sync", help="Sync content")
    # sync_parser.add_argument("-u", "--update", action="store_true", help="Write table to disk")
    # sync_parser.add_argument("-w", "--whitelist", default="whitelist.json", help="Filename in data/variant/")
    # sync_parser.add_argument("-n", "--notes", default="notes.json", help="Filename in data/variant/")
    # sync_parser.add_argument("-t", "--template", default="ship_variant.template", help="Filename in templates/")
    # sync_parser.add_argument("-o", "--collapse_whitelist", default="collapse_whitelist.json",
    #                          help="Path to the whitelist JSON")
    # sync_parser.add_argument("-c", "--collapse_after_amount", default=0, type=int,
    #                          help="After what amount of variants to collapse")
    # sync_parser.add_argument("-s", "--ships", default="", help="Ships to update")
    #
    # args = parser.parse_args()
    #
    # if args.data and not (args.data.endswith("/") or args.data.endswith("\\")):
    #     args.data += "/"
    #
    # if args.command == "check":
    #     check(args)
    #
    # elif args.command == "generate":
    #     generate(args)
    #
    # elif args.command == "sync":
    #     sync(args)