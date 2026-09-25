# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    nss_country_id = fields.Many2one(
        "nss.country.membership",
        string="Pays NSS",
        tracking=True,
        help="Pays membre NSS de rattachement de ce contact ou cette organisation.",
    )
    nss_org_type = fields.Selection(
        [
            ("afr", "Association de Femmes Rurales"),
            ("federation", "Fédération"),
            ("ong", "ONG"),
            ("coordination", "Coordination"),
            ("point_focal", "Point focal"),
            ("autre", "Autre"),
        ],
        string="Type d'organisation NSS",
        tracking=True,
    )
    nss_founding_member = fields.Boolean(
        string="Organisation fondatrice",
        tracking=True,
    )
