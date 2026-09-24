# -*- coding: utf-8 -*-
{
    "name": "NSS Network",
    "version": "18.0.1.0.0",
    "category": "Association",
    "summary": "Réseau NSS : pays, coordinations, organisations, adhésions",
    "description": """
NSS Network
===========

Addon spécifique unique pour Nous Sommes la Solution (NSS), conformément
à la décision Product Owner du 24 septembre 2026 (voir
docs/NSS_ERP_02_ARCHITECTURE_ODOO.md section 21).

Fournit :

* le suivi des pays membres du mouvement (nss.country.membership) ;
* l'adhésion des organisations (nss.membership) ;
* l'historique des responsabilités (nss.responsibility.history) ;
* des extensions sur les Contacts (res.partner) et les Projets
  (project.project, project.task).

Ce module ne contient aucune donnée réelle NSS et aucune dépendance
comptable (account, analytic explicite, OCA, localisation).
""",
    "author": "Nous Sommes la Solution (NSS)",
    "license": "LGPL-3",
    "depends": [
        "base",
        "contacts",
        "mail",
        "project",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/nss_country_membership_views.xml",
        "views/nss_membership_views.xml",
        "views/nss_responsibility_history_views.xml",
        "views/res_partner_views.xml",
        "views/project_views.xml",
        "views/nss_network_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
