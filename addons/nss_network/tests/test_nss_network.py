# -*- coding: utf-8 -*-
"""Tests unitaires nss_network.

Toutes les données utilisées sont fictives. Les pays réutilisés
(France, Belgique) servent uniquement de fixtures techniques natives
Odoo et ne représentent pas le périmètre géographique réel de NSS
(10 pays, chargés dans un checkpoint distinct après validation).
"""
from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestNssNetwork(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country_fr = cls.env.ref("base.fr")
        cls.country_be = cls.env.ref("base.be")
        cls.coordinator = cls.env["res.partner"].create({"name": "Coordinatrice Test"})
        cls.membership_fr = cls.env["nss.country.membership"].create(
            {
                "country_id": cls.country_fr.id,
                "status": "fondateur",
                "join_date": date(2020, 1, 1),
                "coordinator_id": cls.coordinator.id,
            }
        )

    def test_create_country_membership(self):
        self.assertEqual(self.membership_fr.status, "fondateur")
        self.assertEqual(self.membership_fr.coordinator_id, self.coordinator)
        self.assertTrue(self.membership_fr.active)

    def test_unique_active_country_membership(self):
        with self.assertRaises(ValidationError):
            self.env["nss.country.membership"].create(
                {
                    "country_id": self.country_fr.id,
                    "status": "extension",
                }
            )

    def test_inactive_country_membership_allows_new_active(self):
        self.membership_fr.active = False
        new_membership = self.env["nss.country.membership"].create(
            {
                "country_id": self.country_fr.id,
                "status": "extension",
            }
        )
        self.assertTrue(new_membership.active)

    def test_country_membership_date_constraint(self):
        with self.assertRaises(ValidationError):
            self.env["nss.country.membership"].create(
                {
                    "country_id": self.country_be.id,
                    "status": "observation",
                    "join_date": date(2024, 1, 1),
                    "exit_date": date(2023, 1, 1),
                }
            )

    def test_create_organization_linked_to_country(self):
        organization = self.env["res.partner"].create(
            {
                "name": "Association Test Fictive",
                "is_company": True,
                "nss_country_id": self.membership_fr.id,
                "nss_org_type": "afr",
                "nss_founding_member": True,
            }
        )
        self.assertIn(organization, self.membership_fr.organization_ids)
        self.assertEqual(self.membership_fr.organization_count, 1)

    def test_create_membership_adhesion(self):
        organization = self.env["res.partner"].create({"name": "Organisation Fictive Adhésion"})
        membership = self.env["nss.membership"].create(
            {
                "organization_id": organization.id,
                "status": "en_cours",
                "member_count_declared": 42,
            }
        )
        self.assertTrue(membership.currency_id)
        self.assertEqual(membership.member_count_declared, 42)

    def test_membership_date_constraint(self):
        organization = self.env["res.partner"].create({"name": "Organisation Fictive Dates"})
        with self.assertRaises(ValidationError):
            self.env["nss.membership"].create(
                {
                    "organization_id": organization.id,
                    "application_date": date(2024, 6, 1),
                    "admission_date": date(2024, 1, 1),
                }
            )

    def test_membership_negative_member_count(self):
        organization = self.env["res.partner"].create({"name": "Organisation Fictive Négative"})
        with self.assertRaises(ValidationError):
            self.env["nss.membership"].create(
                {
                    "organization_id": organization.id,
                    "member_count_declared": -5,
                }
            )

    def test_responsibility_history_is_current(self):
        person = self.env["res.partner"].create({"name": "Personne Fictive"})
        today = date.today()
        current = self.env["nss.responsibility.history"].create(
            {
                "partner_id": person.id,
                "country_membership_id": self.membership_fr.id,
                "role": "Coordinatrice Test",
                "date_start": today - timedelta(days=30),
            }
        )
        past = self.env["nss.responsibility.history"].create(
            {
                "partner_id": person.id,
                "country_membership_id": self.membership_fr.id,
                "role": "Ancienne fonction Test",
                "date_start": today - timedelta(days=400),
                "date_end": today - timedelta(days=100),
            }
        )
        future = self.env["nss.responsibility.history"].create(
            {
                "partner_id": person.id,
                "country_membership_id": self.membership_fr.id,
                "role": "Future fonction Test",
                "date_start": today + timedelta(days=30),
            }
        )
        self.assertTrue(current.is_current)
        self.assertFalse(past.is_current)
        self.assertFalse(future.is_current)

    def test_responsibility_history_date_constraint(self):
        person = self.env["res.partner"].create({"name": "Personne Fictive Dates"})
        with self.assertRaises(ValidationError):
            self.env["nss.responsibility.history"].create(
                {
                    "partner_id": person.id,
                    "role": "Fonction Incohérente Test",
                    "date_start": date(2024, 6, 1),
                    "date_end": date(2024, 1, 1),
                }
            )

    def test_project_project_extension(self):
        funder = self.env["res.partner"].create({"name": "Bailleur Fictif Test"})
        project = self.env["project.project"].create(
            {
                "name": "Projet Pilote Fictif",
                "nss_country_membership_ids": [(6, 0, [self.membership_fr.id])],
                "nss_program_tag": "Programme Test",
                "nss_funder_id": funder.id,
            }
        )
        self.assertIn(self.membership_fr, project.nss_country_membership_ids)
        self.assertEqual(project.nss_funder_id, funder)
        self.assertEqual(project.nss_program_tag, "Programme Test")

    def test_project_task_extension(self):
        project = self.env["project.project"].create({"name": "Projet Fictif Activités"})
        task = self.env["project.task"].create(
            {
                "name": "Atelier Fictif Test",
                "project_id": project.id,
                "nss_activity_type": "atelier",
                "nss_location": "Lieu Fictif",
            }
        )
        self.assertEqual(task.nss_activity_type, "atelier")
        self.assertEqual(task.nss_location, "Lieu Fictif")
