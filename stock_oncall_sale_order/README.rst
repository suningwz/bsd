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

TODO : set this presa OK

This module will create a new Stock location called "On-Call / Customer name (or ref)" when an order for this customer
is validated with the route "On-Call" on one line and if this location is not already existing.
It will copy the location where the product is (avec tt les infos) and put it "under" the on-call location of the customer
It will auto transfer the product into this location
It will create an entry called "oncall_order" with all the needed info (order, line, qty to deliver, qty delivered, ...)
These entries will be available on the partner form with a smartbutton
These entries will be available on the sale order form with a smartbutton
On a list of "oncall_order" we will be able to select and get an "Action" => Send product to the customer
A popup will appear with the lines set (from the orders selected) and we will be able to specify the quantity we are sending
It will create an OUT Picking-list with all the products selected and quantities

Client : BSD
Sujet : Module Sur-Appel
Odoo 12.0E
Par Valentin THIRION

Le module 'stock_oncall_sale_order' a pour but de gérer les commandes en "sur-appel" pour les clients de BSD.
L'intégration de cette fonction est prévue dans le cadre de Odoo 12.0 Enterprise en respectant les procédures de bases des modules de ventes et de stock, sans changer les comportements standards.

Sur une fiche client, nous allons rajouter un champ "Stock Sur-Appel".
Lorsqu'une commande est validée pour ce client et qu'elle comporte au moins une ligne où la route spécifiée est "Sur-Appel", alors le système va créer un emplacement virtuel (si pas déjà existant) appelé "Sur-Appel - CUSTOMER REF/NAME".
Lorsque l'emplacement est créé, le système va déterminer où est actuellement stockée la marchandise et "dupliquer" l'emplacement où elle est. Ce nouvel emplacement va être ajouté comme sous-emplacement de l'emplacement "Sur-Appel" du client.
La duplication a pour but de garder toutes les informations de ce lieux.
Si la quantité commandée est disponible, l'entièreté du besoin va être directement transféré de l'emplacement d'origine, appartenant à BSD vers celui du Sur-Appel du client.
Si la quantité commandée n'est pas disponible, tout ce qui est possible va être transféré et le reste sera mis en attente et directement transféré lorsqu'il sera disponible (= lorsque BSD aura reçu la marchandise).

Le fait de confirmer une commande en "Sur-Appel" va créer un élément "Commande Sur-Appel" qui va contenir l'état et les informations nécessaires à cette commande.
Toutes celles-ci seront accessibles depuis la fiche client, ainsi que depuis les commandes liées.

Lorsque le client désire la marchandise, depuis sa fiche client ou depuis les commandes liées, on pourra voir les lignes en "Sur-Appel".
Il sera alors possible de spécifier la quantité pour chaque article que le client désire et ainsi réaliser un bon de livraion pour ce qu'il a demandé.
Les quantités seront ainsi décrémentées de son stock virtuel et proposées en picking par les opérateurs de stock.

A tous moment, lorsque la commande est confirmée, les produits ne seront plus disponibles pour un autre client.

L'interface de sélection des produits à livrer en fin de chaine au client devra être claire et facile à utiliser, notement pour les personnes qui prennent ces commandes au téléphone.

Temps estimés :
Analyse : 5h
Développement : 8h
Debug : 3h
Mise en production : 1h


Use cases :
- réserver la quantité vendue en On-Call et qu'elle ne soit plus dispo pour un autre
    - ok par la mécanique d'auto réservation
- stock réel : stock réel - commandes en sur-appel
    - ok avec l'ajout de la quantité owned
- organiser les picking out depuis les stock on-call
    -
- articles qui sont dans les on-call ne sont pas disponibles
- faire un flag sur les picking lists venant du sur-appel
- valorisation de l'inventaire : BSD + par clients

# TODO :
- voir les pickings depuis un oncall stock => OK
- voir les oncall stocks responsables d'un picking => OK
- ne plus créer le picking de base dans le SO lorsque la route OnCall est sélectionnée => OK
- marquer les lignes de commandes comme livrées quand on a livré les Pickings crées depuis les OnCall => OK
- Voir les pickings (crées depuis les OnCall) depuis les SO de base => OK
    - ajouter les pickings dans liste des picking de la vente (supprimer donc le bouton en +)
- faire un flag des pickings venant des OnCall => OK

- gérer la création des 2 ou 3 pickings (pick,pack,out) si le système est paramétré comme ça, lorsqu'on crée des pickings depuis des OnCall => OK, MAIS 1 picking par deliver
- faire une disctinction du montant dans la valorisation de l'inventaire => OK dans la vue inventory_valuation
- faire fonctionner la reord rule si la qty owned est < que le min (donc prendre en compte les oncall)

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
