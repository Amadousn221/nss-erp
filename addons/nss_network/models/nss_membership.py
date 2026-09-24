# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class NssMembership(models.Model):
    _name = "nss.membership"
    _description = "NSS Organization Membership"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "organization_id"

    organization_id = fields.Many2one(
        "res.partner",
        string="Organisation",
        required=True,
        tracking=True,
        index=True,
    )
    status = fields.Selection(
        [
            ("en_cours", "En cours"),
            ("active", "Active"),
            ("expiree", "Expirée"),
            ("suspendue", "Suspendue"),
            ("archivee", "Archivée"),
        ],
        string="Statut d'adhésion",
        required=True,
        default="en_cours",
        tracking=True,
    )
    application_date = fields.Date(string="Date de demande")
    admission_date = fields.Date(string="Date d'adhésion effective")
    last_renewal_date = fields.Date(string="Dernier renouvellement")

    currency_id = fields.Many2one(
        "res.currency",
        string="Devise",
        required=True,
        default=lambda self: self.env.ref("base.XOF", raise_if_not_found=False)
        or self.env.company.currency_id,
    )
    fee_due = fields.Monetary(string="Cotisation due", currency_field="currency_id")
    fee_paid = fields.Monetary(string="Cotisation payée", currency_field="currency_id")

    member_count_declared = fields.Integer(string="Nombre de membres déclaré")
    member_count_date = fields.Date(string="Date de la déclaration")

    notes = fields.Text(string="Notes")

    @api.constrains("application_date", "admission_date", "last_renewal_date")
    def _check_dates_coherence(self):
        for record in self:
            if (
                record.application_date
                and record.admission_date
                and record.admission_date < record.application_date
            ):
                raise ValidationError(
                    _("La date d'adhésion effective ne peut pas être antérieure à la date de demande.")
                )
            if (
                record.admission_date
                and record.last_renewal_date
                and record.last_renewal_date < record.admission_date
            ):
                raise ValidationError(
                    _("La date de dernier renouvellement ne peut pas être antérieure à la date d'adhésion.")
                )

    @api.constrains("member_count_declared")
    def _check_member_count_declared(self):
        for record in self:
            if record.member_count_declared < 0:
                raise ValidationError(_("Le nombre de membres déclaré ne peut pas être négatif."))
