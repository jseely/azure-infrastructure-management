#!/usr/bin/env python3
import cli
import json

print(json.dumps(cli.execute(['keyvault', 'list']), indent=4))
