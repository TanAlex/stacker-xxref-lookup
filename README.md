# README for xxref lookup

## Overview

This repo is to extend Stacker's xref lookup

https://stacker.readthedocs.io/en/latest/lookups.html#xref-lookup

The original xref is limited to the same account and same region of the caller  
This xxref lookup is designed to fill the gap to allow cross accounts and cross region stack lookups

## Usage

Copy `xxref_lookup.py` and `utils.py` to your code repo

In your stack yaml file which needs xross account lookup, put all the assume-roles arns in `tags`  
Refer to the `hook_test.yaml` snippet below
```
tags:
  shared: arn:aws:iam::12345567890:role/AWSControlTowerExecution
  dev: arn:aws:iam::23455678901:role/AWSControlTowerExecution
  prod: arn:aws:iam::34556789012:role/AWSControlTowerExecution

lookups:
    xxref: hooks.xxref_lookup.handle
```

the lookup Syntax is:
```
      Syntax:  <tag>@<region>/<stack_name>::<output_name>
          or   <tag>/<stack_name>::<output_name>
      Eample: shared@us-west-2/lab-shared-vpc::VpcId
          or: shared/lab-shared-vpc::VpcId
```
Example snippet:
```
    args:
      vpc_id: ${xxref shared/lab-shared-vpc::VpcId}
      dev_vpc_id: ${xxref dev@us-west-2/lab-dev-vpc::VpcId}
```

Run test

```
stacker build common.env hook_test.yaml -r us-west-2
```

Result
```
stacker build common.env hook_test.yaml -r us-west-2
Registering lookup `xxref`: Please upgrade to use the new style of Lookups.
[2019-09-22T11:13:36] Using default AWS provider mode
[2019-09-22T11:13:37] Executing pre_build hooks: hooks.test_hook.print_result
[2019-09-22T11:13:38] xxref output: vpc-0a4d82c33xxxxxxxx
[2019-09-22T11:13:39] xxref output: vpc-0eb3a12ecyyyyyyyy
[2019-09-22T11:13:40] xxref output: vpc-074b251a5zzzzzzzz
[2019-09-22T11:13:40] Required hook hooks.test_hook.print_result failed. Return value: False
```

Note:

The hook.test_hook failed notice is expected, it is just a placeholder so it intentionally returns False  
