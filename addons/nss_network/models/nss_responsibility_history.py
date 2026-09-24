# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class NssResponsibilityHistory(models.Model):
    _name = "nss.responsibility.history"
    _description = "NSS Responsibility History"
    _inherit = ["mail.thread"]
    _order = "date_start desc"

    partner_id = fields.Many2one(
        "res.partner",
        string="Personne",
        required=True,
        tracking=True,
        index=True,
    )
    organization_id = fields.Many2one(
        "res.partner",
        string="Organisation",
        tracking=True,
        help="Organisation dans laquelle la fonction est exercée, le cas échéant.",
    )
    country_membership_id = fields.Many2one(
        "nss.country.membership",
        string="Pays NSS (coordination)",
        tracking=True,
        help="Renseigné lorsque la fonction concerne une coordination nationale NSS.",
    )
    role = fields.Char(string="Fonction", required=True, tracking=True)
    date_start = fields.Date(string="Début de fonction", required=True, tracking=True)
    date_end = fields.Date(string="Fin de fonction", tracking=True)
    is_current = fields.Boolean(
        string="En poste actuellement",
        compute="_compute_is_current",
        store=True,
    )
    notes = fields.Text(string="Notes")

    @api.depends("date_start", "date_end")
    def _compute_is_current(self):
        today = fields.Date.context_today(self)
        for record in self:
            record.is_current = bool(
                record.date_start
                and record.date_start <= today
                and (not record.date_end or record.date_end >= today)
            )

    @api.constrains("date_start", "date_end")
    def _check_dates_coherence(self):
        for record in self:
            if record.date_end and record.date_start and record.date_end < record.date_start:
                raise ValidationError(
                    _("La date de fin de fonction ne peut pas être antérieure à la date de début.")
                )
