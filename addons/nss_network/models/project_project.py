# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    nss_country_membership_ids = fields.Many2many(
        "nss.country.membership",
        string="Pays NSS concernés",
        tracking=True,
    )
    nss_program_tag = fields.Char(
        string="Programme NSS",
        help="Regroupement libre des projets par programme (MVP : simple champ texte).",
    )
    nss_funder_id = fields.Many2one(
        "res.partner",
        string="Bailleur principal",
        tracking=True,
        domain="[('is_company', '=', True)]",
        help="Le bailleur peut être extérieur au réseau NSS (pas de type d'organisation NSS requis).",
    )
