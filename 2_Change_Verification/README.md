# 2. Automate change verification

pyATS, Network Test & Automation Solution, is a Python based versatile test framework that can be used to verify the state of the network, run tests, and even for making configuration changes. pyATS can be used either from CLI or from Python, making it possible to use the powerful features even without programming knowledge.

## Documentation
- [Cisco pyATS: Network Test & Automation Solution](https://developer.cisco.com/docs/pyats/#!introduction/cisco-pyats-network-test--automation-solution)
- [Getting Started with pyATS](https://developer.cisco.com/docs/pyats-getting-started/)

## pyATS requirements
You can install pyATS on any of the following platforms:
- Most flavors of Linux
- macOS
- Docker containers
- Windows Subsystem for Linux

To install pyATS in your Python virtual environment, you would use `pip install`. The full pyATS is included in the requirements.txt in the root of this repository.

```bash
pip install "pyats[full]"
```

For using the Rest Connector with Cisco DNA Center, also `rest.connector` needs to be installed. This is included in the requirements.txt in the root of this directory.
```bash
pip install rest.connector
```

Read more about the requirements [here](https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/prereqs/prerequisites.html#).

## Testbed

In this repository we have defined the test devices in the [testbed.yaml](testbed.yaml). 
For the IOS XE examples, [*IOS XE on Catalyst 9000 17.03 Code*](https://devnetsandbox.cisco.com/RM/Diagram/Index/e1c0225d-3dfb-4bba-b45a-67308d5251f7) DevNet sandbox device is used. This sandbox is available to reserve for anyone with the DevNet account at the time of writing this instruction. If the sandbox is not available when you read this, review other available sandboxes from the [DevNet Sandbox](devnetsandbox.cisco.com).
For the DNA Center example, the [always-on DevNet DNA Center sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/c3c949dc-30af-498b-9d77-4f1c07d835f9?diagramType=Topology) is used. Note that at the time of writing this instruction, this sandbox is read-only.

## pyATS CLI with IOS XE
**To learn a specific feature** on a device using pyATS models, you can use the CLI command `learn`. The following CLI command learns the VLAN configuration of the device `DISTROSW01`, which is defined in the `testbed.yaml`.

```Bash
pyats learn vlan --testbed-file testbed.yaml --devices "DISTROSW01"
```
For the available pyATS models and their details, refer to the [documentation](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models).

**To query with a specific CLI command** and **to parse the outcome**, you can use the CLI command `parse`.
```Bash
pyats parse "show vlan" --testbed-file testbed.yaml --devices "DISTROSW01"
```
For the available pyATS parses and their details, refer to the [documentation](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers).

By using option `--output <output directory>`, you can store the output from the `parse`and `learn`commands to a selected directory. **To compare different snapshots**, use the pyATS CLI command `diff`. You can specify specific files to be compared, or just compare the contents of two directories.
```Bash
pyats diff file1 file2
pyats diff dir1 dir2
```

**Thus a full flow to compare pre- and post-snapshot could be the following:**
```Bash
pyats learn vlan --testbed-file testbed.yaml --devices "DISTROSW01" --output pre-snapshot
# make a change
pyats learn vlan --testbed-file testbed.yaml --devices "DISTROSW01" --output post-snapshot
pyats diff pre-snapshot post-snapshot
```

You can access the documentation online for further information, however you can also use the CLI manual by using the option `--help`:
```Bash
pyats --help
pyats learn --help
pyats parse --help
pyats diff --help
```

## pyATS Python library with Cisco DNA Center

To take a snapshot from Cisco DNA Center, you would use one of the APIs together with the pyATS Rest Connector. Documentation on how to use the Rest Connector can be found from the [documentation](https://developer.cisco.com/docs/rest-connector/) and the details for Cisco DNA Center usage in the [user guide section for Cisco DNA Center](https://pubhub.devnetcloud.com/media/rest-connector/docs/user_guide/services/dnac.html#). The details for pyATS to connect to the Cisco DNA Center controller are defined in the testbed and the Rest Connector is defined in the connection class:
```yaml
      rest:
        class: rest.connector.Rest
```
Note that the [DevNet DNA Center sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/c3c949dc-30af-498b-9d77-4f1c07d835f9?diagramType=Topology) is (at least at the time of writing this) read-only. If you want to test the functionality of comparing snapshots while using the read-only DevNet sandbox, a good option is to manually change one of the values of the post snapshot to simulate a change in the network.

To connect to DNA Center using pyATS in Python script, you need to import `topology` module from `pyats`. Then you can load the testbed file (`"testbed.yaml"`), select the device you want to test (`"dnac"`) and connect to the device using method `connect()`.
```python
from pyats import topology

testbed = topology.loader.load('testbed.yaml')
device = testbed.devices['dnac']
device.connect()
```
Once you are connected, you can retrieve the preferred snapshot by using the DNA Center APIs and pyATS Rest Connector method `rest.get()`:

```python
url = '/dna/intent/api/v1/interface'
today = device.rest.get(url)
```

To compare snapshots, you can use the pyATS `Diff`, which takes two Python objects and finds their differences with `findDiff()` method.
```python
from genie.utils.diff import Diff
diff = Diff(today.json(), yesterday.json())
diff.findDiff()
print(diff)
```

For a full code taking both the snapshots and comparing them with `Diff`, refer to the [dna_center_snapshot.py](dna_center_snapshot.py).