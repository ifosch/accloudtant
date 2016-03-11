# accloudtant [![Build Status][CI-Image]][CI-Url] [![Code Climate][CC-Image]][CC-Url] [![PyPI Version][PI-Image]][PI-Url]

  [CI-Image]: https://travis-ci.org/ifosch/accloudtant.svg
  [CI-Url]: https://travis-ci.org/ifosch/accloudtant
  [CC-Image]: https://codeclimate.com/github/ifosch/accloudtant/badges/gpa.svg
  [CC-Url]: https://codeclimate.com/github/ifosch/accloudtant
  [PI-Image]: https://badge.fury.io/py/accloudtant.svg
  [PI-Url]: https://badge.fury.io/py/accloudtant

It is a AWS cost calculator oriented to ease the life of an administrator by providing easy tools to get the costs of current infrastructure, or cost foresights.


## Requirements

In order to use this, AWS CLI must be [installed][AWS-CLI-Install] and [configured][AWS-CLI-Setup], with appropriate AWS keys.

  [AWS-CLI-Install]: http://docs.aws.amazon.com/cli/latest/userguide/installing.html
  [AWS-CLI-Setup]: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

## Install

In order to install this tool you'll need `pip`:

    pip install accloudtant

## Usage

`accloudtant` provides two basic commands: `list` and `report`.

### The `list` command

The `list` command reads current prices for AWS EC2 computing costs for all instance types and generations and prints these.
You can use this function by issuing the following command:

    accloudtant list

This command's output looks like the following:

    EC2 (Hourly prices, no upfronts, no instance type features):
    Type          On Demand    1y No Upfront    1y Partial Upfront    1y All Upfront    3y Partial Upfront    3y All Upfront
    ----------  -----------  ---------------  --------------------  ----------------  --------------------  ----------------
    c3.8xlarge        0.768            0.611                0.5121            0.5225                0.4143            0.3894
    g2.2xlarge        0.767            0.611                0.5121            0.5225                0.4143            0.3894

### The `report` command

The `report` command, invoked as follows, gets a list of your current instances and their details:

    accloudtant report

The instance details showed are:

  * The instance id,
  * its tag Name,
  * its type,
  * the availability zone where it was provisioned,
  * the operating system,
  * its current state,
  * the launch time,
  * if it is reserved,
  * current hourly price being billed,
  * the hourly price it would have if reserved again.


The `report` command requires access to the AWS API using AWS CLI credentials setup, or appropriate environment variables.

The following is an example of the output of this command:

    Id          Name    Type        AZ          OS          State    Launch time          Reserved      Current hourly price    Renewed hourly price
    ----------  ------  ----------  ----------  ----------  -------  -------------------  ----------  ----------------------  ----------------------
    i-912a4392  web1    c3.8xlarge  us-east-1c  Windows     running  2015-10-22 14:15:10  Yes                         0.5121                  0.3894
    i-1840273e  app1    r2.8xlarge  us-east-1b  RHEL        running  2015-10-22 14:15:10  Yes                         0.3894                  0.3794
    i-9840273d  app2    r2.8xlarge  us-east-1c  SUSE Linux  running  2015-10-22 14:15:10  Yes                         0.5225                  0.389
    i-1840273d  db1     r2.8xlarge  us-east-1c  Linux/UNIX  stopped  2015-10-22 14:15:10  No                          0                       0.379
    i-1840273c  db2     r2.8xlarge  us-east-1c  Linux/UNIX  running  2015-10-22 14:15:10  Yes                         0.611                   0.379
    i-1840273b  db3     r2.8xlarge  us-east-1c  Linux/UNIX  running  2015-10-22 14:15:10  Yes                         0.611                   0.379
    i-912a4393  test    t1.micro    us-east-1c  Linux/UNIX  running  2015-10-22 14:15:10  No                          0.767                   0.3892

#### About the instance details

Since the AWS API doesn't provide ways of getting certain information, `accloudtant` tries to get by other means:

  - The operating system is guessed from the output of the system logs, which only contains the boot logs.
  - The reserved status of each instance is calculated by checking the instace types, availability zones, and operating systems across the list of both instances and reserved instances.
  - The prices printed are always in an hourly basis.

## Development

In order to get a proper development environment, the following steps might be followed:

  1. Optionally create your environment. If using [Conda](http://conda.pydata.org/docs/intro.html):

        conda env create

  2. Run setup in development mode from project root directory:

        python setup.py develop
        
### Publish process

This is a small brief description of tasks done to release a new version:

  - Update `version` in `setup.py`
  - Update GitHub project and publish release with corresponding version number
  - Run `pandoc --from=markdown --to=rst --output=README README.md`
  - Run `python setup.py sdist upload`

## Roadmap

List of features for version 0.1.0:

  * Get prices from AWS EC2
  * List prices from AWS EC2
  * Get current EC2 costs report
  
The list of features for version 0.2.0:

  * Usage of different accounts

Other goals:

  * Allow select by tag, AZ, service when getting the costs
  * Reservation budget/foresight
  * Cross check with Cloudwatch and prediction
  * Use multiple accounts at a time
  * Output formats (CSV, ODS, XLS,...)
  * Add more AWS services to get prices and costs
  * Add more providers
  * Web/API REST interface
  * IPython interface
  * Customizable reports
