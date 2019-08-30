=====================================
  Stock On-Call Sales Order Management
=====================================

This module is a custom add-on to ``stock`` and ``sale``.
This module creates a Route ``On-Call`` in the stock routes that will be available in the Sales Order Lines.
``On-Call`` route will create two picking-lists when an Order is validated:
* one that takes the product on the Sales Order Line from the Location set in the Sales Order to the Location set on the Customer form
* one that tales the product on the Sales Order Line from the Location set on the Customer form to the Virtual Stock Customer

When the order is validated and the route ``On-Call`` is used on a line, it will check if the customer has a specific Location set.
If yes, it will act as described above.
If not, it will create a dedicated stock location using the Customer Reference for name and act as described above.

It also adds a smart button in the Partner Form to list all the products available in the partner stock location.

Installation notes
==================


Credits
=======

Contributors
------------

* Valentin Thirion <valentin.thirion@abakusitsolutions.eu>

Maintainer
-----------

.. image:: http://www.abakusitsolutions.eu/wp-content/themes/abakus/images/logo.gif
   :alt: AbAKUS IT SOLUTIONS
   :target: http://www.abakusitsolutions.eu

This module is maintained by AbAKUS IT SOLUTIONS
