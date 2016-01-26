# accloudtant [![Build Status][CI-Image]][CI-Url]

    [CI-Image]: https://travis-ci.org/ifosch/accloudtant.svg
    [CI-Url]: https://travis-ci.org/ifosch/accloudtant

It is a AWS cost calculator oriented to ease the life of an administrator by providing easy tools to get the costs of current infrastructure, or cost foresights.

## Development

In order to have development environment working fine, it is required to follow these steps:

  1. Optionally create your environment. If using [Conda](http://conda.pydata.org/docs/intro.html):

        conda env create


  2. Run setup in development mode from project root directory:

        python setup.py develop

## Roadmap

MVP for release 1:

  * Get prices from AWS EC2
  * List prices from AWS EC2
  * Get current EC2 costs report

Other goals:

  * Allow select by tag, AZ, service when getting the costs
  * Allow select account to use
  * Reservation budget/foresight
  * Cross check with Cloudwatch and prediction
  * Use multiple accounts at a time
  * Output formats (CSV, ODS, XLS,...)
  * Add more AWS services to get prices and costs
  * Add more providers
  * Web/API REST interface
  * IPython interface
  * Customizable reports
