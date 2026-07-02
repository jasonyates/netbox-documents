# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/jasonyates/netbox-documents/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

Netbox Documents Plugin could always use more documentation, whether as part of the
official Netbox Documents Plugin docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/jasonyates/netbox-documents/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `netbox-documents` for local development.

1. Fork the `netbox-documents` repo on GitHub.
2. Clone your forked `netbox-documents` repository and the `netbox` repository:

    ```
    $ git clone git@github.com:your_name_here/netbox-documents.git
    $ git clone https://github.com/netbox-community/netbox.git
    ```

3. Enter the NetBox repository and a virtualenv:

    ```
    $ cd netbox
    $ python3.13 -m venv venv
    $ . venv/bin/activate
    ```

4. Install dependencies for NetBox, and add the forked netbox-documents plugin for testing:

    ```
    $ pip install -e ../netbox-documents/
    ```

5. Now you can make your changes in `netbox-documents` locally:

    ```
    $ cd ../netbox-documents
    $ git checkout -b my-new-feature
    ```

5. When you're done making changes, check that your changes pass the
   tests:

    ```
    $ cd ../netbox
    $ NETBOX_CONFIGURATION=netbox.configuration_testing python netbox/manage.py test netbox_documents
    ```

    Note this requires a PostgreSQL and Redis/Valkey server on localhost.

6. Commit your changes and push your branch to GitHub:

    ```
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

7. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
3. The pull request should work for the Python version used by NetBox itself. Check
   https://github.com/jasonyates/netbox-documents/actions
   and make sure that the tests pass for all supported Python versions.