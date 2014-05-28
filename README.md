pyrannosaurus
=============

Python based tools for interacting and developing against the Salesforce platform, currently WIP. 

Currently supports the Metadata, Tooling and Apex API. Also has a few useful utilities for interacting with the xml and responses. 


4/9/14 - Published a very minimal, hopefully stable release, and published it on PyPi. This contains a good amount of functionality, though may contain issues. 

4/15/14 - published 0.0.2 with a zip creation utility, and the check_deploy_status implmemented, to begin working with deployments.

4/19/14 - published 0.0.3 with a schedule apex set of utilities, moving header support to base client, and execute anonymous support

4/20/14 - published patch 0.0.4, added ability to create an object from base client that checks both the sub and base, updated find packages

4/23/14 - published 0.0.5 changing how wsdls are installed and referenced in setup.py, added the base client create method, several new utils, refactored login to support base client methods from sub clients, added utility unit tests, unpinned lxml version 
