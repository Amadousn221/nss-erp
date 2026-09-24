# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    nss_activity_type = fields.Selection(
        [
            ("formation", "Formation"),
            ("iec", "IEC"),
            ("camp", "Camp"),
            ("atelier", "Atelier"),
            ("plaidoyer", "Plaidoyer"),
            ("rencontre", "Rencontre"),
            ("autre", "Autre"),
        ],
        string="Type d'activité NSS",
        tracking=True,
    )
    nss_location = fields.Char(string="Lieu de l'activité")
