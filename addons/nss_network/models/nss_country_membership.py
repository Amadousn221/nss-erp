# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class NssCountryMembership(models.Model):
    _name = "nss.country.membership"
    _description = "NSS Country Membership"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "country_id"

    country_id = fields.Many2one(
        "res.country",
        string="Pays",
        required=True,
        tracking=True,
        index=True,
    )
    status = fields.Selection(
        [
            ("fondateur", "Fondateur"),
            ("extension", "Extension"),
            ("observation", "Observation"),
            ("archive", "Archivé"),
        ],
        string="Statut NSS",
        required=True,
        default="extension",
        tracking=True,
    )
    join_date = fields.Date(string="Date d'entrée", tracking=True)
    exit_date = fields.Date(string="Date de sortie", tracking=True)
    coordinator_id = fields.Many2one(
        "res.partner",
        string="Coordinatrice / Représentante",
        tracking=True,
        domain="[('is_company', '=', False), ('nss_country_id', '!=', False)]",
        help="Personne coordinatrice ou représentante nationale NSS pour ce pays. "
        "Doit être une personne physique déjà rattachée à un pays NSS dans Contacts.",
    )
    focal_org_id = fields.Many2one(
        "res.partner",
        string="Organisation point focal",
        tracking=True,
        domain="[('is_company', '=', True), ('nss_org_type', '!=', False)]",
        help="Organisation jouant le rôle de point focal NSS pour ce pays, le cas échéant. "
        "Doit être une organisation NSS déjà configurée dans Contacts.",
    )
    active = fields.Boolean(string="Actif", default=True)
    notes = fields.Text(string="Notes")
    organization_ids = fields.One2many(
        "res.partner",
        "nss_country_id",
        string="Organisations rattachées",
    )
    organization_count = fields.Integer(
        string="Nombre d'organisations",
        compute="_compute_organization_count",
    )

    @api.depends("organization_ids")
    def _compute_organization_count(self):
        for record in self:
            record.organization_count = len(record.organization_ids)

    @api.constrains("country_id", "active")
    def _check_unique_active_country(self):
        for record in self:
            if not record.active:
                continue
            duplicate = self.search(
                [
                    ("id", "!=", record.id),
                    ("country_id", "=", record.country_id.id),
                    ("active", "=", True),
                ],
                limit=1,
            )
            if duplicate:
                raise ValidationError(
                    _(
                        "Il existe déjà une fiche NSS active pour le pays %(country)s. "
                        "Un seul enregistrement actif est autorisé par pays.",
                        country=record.country_id.display_name,
                    )
                )

    @api.constrains("join_date", "exit_date")
    def _check_dates_coherence(self):
        for record in self:
            if record.join_date and record.exit_date and record.exit_date < record.join_date:
                raise ValidationError(
                    _("La date de sortie ne peut pas être antérieure à la date d'entrée.")
                )

    @api.depends("country_id")
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.country_id.display_name or _("Nouveau pays NSS")
